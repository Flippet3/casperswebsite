import os

from casperswebsite.bokeh_dataflows import InputType, SuperCDS, SuperCDSColumn, SuperCDSDataflow


cds_callback_dir = os.path.join(os.path.dirname(__file__), "cds_callbacks")


time_config = SuperCDS(
    "time_config",
    [
        SuperCDSColumn(name="start_ts", js_type="number", input_type=InputType.SingleValue, initial_value=[0]),
        SuperCDSColumn(name="dt", js_type="number", input_type=InputType.SingleValue, initial_value=[1]),
        SuperCDSColumn(name="max_ts", js_type="number", input_type=InputType.SingleValue, initial_value=[100]),
    ],
)

time_series = SuperCDS("time_series", [SuperCDSColumn(name="ts", js_type="number")], depends_on_columns=list(time_config.columns.values()))

dataflow = SuperCDSDataflow(super_cdss=[time_config, time_series], js_dir=cds_callback_dir)

if __name__ == "__main__":
    # dataflow.clear_js_files()
    # dataflow.update_signatures()
    dataflow.propegate_loop()
