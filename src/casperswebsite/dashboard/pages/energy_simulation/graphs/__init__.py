from bokeh.models import CustomJS
from bokeh.models.dom import DOMElement

from casperswebsite.dashboard.pages.energy_simulation.cds import LoadConfig, SunIntensity, WindData
from casperswebsite.dashboard.pages.energy_simulation.graphs.styled import load_styled_figure, styled_figure


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

    wind_load_graph = load_styled_figure(
        title="Wind load",
        y_range=[0, 5500000 * LoadConfig.nr_5mw_tubrines.linked_column.cds_flow_column.initial_value[0]],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    wind_load_graph.line(x=WindData.ts, y=WindData.load, source=WindData.source)

    WindData.source.js_on_change("data", CustomJS(args={"wind_load_graph": wind_load_graph}, code=f"var ts = cb_obj.data.{WindData.ts};wind_load_graph.x_range.start = ts[0]; wind_load_graph.x_range.end = ts[ts.length - 1];"))
    WindData.source.js_on_change("data", CustomJS(args={"wind_load_graph": wind_load_graph, "load_config": LoadConfig.source}, code=f"var nr_turbines = load_config.data.{LoadConfig.nr_5mw_tubrines}[0];wind_load_graph.y_range.end = nr_turbines * 5500000;"))

    solar_graph = styled_figure(
        title="Solar irradiance",
        y_range=[0, 1500],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    solar_graph.line(x=SunIntensity.ts, y=SunIntensity.intensity, source=SunIntensity.source)

    SunIntensity.source.js_on_change("data", CustomJS(args={"solar_graph": solar_graph}, code=f"var ts = cb_obj.data.{SunIntensity.ts};solar_graph.x_range.start = ts[0]; solar_graph.x_range.end = ts[ts.length - 1];"))


    solar_load_graph = load_styled_figure(
        title="Solar load",
        y_range=[0, 1500 *  LoadConfig.solar_panel_area.linked_column.cds_flow_column.initial_value[0]],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    solar_load_graph.line(x=SunIntensity.ts, y=SunIntensity.load, source=SunIntensity.source)

    SunIntensity.source.js_on_change("data", CustomJS(args={"solar_load_graph": solar_load_graph}, code=f"var ts = cb_obj.data.{SunIntensity.ts};solar_load_graph.x_range.start = ts[0]; solar_load_graph.x_range.end = ts[ts.length - 1];"))
    SunIntensity.source.js_on_change("data", CustomJS(args={"solar_load_graph": solar_load_graph, "load_config": LoadConfig.source}, code=f"var area = load_config.data.{LoadConfig.solar_panel_area}[0];solar_load_graph.y_range.end = area * 1500;"))


    return {"wind_graph": wind_graph, "solar_graph": solar_graph, "wind_load_graph": wind_load_graph, "solar_load_graph": solar_load_graph}
