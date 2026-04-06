import os

from casperswebsite.dashboard.pages.energy_simulation.cds import dataflow
from casperswebsite.dashboard.pages.energy_simulation.graphs import get_plots
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
    #: Plot frame in the same design coordinates as the old 1080×720 html-layer (before
    #: transform scale(stageW/1000, stageH/600)).

    def build_page(self) -> PageInfo:
        plots = get_plots(dataflow)

        bokeh_script, bokeh_divs = dataflow.get_components_and_script(plots)
        bokeh_sources = "".join(div for key, div in bokeh_divs.items() if key.startswith("source_"))

        graphs = [{"div": bokeh_divs["dummy_fig"], "left": 120, "top": 80, "width": 200, "height": 100}]


        anchors = "\n".join(f'''  <div id="anchor-{i}" style="position:absolute; pointer-events: auto;">{graph["div"]}</div>''' for (i, graph) in enumerate(graphs))
        anchor_vars = "\n".join(f"    const anchor_{i} = document.getElementById('anchor-{i}');" for i in range(len(graphs)))
        anchor_rescales = "".join(f"""
        anchor_{i}.style.left = ({graph["left"]} * scaleX) + "px";
        anchor_{i}.style.top = ({graph["top"]} * scaleY) + "px";
        anchor_{i}.style.width = ({graph["width"]} * scaleX) + "px";
        anchor_{i}.style.height = ({graph["height"]} * scaleY) + "px";""" for (i, graph) in enumerate(graphs))

        svg_and_layers = (
            f"""
<div class="stage" style="position: relative; width: 100%; aspect-ratio: 1000 / 600; overflow: hidden;">
  <canvas id="energy-canvas" width="1000" height="600" style="position:absolute;inset:0;width:100%;height:100%;display:block;"></canvas>
  {anchors}
</div>
<script>
    const stage = document.querySelector('.stage');
    {anchor_vars}
    const canvas = document.getElementById('energy-canvas');
    const ctx = canvas.getContext('2d');
    const plotDesign = {{ left: 120, top: 80, width: {self.WIDTH//2}, height: 200 }};

    function syncPlotFrame() {{
        const w = stage.clientWidth;
        const h = stage.clientHeight;
        const scaleX = w / 1000;
        const scaleY = h / 600;
        canvas.style.width = w + "px";
        canvas.style.height = h + "px";
        {anchor_rescales}
    }}

    function resizeAndRedraw() {{
        syncPlotFrame();
    }}

    new ResizeObserver(resizeAndRedraw).observe(stage);
    drawGraphic(ctx);
    resizeAndRedraw();
</script>
"""
        )
        header_html = f"<script>{DRAW_GRAPHIC_FUNC}</script>" + bokeh_script + bokeh_sources
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
                ),
                # CardInfo(
                #     title="Bokeh Divs",
                #     containers=[
                #         ContainerInfo(
                #             width=12,
                #             embed_type=EmbedType.Html,
                #             content="".join(bokeh_sources.values()),
                #         ),
                #     ],
                # )
            ],
        )
