from bokeh.models import CustomJS
from bokeh.models.dom import DOMElement

from casperswebsite.dashboard.pages.energy_simulation.cds import load_config, sun_intensity, wind_data
from casperswebsite.dashboard.pages.energy_simulation.graphs.styled import load_styled_figure, styled_figure


def get_plots() -> dict[str, DOMElement]:

    wind_graph = styled_figure(
        title="Wind speed",
        y_range=[0, 25],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0,
    )
    wind_graph.line(x=wind_data.ts.name, y=wind_data.speed.name, source=wind_data.source)

    wind_data.source.js_on_change("data", CustomJS(args={"wind_graph": wind_graph}, code=f"var ts = cb_obj.data.{wind_data.ts.name};wind_graph.x_range.start = ts[0]; wind_graph.x_range.end = ts[ts.length - 1];"))

    wind_load_graph = load_styled_figure(
        title="Wind load",
        y_range=[0, 5500000 * load_config.nr_5mw_tubrines.initial_value[0]],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    wind_load_graph.line(x=wind_data.ts.name, y=wind_data.load.name, source=wind_data.source)

    wind_data.source.js_on_change("data", CustomJS(args={"wind_load_graph": wind_load_graph}, code=f"var ts = cb_obj.data.{wind_data.ts.name};wind_load_graph.x_range.start = ts[0]; wind_load_graph.x_range.end = ts[ts.length - 1];"))
    wind_data.source.js_on_change("data", CustomJS(args={"wind_load_graph": wind_load_graph, "load_config": load_config.source}, code=f"var nr_turbines = load_config.data.{load_config.nr_5mw_tubrines.name}[0];wind_load_graph.y_range.end = nr_turbines * 5500000;"))

    solar_graph = styled_figure(
        title="Solar irradiance",
        y_range=[0, 1500],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    solar_graph.line(x=sun_intensity.ts.name, y=sun_intensity.intensity.name, source=sun_intensity.source)

    sun_intensity.source.js_on_change("data", CustomJS(args={"solar_graph": solar_graph}, code=f"var ts = cb_obj.data.{sun_intensity.ts.name};solar_graph.x_range.start = ts[0]; solar_graph.x_range.end = ts[ts.length - 1];"))


    solar_load_graph = load_styled_figure(
        title="Solar load",
        y_range=[0, 1500 * load_config.solar_panel_area.initial_value[0]],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    solar_load_graph.line(x=sun_intensity.ts.name, y=sun_intensity.load.name, source=sun_intensity.source)

    sun_intensity.source.js_on_change("data", CustomJS(args={"solar_load_graph": solar_load_graph}, code=f"var ts = cb_obj.data.{sun_intensity.ts.name};solar_load_graph.x_range.start = ts[0]; solar_load_graph.x_range.end = ts[ts.length - 1];"))
    sun_intensity.source.js_on_change("data", CustomJS(args={"solar_load_graph": solar_load_graph, "load_config": load_config.source}, code=f"var area = load_config.data.{load_config.solar_panel_area.name}[0];solar_load_graph.y_range.end = area * 1500;"))


    return {"wind_graph": wind_graph, "solar_graph": solar_graph, "wind_load_graph": wind_load_graph, "solar_load_graph": solar_load_graph}
