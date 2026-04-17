function seededRandom(seed) {
    // Simple LCG: https://en.wikipedia.org/wiki/Linear_congruential_generator
    // Constants from Numerical Recipes
    let m = 4294967296, // 2^32
        a = 1664525,
        c = 1013904223;
    let state = seed % m;
    return function () {
      state = (a * state + c) % m;
      return state / m;
    }
}

/**
 * @param {CanvasRenderingContext2D} ctx - The canvas 2D rendering context.
 * @param {number} ts - Timestamp.
 * @param {number} wind_distance - Aggregate of wind_speed * time.
 * @param {number} zenith - Angle of the sun w.r.t. the horizon.
 * @param {number} nr_turbines - Indicator of how many wind turbines should be drawn.
 * @param {number} solar_panel_size - Indicator of how many solar panels are activated.
 */
function drawGraphic(ctx, ts, wind_distance, zenith, nr_turbines, solar_panel_size) {
    let dt = new Date((ts) * 1000);
    let sun_x_percentage = (dt.getUTCHours() * 3600 + dt.getUTCMinutes() * 60 + dt.getUTCSeconds()) / 86400;
    let sun_y_percentage = zenith;
    let sun_x = (-0.2 + 1.4 * sun_x_percentage) * ctx.canvas.width;
    let sun_y = ctx.canvas.height * 5 / 6 - sun_y_percentage * ctx.canvas.height * 2 / 3;
    const min_brightness = 0.8
    let raw_brightness = (1 / (1 + Math.exp(-10 * (sun_y_percentage - 0.1))));
    let brightness = raw_brightness * (1 - min_brightness) + min_brightness;

    function brightnessAdjustedHSLA(hue, sat, lightness, alpha) {
        let adjustedLightness = lightness * brightness;
        let adjustedSaturation = sat * brightness;
   
        adjustedLightness = Math.max(0, Math.min(100, adjustedLightness));
        adjustedSaturation = Math.max(0, Math.min(100, adjustedSaturation));

        return `hsla(${Math.round(hue)}, ${adjustedSaturation}%, ${adjustedLightness}%, ${alpha})`;

    }

    function z_to_y(z) {
        return 100 / z + 500;
    }

    function y_to_z(y) {
        return 100 / (y - 500);
    }

    
    function drawSky() {
        // Sky (top 2/3)
        ctx.fillStyle = brightnessAdjustedHSLA(204, 100, 83, 1); // #a8ddff
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height * 5 / 6);
    }

    function drawGround() {
        // Grass (bottom 1/3)
        ctx.fillStyle = brightnessAdjustedHSLA(105, 54, 59, 1); // #6dcc57
        ctx.fillRect(0, ctx.canvas.height * 5 / 6, ctx.canvas.width, ctx.canvas.height / 6);
    }


    function drawTurbine(x, y, scale=1, bladeAngle=0) {
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(scale, scale);

        // Draw the tower up from current (x, y) position — base is at origin, tower extends upward
        ctx.save();
        ctx.strokeStyle = brightnessAdjustedHSLA(0, 0, 85, 1); // #d9d9d9
        ctx.fillStyle = brightnessAdjustedHSLA(0, 0, 85, 1);   // #d9d9d9
        ctx.lineWidth = 8;
        ctx.beginPath();
        ctx.moveTo(0, 0);     // Tower base at origin
        ctx.lineTo(0, -90);   // Tower goes upward (negative Y)
        ctx.stroke();
        ctx.restore();

        // Hub shadow/outline, for a slight 3D effect
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, -90, 11, 0, Math.PI * 2, false); // Hub at tower top (y = -90)
        ctx.fillStyle = brightnessAdjustedHSLA(0, 0, 69, 1); // #b1b1b1
        ctx.globalAlpha = 0.3;
        ctx.fill();
        ctx.restore();

        // Draw the hub
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, -90, 9, 0, Math.PI * 2, false);
        ctx.fillStyle = brightnessAdjustedHSLA(0, 0, 93, 1); // #eeeeee
        ctx.shadowColor = brightnessAdjustedHSLA(192, 68, 83, 1); // #b5e0f1
        ctx.shadowBlur = 2;
        ctx.fill();
        ctx.restore();

        // Draw the blades
        for (let i = 0; i < 3; i++) {
            ctx.save();
            // Center at turbine hub (top of tower)
            ctx.translate(0, -90);
            // Set angle for blade: 3 equally spaced
            let angle = bladeAngle + i * (2 * Math.PI / 3);
            ctx.rotate(angle);

            // Draw one blade
            ctx.beginPath();
            // Blade shape: a rounded rectangle-ish blade, fairly lightweight
            ctx.moveTo(-7, -10);
            ctx.quadraticCurveTo(-9, -35, 0, -70);  // left edge curve
            ctx.quadraticCurveTo(9, -35, 7, -10);   // right edge curve
            ctx.lineTo(3, 0);
            ctx.arc(0, 0, 3, 0, Math.PI, true); // root/bulge at hub
            ctx.closePath();

            ctx.fillStyle = brightnessAdjustedHSLA(210, 32, 98, 1); // #f8f9fa
            ctx.strokeStyle = brightnessAdjustedHSLA(0, 0, 80, 1); // #ccc
            ctx.lineWidth = 2;
            ctx.shadowColor = brightnessAdjustedHSLA(199, 70, 94, 1); // #e1f2fc
            ctx.shadowBlur = 1;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.stroke();

            ctx.restore();
        }

        ctx.restore();
    }

    /**
     * Draws a "cone" of wind turbines, with row/col calculated directly per index.
     * Each row has r+1 turbines; row computed by: row = floor((sqrt(8*idx+1)-1)/2).
     * Column is idx - (row*(row+1))/2.
     * Draws back-to-front for proper overlap. Blade jitter is deterministic per idx.
     */
    function drawTurbines(x, y, nr_turbines, seed, scale=1, bladeAngle=0) {
        if (y < 500 || y > 600) return;

        // Draw from max index (furthest/backmost) to 0 (nearest/frontmost)
        // so that foreground turbines overlap background ones
        let z_zero = y_to_z(y);
        let z_step = 1;
        let spread = 50 / (z_zero/(z_zero+z_step));

        // Prepare deterministic random jitter for each turbine
        let perTurbineRand = seededRandom(seed);

        // To ensure deterministic jitter, generate and cache all jitters front-to-back
        let jitters = [];
        for (let i = 0; i < nr_turbines; i++) {
            jitters[i] = (perTurbineRand() - 0.5) * Math.PI;
        }

        // Draw backmost (largest idx) to frontmost (idx=0)
        for (let idx = nr_turbines - 1; idx >= 0; idx--) {
        // for (let idx = 0; idx <= 0; idx++) {
            // Row: floor((sqrt(8*idx+1)-1)/2)
            let row = Math.floor((Math.sqrt(8 * idx + 1) - 1) / 2);
            // Column within row
            let col = idx - (row * (row + 1)) / 2;
            // Only draw when col is lower than 2, or higher than row - 2
            if (!(col < 2 || col > row - 2)) continue;
            if (row > 8) continue;
    

            // In each row, # turbines = row+1
            let in_this_row = row + 1;
            let row_z = z_zero + z_step * row;
            let row_y = z_to_y(row_z);
            let turbine_scale = scale * (z_zero/row_z)
            let row_spread = row * spread * (z_zero/row_z);

            // Evenly space across the row
            let fx = (in_this_row === 1)
                ? 0
                : (-row_spread / 2) + (row_spread * col / (in_this_row - 1));
            let tx = x + fx;

            drawTurbine(
                tx,
                row_y,
                turbine_scale,
                bladeAngle + jitters[idx]
            );
        }
    }

    function drawCloud(seed) {
        let rand = seededRandom(seed);
        let cycleLength = 1000 * (0.5 + rand());
        let percentage_offset = rand();
        let cloud_id = Math.floor(wind_distance/cycleLength + percentage_offset);
        let percentage = wind_distance/cycleLength + percentage_offset - Math.floor(wind_distance/cycleLength + percentage_offset);
        let cloudrand = seededRandom(seed + cloud_id);
        // console.log(cloudrand());
        let cloudY = ctx.canvas.height * (0.05  + 0.1 * cloudrand());
        // console.log(cloudY);
        ctx.save();
        // Cloud horizontal position moves with "percentage" (looping across width)
        let cloudX = ctx.canvas.width * (-0.2 + 1.2 * percentage); // canvas width assumed 700
        ctx.translate(cloudX, cloudY);

        ctx.fillStyle = brightnessAdjustedHSLA(203, 65, 95, 1); // #e2f1fb
        ctx.strokeStyle = "hsla(190, 56%, 84%, 0)"; // #bee0ee00 transparent
        ctx.lineWidth = 1.8;
        
        // Cloud body: draw 3-5 ellipses/circles for a fluffy look
        let numBlobs = 10 + Math.floor(cloudrand() * 10);
        let peak_i = (0.25 + 0.5 * percentage) * numBlobs;
        for (let i = 0; i < numBlobs; i++) {
            let f = 1 - (Math.abs(i - peak_i) / numBlobs * 4);
            let offsetX = (i - (numBlobs - 1) / 2) * 14 + 8 * (cloudrand() - 0.5);
            let offsetY = 8 * (cloudrand() - 0.5);
            let radX = (26 + 12 * cloudrand()) * f;
            let radY = (17 + 8 * cloudrand()) * f;
            if (f > 0.001) {
                ctx.save();
                ctx.globalAlpha = f;
                ctx.beginPath();
                ctx.ellipse(offsetX, offsetY, radX, radY, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
                ctx.restore();
            }
        }

        ctx.restore();
    }
    function drawSun() {
        ctx.save();
        ctx.translate(sun_x, sun_y);

        // Draw outer (yellow) sun with radial gradient fading edge
        let outerRadius = 48;
        let innerRadius = 0;
        let gradient = ctx.createRadialGradient(0, 0, innerRadius, 0, 0, outerRadius);
        gradient.addColorStop(0, brightnessAdjustedHSLA(51, 100 / brightness, 50 / brightness, 1));
        gradient.addColorStop(0.6, brightnessAdjustedHSLA(48, 100 / brightness, 64 / brightness, 0.7));
        gradient.addColorStop(1, brightnessAdjustedHSLA(51, 100 / brightness, 50 / brightness, 0));
        ctx.beginPath();
        ctx.arc(0, 0, outerRadius, 0, 2 * Math.PI, false);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Draw inner (white) sun with strong center and fading edge
        let whiteRadius = 24;
        let whiteGradient = ctx.createRadialGradient(0, 0, 0, 0, 0, whiteRadius);
        // Decreasing stops from 0 to 1 by 0.1, lightness (L) from 1100 to 100
        for (let t = 10; t >= 0; t -= 1) {
            let alpha = Math.max(Math.min(brightness * t, 1), 0);
            whiteGradient.addColorStop((10-t) / 10, brightnessAdjustedHSLA(0, 0, 2000, alpha));
        }
        ctx.beginPath();
        ctx.arc(0, 0, whiteRadius, 0, 2*Math.PI, false);
        ctx.fillStyle = whiteGradient;
        ctx.fill();

        ctx.restore();
    }

    function drawSolarPanels(x, y, scale = 1, nr_solar_panels) {
        ctx.save();

        let grid_x_size = 11;
        let grid_z_size = 0.06;
        let cell_percentage = 0.8;
        let grid_origin_x = x;
        let grid_origin_z = y_to_z(y);


        let x_translate = Math.pow(nr_solar_panels, 1/4);
        let w = Math.ceil(x_translate);
        let prev_w = w - 1;
        let full_width_rows = nr_solar_panels - Math.pow(prev_w, 4);

        let h_grid = Math.max(nr_solar_panels / w, Math.pow(prev_w, 3));

        let base_z = grid_origin_z;
        let base_y = z_to_y(base_z);
        let base_left_x = grid_origin_x - (x_translate / 2) * grid_x_size / base_z;
        let base_right_x = grid_origin_x - ((x_translate / 2) - w) * grid_x_size / base_z;

        let top_z = grid_origin_z + h_grid * grid_z_size;
        let top_y = z_to_y(top_z);
        let top_left_x = grid_origin_x - (x_translate / 2) * grid_x_size / top_z;
        let top_right_x = grid_origin_x - ((x_translate / 2) - w) * grid_x_size / top_z;

        // Draw trapezoidal panel frame using grid width and height
        ctx.beginPath();
        ctx.moveTo(base_left_x, base_y);   // Bottom left
        ctx.lineTo(base_right_x, base_y);  // Bottom right
        ctx.lineTo(top_right_x, top_y);    // Top right
        ctx.lineTo(top_left_x, top_y);     // Top left
        ctx.closePath();

        ctx.fillStyle = brightnessAdjustedHSLA(210, 15, 76, 1); // silvery frame
        ctx.strokeStyle = brightnessAdjustedHSLA(210, 8, 61, 1);
        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();

        const interp = (a, b) => a + (b - a) * raw_brightness;
        // Make the cells a vibrant, electric blue, evocative of energy and power.
        const h = interp(220, 205);   // Base to more electric blue
        const s = interp(15, 100);    // High saturation for vibrancy
        const l = interp(15, 55);     // Medium lightness for intensity

        ctx.fillStyle = `hsla(${h}, ${s}%, ${l}%, 0.92)`;

        function i_to_gx_gz(input_i) {
            let gz, gx;
            if (Math.floor(input_i) <= w * full_width_rows) {
                gz = Math.floor(Math.floor(input_i) / w);
                gx = Math.floor(input_i) - gz * w;
            } else {
                let j = Math.floor(input_i) - w * full_width_rows;
                gz = Math.floor(full_width_rows + (j / (w - 1)));
                gx = Math.floor(j % (w - 1));
            }
            return [gx, gz];
        }

        let i = 0;
        let stride = 0;
        let rows_left = 3;
        while (i < nr_solar_panels) {
            let [gx, gz] = i_to_gx_gz(i);
            if (gx == 0) {
                rows_left -= 1;
                i += stride * w
                i -= i_to_gx_gz(i)[0] // Manage shorter columns.
                if (rows_left < 0) {
                    rows_left = 3;
                    stride = Math.max(1, stride * 2);
                }
            }
    
            let raw_dx = (gx - x_translate / 2) * grid_x_size;
            let cell_width = grid_x_size * cell_percentage;
            let raw_z = grid_origin_z + gz * grid_z_size;
            let z_size = (grid_z_size * cell_percentage) + grid_z_size * stride;

            
            let y1 = z_to_y(raw_z);
            let y2 = z_to_y(raw_z + z_size);

            // X extents for this cell
            let x1 = grid_origin_x + (raw_dx) / (raw_z);
            let x2 = grid_origin_x + (raw_dx + cell_width) / (raw_z);
            let x3 = grid_origin_x + (raw_dx + cell_width) / (raw_z + z_size);
            let x4 = grid_origin_x + (raw_dx) / (raw_z + z_size);

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y1);
            ctx.lineTo(x3, y2);
            ctx.lineTo(x4, y2);
            ctx.closePath();
            ctx.fill();

            i += 1;
        }
        ctx.restore();
    }


    drawSky();
    drawSun();
    drawGround();

    const static_rand = seededRandom(0);
    for (var i = 0; i < 7; i++) {
        drawCloud(Math.floor(4294967296 * static_rand()));
    }

    // Distance rules on the ground. 
    // 500 is infinitely far away.
    // 600 is at a scale of 1.
    // This means that scale at Y:
    // Frac to top of screen = Y_P = ((600 - 500) - (Y - 500)) / (600 - 500)
    // Scale = Z = 1/(1-Y_P)  // When Y_P = 0 (Y=600), we're at 1, when Y_P = 1 (Y=500), we're at infinite.
    // Y_P = (600 - 500 - Y + 500) / (600 - 500) = (600 - Y) / 100
    // Z = 1/(1 - (600 - Y) / 100) = 100 / (100 - (600 - Y)) = 100 / (Y - 500)  // Makes sense, because at Y = 500, we're at inf; at Y = 600; we're at 1.

    drawTurbines(325, 570, Math.floor(nr_turbines), 4294967296 * static_rand(), 1, wind_distance / 10);
    drawSolarPanels(120, 580, 1, solar_panel_size);

    // let start_dt = 365.25 * 24 * 3600 / 4 - 6 * 60 * 60
    // let nr_squares = Math.floor((ts - start_dt)/900);
    // let w = Math.ceil(Math.pow(nr_squares, 1/3));
    // let prev_w = w - 1;
    // let full_width_rows = nr_squares - Math.pow(prev_w, 3);
    
    // let square_spacing = 7;
    // let square_size = 5;
    // let grid_origin_x = 0;
    // let grid_origin_y = 0;

    // ctx.save();
    // for (let i = 0; i < nr_squares; i++) {
    //     let gy, gx;
    //     if (i <= w * full_width_rows) {
    //         gy = Math.floor(i / w);
    //         gx = i - gy * w;
    //     } else {
    //         let j = i - w * full_width_rows;
    //         gy = full_width_rows + Math.floor(j / (w - 1));
    //         gx = j % (w - 1);
    //     }

    //     let x = grid_origin_x + gx * square_spacing;
    //     let y = grid_origin_y + gy * square_spacing;
    //     ctx.beginPath();
    //     ctx.rect(x, y, square_size, square_size);
    //     ctx.fillStyle = `hsla(220, 80%, 65%, 0.75)`;
    //     ctx.fill();
    //     ctx.lineWidth = 1;
    //     ctx.strokeStyle = `hsla(220, 50%, 35%, 0.25)`;
    //     ctx.stroke();
    // }
    // ctx.restore();
}