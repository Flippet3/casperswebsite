import os

from casperswebsite.dashbuilder.contract import (
    CardInfo,
    ContainerInfo,
    EmbedType,
    OverViewCategory,
    PageInfo,
)


draw_graphic_js_path = os.path.join(os.path.dirname(__file__), "draw_graphic.js")
with open(draw_graphic_js_path, encoding="utf-8") as f:
    DRAW_GRAPHIC_FUNC = f.read()


class EnergySimulationPage:
    WIDTH = 1080
    HEIGHT = 720

    def build_page(self) -> PageInfo:

        svg_and_layers = """
<div class="stage" style="position: relative; width: 100%; aspect-ratio: 1000 / 600; overflow: hidden;">
  <canvas id="energy-canvas" width="1000" height="600" style="position:absolute;inset:0;width:100%;height:100%;display:block;"></canvas>
  <div class="html-layer" style="position:absolute;inset:0;width:1080px;height:720px;transform-origin:top left; pointer-events: none;">
    <div style="position:absolute;left:120px; top:80px; width:180px; height:100px; pointer-events: auto;"><p>hi</p></div>
  </div>
</div>
<script>
    const stage = document.querySelector('.stage');
    const htmlLayer = document.querySelector('.html-layer');
    const canvas = document.getElementById('energy-canvas');
    const ctx = canvas.getContext('2d');

    // Scale overlay and canvas for responsive design
    function syncOverlayScale() {
        const scaleX = stage.clientWidth / 1000;
        const scaleY = stage.clientHeight / 600;
        htmlLayer.style.transform = `scale(${scaleX}, ${scaleY})`;
        canvas.style.width = stage.clientWidth + "px";
        canvas.style.height = stage.clientHeight + "px";
    }

    function resizeAndRedraw() {
        // We do NOT resize canvas element inner size (width/height), only scale visually
        // Redraw the static background
        drawGraphic(ctx);
        syncOverlayScale();
    }

    new ResizeObserver(resizeAndRedraw).observe(stage);

    // Initial draw
    drawGraphic(ctx);
    syncOverlayScale();
</script>
"""
        header_html = f"<script>{DRAW_GRAPHIC_FUNC}</script>"
        return PageInfo(
            category=OverViewCategory.EnergySimulation,
            title="Energy Simulation",
            header_html=header_html,
            cards=[
                CardInfo(
                    title="What is this?",
                    containers=[
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Text,
                            content="""
                                Casper is my name, and power is my game. 
                                Domain-wise, I've learned a lot about electricity markets and renewable power generation. 
                                Skill-wise, I've learned a lot about visualization of data and creating dashboards. This is a page to combine the two!
                                <br><br>
                                I've made a little scene that visualizes some energy production and demand.
                                I've then made some graphs that give insight into what's happening in the scene.
                                Then there's also some levers you can pull to influence the state of energy production.
                                Can you optimize profit?!
                            """,
                        ),
                    ],
                ),
                CardInfo(
                    title="Scene",
                    body_style="padding:0!important;",
                    containers=[
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Html,
                            content=svg_and_layers,
                        ),
                    ],
                )
            ],
        )
