import os
from typing import Literal

from casperswebsite.bokeh_dataflows import (
    InputType,
    SuperCDSDataflow,
    SuperCDSMeta,
)

_cds_callback_dir = os.path.join(os.path.dirname(__file__), "cds_callbacks")


class TimeConfig(metaclass=SuperCDSMeta):
    __cds_name__ = "time_config"

    dt: Literal["number"] = [900]
    max_ts: Literal["number"] = [100]
    input_type = InputType.SingleValue


class TimeSeries(metaclass=SuperCDSMeta):
    ts: Literal["number"] = [0]
    input_type = InputType.Array
    depends_on_columns = []

class WindConfig(metaclass=SuperCDSMeta):
    mean: Literal["number"] = [15]
    phi: Literal["number"] = [0.95]
    sigma: Literal["number"] = [0.25]
    seasonal_period: Literal["number"] = [60*60*24*365]
    input_type = InputType.SingleValue

class WindData(metaclass=SuperCDSMeta):
    ts: Literal["number"] = [0]
    speed: Literal["number"] = [5]
    z: Literal["number"] = [0]

    input_type = InputType.Array
    depends_on_columns = [WindConfig, TimeSeries]


dataflow = SuperCDSDataflow(
    super_cdss=[
        cls.super_cds
        for cls in globals().values()
        if isinstance(cls, type) and hasattr(cls, "super_cds")
    ],
    js_dir=_cds_callback_dir,
    tick_ms=33,
    engine_code=f"""
        var engine_ts = [...{TimeSeries.super_cds.name}.data.{TimeSeries.ts}] 
        var last_val = engine_ts[engine_ts.length - 1];
        engine_ts.push(last_val + {TimeConfig.super_cds.name}.data.{TimeConfig.dt}[0]);
        while (engine_ts.length > {TimeConfig.super_cds.name}.data.{TimeConfig.max_ts}[0]) {{
            engine_ts.shift();
        }}
        {TimeSeries.super_cds.name}.data = {{
            "ts": engine_ts
        }}
    """,
)

if __name__ == "__main__":
    dataflow.update_signatures()
    import inspect

    def write_stub():
        stub_path = os.path.join(os.path.dirname(__file__), "cds.pyi")
        imports = [
            "from typing import Any",
            "from casperswebsite.bokeh_dataflows import SuperCDSDataflow, SuperCDSMeta",
        ]
        lines = [
            "",
        ]

        current_globals = globals()
        for name, obj in current_globals.items():
            if inspect.isclass(obj) and getattr(obj, "__class__", None) is not None:
                if getattr(obj, "__class__", None).__name__ == "SuperCDSMeta":
                    lines.append(f"class {name}(metaclass=SuperCDSMeta):")
                    for field_name in dir(obj):
                        if field_name.startswith("_"):
                            continue
                        attr = getattr(obj, field_name)
                        # Add the type line with just the type (not as a string), and ensure import
                        attr_type = type(attr)
                        type_module = attr_type.__module__
                        type_name = attr_type.__name__
                        if type_module == "builtins":
                            import_line = None
                        else:
                            import_line = f"from {type_module} import {type_name}"
                            if import_line not in imports:
                                imports.append(import_line)
                        lines.append(f"    {field_name}: {type_name}")

                    # Add extra class attributes if present
                    if hasattr(obj, "input_type"):
                        lines.append("    input_type: InputType")
                    if hasattr(obj, "depends_on_columns"):
                        lines.append("    depends_on_columns: list[Any]")
                    lines.append("")
        lines.append("dataflow: SuperCDSDataflow")
        print(stub_path)
        with open(stub_path, "w") as f:
            f.write("\n".join(imports + lines))

    write_stub()
