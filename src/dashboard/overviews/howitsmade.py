import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate


class HowItsMade(OverviewBase):
    overview_category = OverViewCategory.HowItsMade

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        bootstrap.add_card("How it's made")
        bootstrap.add_container(12)
        bootstrap.add_text("Magic.")
        bootstrap.add_card("How it's really made")
        bootstrap.add_container(12)
        bootstrap.add_text("""This website is built dynamically using Jinja2 and python.
         It is hosted on a small droplet (digital ocean) and uses Holoviz Panel to configure any interactive widgets.
         I've set-up a pipeline using Github Actions to automatically update this whenever I make a change to the repo.
         Oh yeah, the repo is public, and can be found <a href='https://github.com/Flippet3/casperswebsite'>here</a> if you'd like to take a look for yourself!""")
        return bootstrap
