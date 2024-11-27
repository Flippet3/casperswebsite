import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate


class HowItsMade(OverviewBase):
    overview_category = OverViewCategory.HowItsMade

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        bootstrap.add_card("How it's made")
        bootstrap.add_container(8)
        bootstrap.add_text("Magic.")
        return bootstrap
