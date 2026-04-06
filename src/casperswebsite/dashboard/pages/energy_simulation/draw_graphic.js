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
function drawGraphic(ctx, ts, wind_distance) {
    function drawBackground() {
        // Sky (top 2/3)
        ctx.fillStyle = "#a8ddff";
        ctx.fillRect(0, 0, ctx.canvas.width, 400);
        // Grass (bottom 1/3)
        ctx.fillStyle = "#6dcc57";
        ctx.fillRect(0, 400, ctx.canvas.width, 200);
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
        ctx.strokeStyle = "#d9d9d9";
        ctx.fillStyle = "#d9d9d9";
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
        ctx.fillStyle = "#b1b1b1";
        ctx.globalAlpha = 0.3;
        ctx.fill();
        ctx.restore();

        // Draw the hub
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 30, 9, 0, Math.PI * 2, false);
        ctx.fillStyle = "#eeeeee";
        ctx.shadowColor = "#b5e0f1";
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

            ctx.fillStyle = "#f8f9fa";
            ctx.strokeStyle = "#ccc";
            ctx.lineWidth = 2;
            ctx.shadowColor = "#e1f2fc";
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

        ctx.fillStyle = "#e2f1fb";
        ctx.strokeStyle = "#bee0ee00";
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
    drawBackground();

    const static_rand = seededRandom(0);
    for (var i = 0; i < 7; i++) {
        drawCloud(Math.floor(4294967296 * static_rand()));
    }

    const rand = seededRandom(ts);
    drawTurbine(700, 350, 1, wind_distance / 50);
}