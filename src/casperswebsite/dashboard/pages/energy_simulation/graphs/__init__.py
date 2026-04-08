from bokeh.models import CustomJS
from bokeh.models.dom import DOMElement

from casperswebsite.dashboard.pages.energy_simulation.cds import SunIntensity, WindData


def get_plots() -> dict[str, DOMElement]:
    from bokeh.plotting import figure

    wind_graph = figure(
        title="Wind speed",
        sizing_mode="stretch_both",
        toolbar_location=None,
        y_range=[0, 25],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    wind_graph.toolbar.tools = []
    wind_graph.line(x=WindData.ts, y=WindData.speed, source=WindData.source)

    WindData.source.js_on_change("data", CustomJS(args={"wind_graph": wind_graph}, code=f"var ts = cb_obj.data.{WindData.ts};wind_graph.x_range.start = ts[0]; wind_graph.x_range.end = ts[ts.length - 1];"))

    solar_graph = figure(
        title="Solar irradiance",
        sizing_mode="stretch_both",
        toolbar_location=None,
        y_range=[0, 1500],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    solar_graph.toolbar.tools = []
    solar_graph.line(x=SunIntensity.ts, y=SunIntensity.intensity, source=SunIntensity.source)

    SunIntensity.source.js_on_change("data", CustomJS(args={"solar_graph": solar_graph}, code=f"var ts = cb_obj.data.{WindData.ts};solar_graph.x_range.start = ts[0]; solar_graph.x_range.end = ts[ts.length - 1];"))


    return {"wind_graph": wind_graph, "solar_graph": solar_graph}
