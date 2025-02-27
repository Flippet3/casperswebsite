from platform import system

import panel as pn

from dashboard.overview_base import OverviewBase
from general_tools.general_tools import IS_LOCAL


def register_overviews():
    from dashboard.overviews.home import Home
    from dashboard.overviews.howitsmade import HowItsMade
    from dashboard.overviews.resume import Resume
    from dashboard.overviews.authors_page import AuthorsPage
    from dashboard.overviews.storyguide import StoryGuide
    from dashboard.overviews.shirt import Shirt

    Home.register()
    HowItsMade.register()
    Resume.register()
    AuthorsPage.register()
    StoryGuide.register()
    Shirt.register()

def run_dashboard():
    register_overviews()

    apps = {app_name: run_app_func for (app_name, run_app_func) in sum(OverviewBase.apps.values(), [])}
    if IS_LOCAL:
        apps[""] = apps["Shirt"]  # Set initial site.
    else:
        apps[""] = apps["Home"]  # Set initial site.

    # Manage favicon
    server_kwargs = dict(
        port=5006,
        websocket_origin="*",
        static_dirs={"assets": "./static"},
        favicon="assets/favicon.ico",
        title="Casper's website"
    )

    if "windows" in system().lower():
        pn.serve(apps, threaded=True, **server_kwargs)
    else:
        pn.serve(apps, **server_kwargs)

if __name__ == "__main__":
    run_dashboard()