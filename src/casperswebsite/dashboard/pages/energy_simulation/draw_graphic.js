/**
 * @param {CanvasRenderingContext2D} ctx - The canvas 2D rendering context.
 */
function drawGraphic(ctx) {
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
    drawBackground();
    drawTurbine(700, 350, 1, 0);
}