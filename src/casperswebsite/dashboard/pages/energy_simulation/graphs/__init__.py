from bokeh.models import CustomJS
from bokeh.models.dom import DOMElement

from casperswebsite.dashboard.pages.energy_simulation.cds import WindData


def get_plots() -> dict[str, DOMElement]:
    from bokeh.plotting import figure

    p = figure(
        title="Wind speed",
        sizing_mode="stretch_both",
        toolbar_location=None,
        y_range=[0, 25],
        x_range=[0, 900],
        background_fill_alpha=0.2,
        border_fill_alpha=0
    )
    p.toolbar.tools = []
    p.line(x=WindData.ts, y=WindData.speed, source=WindData.source)

    WindData.source.js_on_change("data", CustomJS(args={"p": p}, code=f"var ts = cb_obj.data.{WindData.ts};p.x_range.start = ts[0]; p.x_range.end = ts[ts.length - 1];"))

    return {"dummy_fig": p}
