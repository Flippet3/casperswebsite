from bokeh.plotting import figure as bokeh_figure
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

    from bokeh.models.formatters import CustomJSTickFormatter

    # Set xaxis major label formatter to display dates, assuming x is in seconds, convert to ms
    fig.xaxis.formatter = CustomJSTickFormatter(code="""
        var dt = new Date(tick * 1000);
        var hh = String(dt.getHours()).padStart(2, '0');
        var mi = String(dt.getMinutes()).padStart(2, '0');
        return hh + ':' + mi;
    """)


    
    return fig