import os

from bokeh_cdsflow import (
    CdsFlowBase,
    CdsFlowManager,
    CdsFlowStr,
    InputType,
)

_cds_callback_dir = os.path.join(os.path.dirname(__file__), "cds_callbacks")


START_DT = 365.25 * 24 * 3600 / 4 - 6 * 60 * 60


class TimeConfig(CdsFlowBase):
    dt: CdsFlowStr = "number", [900]
    max_ts: CdsFlowStr = "number", [100]
    input_type = InputType.SingleValue


class TimeSeries(CdsFlowBase):
    ts: CdsFlowStr = "number", [START_DT]
    input_type = InputType.Array
    depends_on_columns = []


class WindConfig(CdsFlowBase):
    A: CdsFlowStr = "number", [8]
    k: CdsFlowStr = "number", [2]
    min_bin: CdsFlowStr = "number", [0]
    max_bin: CdsFlowStr = "number", [30]
    nr_bins: CdsFlowStr = "number", [40]
    rated_ws: CdsFlowStr = "number", [11]
    input_type = InputType.SingleValue


class LoadConfig(CdsFlowBase):
    solar_panel_area: CdsFlowStr = "number", [100000]
    nr_5mw_tubrines: CdsFlowStr = "number", [100]
    input_type = InputType.SingleValue


class WeibullBins(CdsFlowBase):
    edges: CdsFlowStr = "number", []
    input_type = InputType.Array
    depends_on_columns = [WindConfig]


class WindData(CdsFlowBase):
    ts: CdsFlowStr = "number", [START_DT]
    target_bin: CdsFlowStr = "number", [5]
    speed: CdsFlowStr = "number", [5]
    load: CdsFlowStr = "number", [0]

    input_type = InputType.Array
    depends_on_columns = [WeibullBins, TimeSeries, LoadConfig.nr_5mw_tubrines, WindConfig.rated_ws]


class WindDistance(CdsFlowBase):
    wind_distance: CdsFlowStr = "number", [0]
    watermark: CdsFlowStr = "number", [0]

    input_type = InputType.SingleValue
    depends_on_columns = [WindData.speed, WindData.ts]


class GeoConfig(CdsFlowBase):
    latitude: CdsFlowStr = "number", [50]

    input_type = InputType.SingleValue


class SunIntensity(CdsFlowBase):
    ts: CdsFlowStr = "number", [START_DT]
    intensity: CdsFlowStr = "number", [0]
    zenith: CdsFlowStr = "number", [0]
    load: CdsFlowStr = "number", [0]

    input_type = InputType.Array
    depends_on_columns = [TimeSeries, GeoConfig.latitude, LoadConfig.solar_panel_area]


dataflow = CdsFlowManager(
    cds_flows=[
        cls.cds_flow
        for cls in globals().values()
        if isinstance(cls, type)
        and cls is not CdsFlowBase
        and issubclass(cls, CdsFlowBase)
        and getattr(cls, "cds_flow", None) is not None
    ],
    js_dir=_cds_callback_dir,
    tick_ms=33,
    engine_setup="""
        const canvas = document.getElementById('energy-canvas');
        const ctx = canvas.getContext('2d');
    """,
    engine_code=f"""
        var engine_ts = [...{TimeSeries.cds_flow.name}.data.{TimeSeries.ts}] 
        var last_val = engine_ts[engine_ts.length - 1];
        engine_ts.push(last_val + {TimeConfig.cds_flow.name}.data.{TimeConfig.dt}[0]);
        while (engine_ts.length > {TimeConfig.cds_flow.name}.data.{TimeConfig.max_ts}[0]) {{
            engine_ts.shift();
        }}
        {TimeSeries.cds_flow.name}.data = {{
            "ts": engine_ts
        }}
        drawGraphic(
            ctx, 
            {TimeSeries.cds_flow.name}.data.{TimeSeries.ts}[{TimeSeries.cds_flow.name}.data.{TimeSeries.ts}.length - 1], 
            {WindDistance.wind_distance.linked_column.js_input},
            {SunIntensity.cds_flow.name}.data.{SunIntensity.zenith}[{SunIntensity.cds_flow.name}.data.{SunIntensity.zenith}.length - 1], 
        );
    """,
)


if __name__ == "__main__":
    dataflow.update_signatures()
