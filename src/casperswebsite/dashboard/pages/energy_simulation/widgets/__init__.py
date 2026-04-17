import math
from bokeh.models.dom import DOMElement
from bokeh.models import CustomJS, Slider, Button
from bokeh.models.formatters import CustomJSTickFormatter

from casperswebsite.dashboard.pages.energy_simulation.cds import load_config, pause


def get_widgets() -> dict[str, DOMElement]:
    solar_panel_area_slider = Slider(
        title="Solar panel area (m^2)",
        start=0,
        end=6,
        value=math.log10(load_config.solar_panel_area.initial_value[0]),
        step=0.1,
        format=CustomJSTickFormatter(code="return Math.round(Math.pow(10, tick));"),
    )
    solar_panel_area_slider.js_on_change(
        "value",
        CustomJS(
            args={load_config.name: load_config.source},
            code=f"""{load_config.set_value_str({load_config.solar_panel_area: "[Math.pow(10, cb_obj.value)]"})}""",
        ),
    )

    nr_wind_turbines_slider = Slider(
        title="Nr wind Turbines (5MW)", start=0, end=3, value=math.log10(load_config.nr_5mw_tubrines.initial_value[0]), step=0.1, format=CustomJSTickFormatter(code="return Math.round(Math.pow(10, tick));")
    )
    nr_wind_turbines_slider.js_on_change(
        "value",
        CustomJS(
            args={load_config.name: load_config.source},
            code=f"""{load_config.set_value_str({load_config.nr_5mw_tubrines: "[Math.pow(10, cb_obj.value)]"})}""",
        ),
    )

    pause_button = Button(label="Pause", button_type="primary")
    pause_button.js_on_click(
        CustomJS(
            args={pause.name: pause.source},
            code=f"""{pause.set_value_str({pause.paused: "[!" + pause.paused.js_input + "]"})}""",
       
        ),
    )

    return {
        "solar_panel_area_slider": solar_panel_area_slider,
        "nr_wind_turbines_slider": nr_wind_turbines_slider,
        "pause_button": pause_button,
    }
