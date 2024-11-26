import panel as pn

from src.dashboard.overview_base import OverviewBase, OverViewCategory
from src.dashboard.template import CustomTemplate


class Resume(OverviewBase):
    overview_category = OverViewCategory.CV

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:

        bootstrap.add_card("Education")
        bootstrap.add_container(6)
        bootstrap.add_text("meat")
        bootstrap.add_container(1)
        bootstrap.add_text("note")
        bootstrap.add_container(1)
        bootstrap.add_text("note")

        bootstrap.add_container(6)
        bootstrap.add_text("meat")
        bootstrap.add_container(1)
        bootstrap.add_text("note")
        bootstrap.add_container(1)
        bootstrap.add_text("note")

        bootstrap.add_container(6)
        bootstrap.add_text("meat")
        bootstrap.add_container(1)
        bootstrap.add_text("note")
        bootstrap.add_container(1)
        bootstrap.add_text("note")
        return bootstrap
