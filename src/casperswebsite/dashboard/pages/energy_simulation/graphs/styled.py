from bokeh.plotting import figure as bokeh_figure
from bokeh.models.formatters import CustomJSTickFormatter
from functools import wraps

@wraps(bokeh_figure)
def styled_figure(*args, **kwargs):
    # Always set toolbar_location to None to remove the toolbar from its location
    kwargs['toolbar_location'] = None
    # Always set sizing_mode to "stretch_both"
    kwargs['sizing_mode'] = "stretch_both"

    fig = bokeh_figure(*args, **kwargs)
    fig.title.text_font_size = "0.5vw"
    fig.xaxis.axis_label_text_font_size = "0.5vw"
    fig.xaxis.major_label_text_font_size = "0.5vw"
    fig.xaxis.major_tick_line_width = 0.5
    fig.xaxis.minor_tick_line_width = 0.5
    fig.xaxis.axis_line_width = 0
    fig.yaxis.axis_label_text_font_size = "0.5vw"
    fig.yaxis.major_label_text_font_size = "0.5vw"
    fig.yaxis.major_tick_line_width = 0.5
    fig.yaxis.minor_tick_line_width = 0.5
    fig.yaxis.axis_line_width = 0
    fig.toolbar.tools = []


    # Set xaxis major label formatter to display dates, assuming x is in seconds, convert to ms
    fig.xaxis.formatter = CustomJSTickFormatter(code="""
        var dt = new Date(tick * 1000);
        var hh = String(dt.getHours()).padStart(2, '0');
        var mi = String(dt.getMinutes()).padStart(2, '0');
        return hh + ':' + mi;
    """)
    return fig

@wraps(styled_figure)
def load_styled_figure(*args, **kwargs):
    fig = styled_figure(*args, **kwargs)
    fig.yaxis.formatter = CustomJSTickFormatter(code="""
        if (tick < 1000) {
            return tick + " W";
        } else if (tick < 1000 * 1000) {
            var val = tick / 1000;
            var digits = Math.floor(Math.log10(Math.abs(val))) + 1;
            var decimals = Math.max(0, 3 - digits);
            var pow10 = Math.pow(10, decimals);
            var rounded = Math.round(val * pow10) / pow10;
            return rounded + " kW";
        } else {
            var val = tick / 1000000;
            var digits = Math.floor(Math.log10(Math.abs(val))) + 1;
            var decimals = Math.max(0, 3 - digits);
            var pow10 = Math.pow(10, decimals);
            var rounded = Math.round(val * pow10) / pow10;
            return rounded + " MW";
        }
   
    """)
    return fig
