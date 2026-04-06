from typing import Any
from casperswebsite.bokeh_dataflows import SuperCDSDataflow, SuperCDSMeta
from casperswebsite.bokeh_dataflows import AnnotatedStr
from casperswebsite.bokeh_dataflows import InputType
from bokeh.models.sources import ColumnDataSource
from casperswebsite.bokeh_dataflows import SuperCDS

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
    input_type: InputType
    mean: AnnotatedStr
    phi: AnnotatedStr
    seasonal_period: AnnotatedStr
    sigma: AnnotatedStr
    source: ColumnDataSource
    super_cds: SuperCDS
    input_type: InputType

class WindData(metaclass=SuperCDSMeta):
    depends_on_columns: list
    input_type: InputType
    source: ColumnDataSource
    speed: AnnotatedStr
    super_cds: SuperCDS
    ts: AnnotatedStr
    z: AnnotatedStr
    input_type: InputType
    depends_on_columns: list[Any]

dataflow: SuperCDSDataflow