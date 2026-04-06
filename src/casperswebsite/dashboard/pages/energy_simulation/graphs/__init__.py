from bokeh.models.dom import DOMElement
from casperswebsite.bokeh_dataflows import SuperCDSDataflow


class AnnotatedStr(str):
    def __new__(cls, value, extra_info):
        obj = str.__new__(cls, value)
        obj.extra_info = extra_info
        return obj


def get_plots(dataflows: SuperCDSDataflow) -> dict[str, DOMElement]:
    from bokeh.plotting import figure

    ts_source = dataflows.super_cdss["time_series"]

    p = figure(
        title="Line at height 5",
        sizing_mode="stretch_both",
        toolbar_location=None,
    )
    p.toolbar.tools = []
    p.line(x=AnnotatedStr("ts", 12355), y="ts", source=ts_source.source)

    return {"dummy_fig": p}