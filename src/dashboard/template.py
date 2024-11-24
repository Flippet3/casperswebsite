import panel as pn

from src.general_tools.general_tools import get_base_folder

# Initialize Panel Extension
pn.extension()

# Read the template file
with open(get_base_folder() + "dashboard\\index.html", 'r') as file:
    template_str = file.read()

class CustomTemplate(pn.Template):
    def add_card(self, title: str):
        pass


def get_custom_template():
    custom_template = pn.Template
    return CustomTemplate(template_str)

# class CustomTemplate(pn.template.BaseTemplate):
#     _template =
