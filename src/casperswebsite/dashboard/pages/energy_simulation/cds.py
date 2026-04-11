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
    dt: CdsFlowStr = "number", [900]  # type: ignore[assignment]
    max_ts: CdsFlowStr = "number", [100]  # type: ignore[assignment]
    input_type = InputType.SingleValue


class TimeSeries(CdsFlowBase):
    ts: CdsFlowStr = "number", [START_DT]  # type: ignore[assignment]
    input_type = InputType.Array
    depends_on_columns = []


class WindConfig(CdsFlowBase):
    A: CdsFlowStr = "number", [7]  # type: ignore[assignment]
    k: CdsFlowStr = "number", [2]  # type: ignore[assignment]
    min_bin: CdsFlowStr = "number", [0]  # type: ignore[assignment]
    max_bin: CdsFlowStr = "number", [30]  # type: ignore[assignment]
    nr_bins: CdsFlowStr = "number", [40]  # type: ignore[assignment]
    input_type = InputType.SingleValue


class WeibullBins(CdsFlowBase):
    edges: CdsFlowStr = "number", []  # type: ignore[assignment]
    input_type = InputType.Array
    depends_on_columns = [WindConfig]


class WindData(CdsFlowBase):
    ts: CdsFlowStr = "number", [START_DT]  # type: ignore[assignment]
    target_bin: CdsFlowStr = "number", [5]  # type: ignore[assignment]
    speed: CdsFlowStr = "number", [5]  # type: ignore[assignment]

    input_type = InputType.Array
    depends_on_columns = [WeibullBins, TimeSeries]


class WindDistance(CdsFlowBase):
    wind_distance: CdsFlowStr = "number", [0]  # type: ignore[assignment]
    watermark: CdsFlowStr = "number", [0]  # type: ignore[assignment]

    input_type = InputType.SingleValue
    depends_on_columns = [WindData.speed, WindData.ts]


class GeoConfig(CdsFlowBase):
    latitude: CdsFlowStr = "number", [50]  # type: ignore[assignment]

    input_type = InputType.SingleValue


class SunIntensity(CdsFlowBase):
    ts: CdsFlowStr = "number", [START_DT]  # type: ignore[assignment]
    intensity: CdsFlowStr = "number", [0]  # type: ignore[assignment]
    zenith: CdsFlowStr = "number", [0]  # type: ignore[assignment]

    input_type = InputType.Array
    depends_on_columns = [TimeSeries, GeoConfig.latitude]


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
