import math
from bokeh.models.dom import DOMElement
from bokeh.models import CustomJS, Slider
from bokeh.models.formatters import CustomJSTickFormatter

from casperswebsite.dashboard.pages.energy_simulation.cds import LoadConfig


def get_widgets() -> dict[str, DOMElement]:
    solar_panel_area_slider = Slider(
        title="Solar panel area (m^2)",
        start=0,
        end=6,
        value=math.log10(LoadConfig.solar_panel_area.linked_column.cds_flow_column.initial_value[0]),
        step=0.1,
        format=CustomJSTickFormatter(code="return Math.round(Math.pow(10, tick));"),
    )
    solar_panel_area_slider.js_on_change(
        "value",
        CustomJS(
            args={LoadConfig.cds_flow.name: LoadConfig.source},
            code=f"""{LoadConfig.set_value_str({LoadConfig.solar_panel_area: "[Math.pow(10, cb_obj.value)]"})}""",
        ),
    )

    nr_wind_turbines_slider = Slider(
        title="Nr wind Turbines (5MW)", start=0, end=3, value=math.log10(LoadConfig.nr_5mw_tubrines.linked_column.cds_flow_column.initial_value[0]), step=0.1, format=CustomJSTickFormatter(code="return Math.round(Math.pow(10, tick));")
    )
    nr_wind_turbines_slider.js_on_change(
        "value",
        CustomJS(
            args={LoadConfig.cds_flow.name: LoadConfig.source},
            code=f"""{LoadConfig.set_value_str({LoadConfig.nr_5mw_tubrines: "[Math.pow(10, cb_obj.value)]"})}""",
        ),
    )

    return {"solar_panel_area_slider": solar_panel_area_slider, "nr_wind_turbines_slider": nr_wind_turbines_slider}
