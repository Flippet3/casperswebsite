"""Run: python this_file.py — then open the printed URL and click the button."""

from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Button, ColumnDataSource, CustomJS

source = ColumnDataSource(data={"x": [[1,2,3], [1,2,3]], "y": [[2,3,4], [4,5,6]]})

source.js_on_change(
    "data",
    CustomJS(
        code="""
        console.log("LISTENER: data (js_on_change)");
        """
    ),
)

button = Button(label="Patch data")
button.js_on_click(
    CustomJS(
        args=dict(source=source),
        code="""
        console.log("BUTTON: before source.data = ...");
        source.data = { x: [[99, 99, 99], [99, 99, 99]], y: [..source.data.y] };
        console.log("BUTTON: after source.data = ...");
        """,
    )
)

show(column(button))