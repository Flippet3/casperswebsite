import panel as pn

from src.dashboard.overview_base import OverviewBase, OverViewCategory


class Home2(OverviewBase):
    overview_category = OverViewCategory.Home

    @classmethod
    def app_content(cls, bootstrap):
        bootstrap.main.append(pn.Column(pn.widgets.TextInput(value="Test")))
        return bootstrap
