import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate


class Home(OverviewBase):
    overview_category = OverViewCategory.Home

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        bootstrap.add_card("Intro")
        bootstrap.add_container(6)
        bootstrap.add_text("Hello -- welcome to my website! My name is Casper and I'm a Dutch guy living in Denmark. For those interested in how I made this website, check out the 'how it's made' page. For those interested in why I made this website, I can't help you -- it just kind of happened.")
        bootstrap.add_container(6)
        bootstrap.add_image("https://s7.gifyu.com/images/SGR3S.gif")
        return bootstrap
