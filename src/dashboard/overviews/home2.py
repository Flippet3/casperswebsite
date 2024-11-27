import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory


class Home2(OverviewBase):
    overview_category = OverViewCategory.Home

    @classmethod
    def app_content(cls, bootstrap):
        bootstrap.add_card("Intro")
        bootstrap.add_container(12)
        bootstrap.add_text(
            "Hello -- welcome to my website! My name is Casper and I'm a Dutch guy living in Denmark. For those interested in how I made this, check out the 'how it's made' page. For those interested in why I made this, I can't help you. It just kind of happened.")
        return bootstrap
