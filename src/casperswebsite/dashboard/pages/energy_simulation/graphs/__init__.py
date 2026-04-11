from bokeh.models import CustomJS
from bokeh.models.dom import DOMElement

from casperswebsite.dashboard.pages.energy_simulation.cds import SunIntensity, WindData
from casperswebsite.dashboard.pages.energy_simulation.graphs.styled import styled_figure


def get_plots() -> dict[str, DOMElement]:

    wind_graph = styled_figure(
        title="Wind speed",
        y_range=[0, 25],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0,
    )
    wind_graph.line(x=WindData.ts, y=WindData.speed, source=WindData.source)

    WindData.source.js_on_change("data", CustomJS(args={"wind_graph": wind_graph}, code=f"var ts = cb_obj.data.{WindData.ts};wind_graph.x_range.start = ts[0]; wind_graph.x_range.end = ts[ts.length - 1];"))

    solar_graph = styled_figure(
        title="Solar irradiance",
        y_range=[0, 1500],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    solar_graph.line(x=SunIntensity.ts, y=SunIntensity.intensity, source=SunIntensity.source)

    SunIntensity.source.js_on_change("data", CustomJS(args={"solar_graph": solar_graph}, code=f"var ts = cb_obj.data.{WindData.ts};solar_graph.x_range.start = ts[0]; solar_graph.x_range.end = ts[ts.length - 1];"))


    return {"wind_graph": wind_graph, "solar_graph": solar_graph}
