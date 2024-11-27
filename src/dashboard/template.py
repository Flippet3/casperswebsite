import uuid

import panel as pn

from general_tools.general_tools import get_base_folder

# Initialize Panel Extension
pn.extension()

# Read the template file
with open(get_base_folder() + "dashboard/index.html", 'r') as file:
    template_str = file.read()


class CustomTemplate(pn.template.Template):

    def __init__(self, template, *args, **kwargs):
        super().__init__(template, *args, **kwargs)
        self.cards = []
        self.components = {}
        self.current_card = None
        self.current_container = None

    def add_card(self, title: str, skills=None):
        self.current_container = None
        self.current_card = {
            "title": title,
            "containers": [],
            "skills": skills or []
        }
        self.cards.append(self.current_card)

    def add_container(self, width: int):
        assert self.current_card, "first add a card before adding a container"
        assert 0 < width < 13, "width should be between 1 and 12"
        self.current_container = {
            "width": width,
            "content": []
        }
        self.current_card["containers"].append(self.current_container)

    def add_text(self, text: str):
        assert self.current_container, "First add a container before adding content"
        self.current_container["content"].append({
            "content_type": "text",
            "value": text
        })

    def add_image(self, image_path: str):
        assert self.current_container, "First add a container before adding content"
        self.current_container["content"].append({
            "content_type": "image",
            "value": image_path
        })

    def add_panel_component(self, component):
        assert self.current_container, "First add a container before adding content"
        component_id = str(uuid.uuid4())
        self.components[component_id] = component
        self.current_container["content"].append({
            "content_type": "panel_component",
            "component_id": component_id
        })

    def resolve_cards(self):
        self.add_variable("cards", self.cards)
        for component_id, component in self.components.items():
            self.add_panel(component_id, component)


def get_custom_template():
    return CustomTemplate(template_str)

