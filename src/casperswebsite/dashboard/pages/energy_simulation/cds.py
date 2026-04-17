import os

from bokeh_cdsflow import (
    CdsFlowBase,
    CdsFlowManager,
    CdsFlowCol,
    InputType,
)

_cds_callback_dir = os.path.join(os.path.dirname(__file__), "cds_callbacks")


START_DT = 365.25 * 24 * 3600 / 4 - 6 * 60 * 60


class TimeConfig(CdsFlowBase):
    dt = CdsFlowCol("number", [900])
    max_ts = CdsFlowCol("number", [24 * 4 * 2])
    input_type = InputType.SingleValue


class TimeSeries(CdsFlowBase):
    ts = CdsFlowCol("number", [START_DT])
    input_type = InputType.Array


class WindConfig(CdsFlowBase):
    A = CdsFlowCol("number", [8])
    k = CdsFlowCol("number", [2])
    min_bin = CdsFlowCol("number", [0])
    max_bin = CdsFlowCol("number", [30])
    nr_bins = CdsFlowCol("number", [40])
    rated_ws = CdsFlowCol("number", [11])
    input_type = InputType.SingleValue


class LoadConfig(CdsFlowBase):
    solar_panel_area = CdsFlowCol("number", [100000])
    nr_5mw_tubrines = CdsFlowCol("number", [100])
    input_type = InputType.SingleValue


class WeibullBins(CdsFlowBase):
    edges = CdsFlowCol("number", [])
    input_type = InputType.Array


class WindData(CdsFlowBase):
    ts = CdsFlowCol("number", [START_DT])
    target_bin = CdsFlowCol("number", [5])
    speed = CdsFlowCol("number", [5])
    load = CdsFlowCol("number", [0])

    input_type = InputType.Array


class WindPlot(CdsFlowBase):
    t_today = CdsFlowCol("number", [START_DT])
    speed_today = CdsFlowCol("number", [5])
    load_today = CdsFlowCol("number", [0])
    t_yesterday = CdsFlowCol("number", [START_DT])
    speed_yesterday = CdsFlowCol("number", [5])
    load_yesterday = CdsFlowCol("number", [0])

    input_type = InputType.Array


class SunIntensity(CdsFlowBase):
    ts = CdsFlowCol("number", [START_DT])
    intensity = CdsFlowCol("number", [0])
    zenith = CdsFlowCol("number", [0])
    load = CdsFlowCol("number", [0])

    input_type = InputType.Array


# New: SunPlot class, like WindPlot, but for SunIntensity
class SunPlot(CdsFlowBase):
    t_today = CdsFlowCol("number", [START_DT])
    intensity_today = CdsFlowCol("number", [0])
    load_today = CdsFlowCol("number", [0])
    t_yesterday = CdsFlowCol("number", [START_DT])
    intensity_yesterday = CdsFlowCol("number", [0])
    load_yesterday = CdsFlowCol("number", [0])

    input_type = InputType.Array


class ColorConfig(CdsFlowBase):
    today_line_color = CdsFlowCol("string", ["#FF1744"])
    yesterday_line_color = CdsFlowCol("string", ["#B0B0B0"])
    input_type = InputType.SingleValue


class WindDistance(CdsFlowBase):
    wind_distance = CdsFlowCol("number", [0])
    watermark = CdsFlowCol("number", [0])

    input_type = InputType.SingleValue


class GeoConfig(CdsFlowBase):
    latitude = CdsFlowCol("number", [50])

    input_type = InputType.SingleValue


# New Pause config with just one boolean value
class Pause(CdsFlowBase):
    paused = CdsFlowCol("boolean", [False])
    input_type = InputType.SingleValue


time_config = TimeConfig()
time_series = TimeSeries()
wind_config = WindConfig()
load_config = LoadConfig()
geo_config = GeoConfig()
color_config = ColorConfig()
pause = Pause()

weibull_bins = WeibullBins(depends=[wind_config])
wind_data = WindData(depends=[weibull_bins, time_series, load_config.nr_5mw_tubrines, wind_config.rated_ws])
wind_plot = WindPlot(depends=[wind_data.ts, wind_data.speed, wind_data.load])
wind_distance = WindDistance(depends=[wind_data.speed, wind_data.ts])
sun_intensity = SunIntensity(depends=[time_series, geo_config.latitude, load_config.solar_panel_area])
sun_plot = SunPlot(depends=[sun_intensity.ts, sun_intensity.intensity, sun_intensity.load])


dataflow = CdsFlowManager(
    cds_flows=[
        time_config,
        time_series,
        wind_config,
        load_config,
        geo_config,
        color_config,
        pause,
        weibull_bins,
        wind_data,
        wind_plot,
        wind_distance,
        sun_intensity,
        sun_plot,
    ],
    js_dir=_cds_callback_dir,
    tick_ms=33,
    engine_setup="""
        const canvas = document.getElementById('energy-canvas');
        const ctx = canvas.getContext('2d');
    """,
    engine_code=f"""
        if (!{pause.paused.js_input}) {{
            var engine_ts = {time_series.ts.js_input} 
            var last_val = engine_ts[engine_ts.length - 1];
            engine_ts.push(last_val + {time_config.dt.js_input});
            while (engine_ts.length > {time_config.max_ts.js_input}) {{
                engine_ts.shift();
            }}
            {time_series.set_value_str({time_series.ts: "engine_ts"})}
        drawGraphic(
            ctx, 
            {time_series.ts.js_data_accessor}[{time_series.ts.js_data_accessor}.length - 1], 
            {wind_distance.wind_distance.js_input},
            {sun_intensity.zenith.js_data_accessor}[{sun_intensity.zenith.js_data_accessor}.length - 1], 
            {load_config.nr_5mw_tubrines.js_input}, 
            {load_config.solar_panel_area.js_input}, 
        );
        }}
   
    """,
)


if __name__ == "__main__":
    dataflow.update_signatures()
