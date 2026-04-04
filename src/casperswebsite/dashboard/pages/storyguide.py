import yaml

from bokeh.models import Button, Div, CustomJS
from bokeh.layouts import column
from bokeh.embed import components

from casperswebsite.dashbuilder.contract import (
    CardInfo,
    ContainerInfo,
    EmbedType,
    OverViewCategory,
    PageInfo,
)
from casperswebsite.general_tools import get_module_folder

with open(get_module_folder() + "static/writing_options.yaml", "r") as o:
    OPTIONS = yaml.load(o, Loader=yaml.SafeLoader)

def _story_guide_bokeh_component():
    # This builds a Bokeh layout replicating the prompt generator
    # We'll expose the options and a button that, when clicked, will randomize and output the story guide to a Div

    # Precompute options for JS
    options_js = "{%s}" % (
        ", ".join(f"'{k}': {OPTIONS[k]!r}" for k in OPTIONS)
    )

    initial_text = "Click 'Generate story guide' to create a prompt."

    div = Div(text=initial_text, css_classes=["story-guide-output"])
    button = Button(label="Generate story guide", button_type="primary", width=240)

    # CustomJS to randomize
    button.js_on_click(CustomJS(args=dict(div=div), code=f"""
        // Parse the options dict
        const options = {options_js};
        function pick(arr) {{
            return arr[Math.floor(Math.random() * arr.length)];
        }}
        let response = "";
        for (const key in options) {{
            response += key + ": " + pick(options[key]) + "<br>";
        }}
        response += "Event: <br>";
        response += "Before event: <br>";
        response += "After event: ";
        div.text = `<p>${{response}}</p>`;
    """))

    layout = column(button, div, sizing_mode="stretch_width")
    return components(layout)

class StoryGuidePage:
    def build_page(self) -> PageInfo:
        bokeh_script, bokeh_div = _story_guide_bokeh_component()
        return PageInfo(
            category=OverViewCategory.Tools,
            title="Story Generator",
            header_html=bokeh_script,
            cards=[
                CardInfo(
                    title="Story generator",
                    containers=[
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Text,
                            content="This is effectively a writing prompt generator that simply picks from a few options for goal, setting, emotion, and arc (following the Save The Cat arc structures)."
                        ),
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Html,
                            content=bokeh_div,
                        )
                    ]
                )
            ]
        )
