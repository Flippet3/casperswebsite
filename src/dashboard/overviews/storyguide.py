import os
from random import choice

import yaml

import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate


with open(os.getcwd().split("casperswebsite")[0] + r"casperswebsite\src\static\writing_options.yaml", "r") as o:
    OPTIONS = yaml.load(o, Loader=yaml.SafeLoader)


class StoryGuide(OverviewBase):
    overview_category = OverViewCategory.Tools

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        def pick_story_guide(event):
            response = ""
            for key in OPTIONS:
                response += f"{key}: {choice(OPTIONS[key])}\n"
            response += "Event: \n"
            response += "Before event: \n"
            response += "After event: "
            html.value = response.replace("\n", "<br>")

        button = pn.widgets.Button(name="Generate story guide", button_type="primary")
        button.on_click(pick_story_guide)

        html = pn.widgets.StaticText()
        bootstrap.add_card("Story generator")
        bootstrap.add_container(10)
        bootstrap.add_panel_component(html)
        bootstrap.add_container(2)
        bootstrap.add_panel_component(button)
        return bootstrap
