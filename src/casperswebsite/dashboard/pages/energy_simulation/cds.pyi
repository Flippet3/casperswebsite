from typing import Any
from bokeh_cdsflow import SuperCDSDataflow, SuperCDSMeta
from bokeh_cdsflow import AnnotatedStr
from bokeh_cdsflow import InputType
from bokeh.models.sources import ColumnDataSource
from bokeh_cdsflow import SuperCDS

class TimeConfig(metaclass=SuperCDSMeta):
    dt: AnnotatedStr
    input_type: InputType
    max_ts: AnnotatedStr
    source: ColumnDataSource
    super_cds: SuperCDS
    input_type: InputType

class TimeSeries(metaclass=SuperCDSMeta):
    depends_on_columns: list
    input_type: InputType
    source: ColumnDataSource
    super_cds: SuperCDS
    ts: AnnotatedStr
    input_type: InputType
    depends_on_columns: list[Any]

class WindConfig(metaclass=SuperCDSMeta):
    A: AnnotatedStr
    input_type: InputType
    k: AnnotatedStr
    max_bin: AnnotatedStr
    min_bin: AnnotatedStr
    nr_bins: AnnotatedStr
    source: ColumnDataSource
    super_cds: SuperCDS
    input_type: InputType

class WeibullBins(metaclass=SuperCDSMeta):
    depends_on_columns: list
    edges: AnnotatedStr
    input_type: InputType
    source: ColumnDataSource
    super_cds: SuperCDS
    input_type: InputType
    depends_on_columns: list[Any]

class WindData(metaclass=SuperCDSMeta):
    depends_on_columns: list
    input_type: InputType
    source: ColumnDataSource
    speed: AnnotatedStr
    super_cds: SuperCDS
    target_bin: AnnotatedStr
    ts: AnnotatedStr
    input_type: InputType
    depends_on_columns: list[Any]

class WindDistance(metaclass=SuperCDSMeta):
    depends_on_columns: list
    input_type: InputType
    source: ColumnDataSource
    super_cds: SuperCDS
    watermark: AnnotatedStr
    wind_distance: AnnotatedStr
    input_type: InputType
    depends_on_columns: list[Any]

class GeoConfig(metaclass=SuperCDSMeta):
    input_type: InputType
    latitude: AnnotatedStr
    source: ColumnDataSource
    super_cds: SuperCDS
    input_type: InputType

class SunIntensity(metaclass=SuperCDSMeta):
    depends_on_columns: list
    input_type: InputType
    intensity: AnnotatedStr
    source: ColumnDataSource
    super_cds: SuperCDS
    ts: AnnotatedStr
    zenith: AnnotatedStr
    input_type: InputType
    depends_on_columns: list[Any]

dataflow: SuperCDSDataflow