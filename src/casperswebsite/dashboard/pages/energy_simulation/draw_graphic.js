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
 */
function drawGraphic(ctx, ts, wind_distance, zenith) {
    // ts = ts === undefined ? 0 : ts;
    let dt = new Date((ts) * 1000);
    let sun_x_percentage = (dt.getUTCHours() * 3600 + dt.getUTCMinutes() * 60 + dt.getUTCSeconds()) / 86400;
    let startOfYear = Date.UTC(dt.getUTCFullYear(), 0, 0);
    let dayOfYear = Math.floor((dt.getTime() - startOfYear) / 86400000);
    let offset = Math.cos(2 * Math.PI * (dayOfYear - 172) / 365) * Math.sqrt(3) / 2;
    // let sun_y_percentage = offset + Math.cos(2 * Math.PI * sun_x_percentage + Math.PI);
    // console.log(Math.acos(zenith));
    let sun_y_percentage = zenith;
    let sun_x = (-0.2 + 1.4 * sun_x_percentage) * ctx.canvas.width;
    let sun_y = ctx.canvas.height * 2 / 3 - sun_y_percentage * ctx.canvas.height / 3;
    const min_brightness = 0.8
    let raw_brightness = (1 / (1 + Math.exp(-10 * (sun_y_percentage - 0.1))));
    let brightness = raw_brightness * (1 - min_brightness) + min_brightness;

    function brightnessAdjustedHSLA(hue, sat, lightness, alpha) {
        // Lightness is between 0 (black) and 100 (white)
        // We'll interpolate between the provided lightness and 100
        let adjustedLightness = lightness * brightness;
        let adjustedSaturation = sat * brightness;
   
        // Clamp adjustedLightness and adjustedSaturation between 0 and 100, and ensure they are integers
        adjustedLightness = Math.max(0, Math.min(100, adjustedLightness));
        adjustedSaturation = Math.max(0, Math.min(100, adjustedSaturation));

        return `hsla(${Math.round(hue)}, ${adjustedSaturation}%, ${adjustedLightness}%, ${alpha})`;

    }

    function drawSky() {
        // Sky (top 2/3)
        ctx.fillStyle = brightnessAdjustedHSLA(204, 100, 83, 1); // #a8ddff
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height * 2 / 3);
    }

    function drawGround() {
        // Grass (bottom 1/3)
        ctx.fillStyle = brightnessAdjustedHSLA(105, 54, 59, 1); // #6dcc57
        ctx.fillRect(0, ctx.canvas.height * 2 / 3, ctx.canvas.width, ctx.canvas.height / 3);
    }

    /**
     * @param {number} x
     * @param {number} y
     * @param {number} [scale]
     * @param {number} [bladeAngle]
     */
    function drawTurbine(x, y, scale=1, bladeAngle=0) {
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(scale, scale);

        // Draw the tower
        ctx.save();
        ctx.strokeStyle = brightnessAdjustedHSLA(0, 0, 85, 1); // #d9d9d9
        ctx.fillStyle = brightnessAdjustedHSLA(0, 0, 85, 1);   // #d9d9d9
        ctx.lineWidth = 8;
        ctx.beginPath();
        ctx.moveTo(0, 30);
        ctx.lineTo(0, 120); // Tower base point
        ctx.stroke();
        ctx.restore();

        // Hub shadow/outline, for a slight 3D effect
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 30, 11, 0, Math.PI * 2, false);
        ctx.fillStyle = brightnessAdjustedHSLA(0, 0, 69, 1); // #b1b1b1
        ctx.globalAlpha = 0.3;
        ctx.fill();
        ctx.restore();

        // Draw the hub
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 30, 9, 0, Math.PI * 2, false);
        ctx.fillStyle = brightnessAdjustedHSLA(0, 0, 93, 1); // #eeeeee
        ctx.shadowColor = brightnessAdjustedHSLA(192, 68, 83, 1); // #b5e0f1
        ctx.shadowBlur = 2;
        ctx.fill();
        ctx.restore();

        // Draw the blades
        for (let i = 0; i < 3; i++) {
            ctx.save();
            // Center at turbine hub
            ctx.translate(0, 30);
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

    function drawSolarPanels(x, y, scale = 1) {
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(scale, scale);

        // Solar panel as a low-base trapezoid
        // Panel dimensions
        const baseWidth = 64;    // bottom of panel
        const topWidth = 48;     // top of panel
        const height = 22;
        const cellRows = 2, cellCols = 4;

        // Draw legs/poles
        ctx.save();
        ctx.strokeStyle = brightnessAdjustedHSLA(205, 8, 30, 1);
        ctx.lineWidth = 4;
        // Poles at 1/4 and 3/4 along the base
        for (let i of [-0.3, 0.3]) {
            let px = i * (baseWidth * 0.5);
            ctx.beginPath();
            ctx.moveTo(px, height + 2);
            ctx.lineTo(px, height + 18);
            ctx.stroke();
        }
        ctx.restore();

        ctx.save();

        // Draw trapezoidal panel frame
        ctx.beginPath();
        ctx.moveTo(-baseWidth / 2, height);     // Bottom left
        ctx.lineTo(baseWidth / 2, height);      // Bottom right
        ctx.lineTo(topWidth / 2, 0);            // Top right
        ctx.lineTo(-topWidth / 2, 0);           // Top left
        ctx.closePath();

        ctx.fillStyle = brightnessAdjustedHSLA(210, 15, 76, 1); // silvery frame
        ctx.strokeStyle = brightnessAdjustedHSLA(210, 8, 61, 1);
        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();

        // Draw cells as smaller trapezoids inside the panel
        for (let r = 0; r < cellRows; r++) {
            for (let c = 0; c < cellCols; c++) {
                // Linear interpolation on top/bottom widths for left/right of cells
                let cellPad = 2;
                let tY1 = height * r / cellRows + cellPad / 2;
                let tY2 = height * (r + 1) / cellRows - cellPad / 2;
                // Widths at these Ys
                let widthAtY1 = topWidth + (baseWidth - topWidth) * (tY1 / height);
                let widthAtY2 = topWidth + (baseWidth - topWidth) * (tY2 / height);
                // X extents for this cell
                let x1 = -widthAtY1 / 2 + (widthAtY1 * c / cellCols) + cellPad / 2;
                let x2 = -widthAtY1 / 2 + (widthAtY1 * (c + 1) / cellCols) - cellPad / 2;
                let x3 = -widthAtY2 / 2 + (widthAtY2 * (c + 1) / cellCols) - cellPad / 2;
                let x4 = -widthAtY2 / 2 + (widthAtY2 * c / cellCols) + cellPad / 2;
                ctx.beginPath();
                ctx.moveTo(x1, tY1);
                ctx.lineTo(x2, tY1);
                ctx.lineTo(x3, tY2);
                ctx.lineTo(x4, tY2);
                ctx.closePath();

                const interp = (a, b) => a + (b - a) * raw_brightness;
                // Make the cells a vibrant, electric blue, evocative of energy and power.
                const h = interp(220, 205);   // Base to more electric blue
                const s = interp(15, 100);    // High saturation for vibrancy
                const l = interp(15, 55);     // Medium lightness for intensity
        
                ctx.fillStyle = `hsla(${h}, ${s}%, ${l}%, 0.92)`;
                ctx.fill();
            }
        }

        ctx.restore();
        ctx.restore();
    }


    drawSky();
    drawSun();
    drawGround();

    const static_rand = seededRandom(0);
    for (var i = 0; i < 7; i++) {
        drawCloud(Math.floor(4294967296 * static_rand()));
    }

    const rand = seededRandom(ts);
    drawTurbine(700, 350, 1, wind_distance / 50);
    drawSolarPanels(300, 420, 1);
}