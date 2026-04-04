from platform import system

import panel as pn

from casperswebsite.dashboard.overview_base import OverviewBase
from casperswebsite.general_tools import IS_LOCAL, get_module_folder


def register_overviews():
    from casperswebsite.dashboard.overviews.home import Home
    from casperswebsite.dashboard.overviews.howitsmade import HowItsMade
    from casperswebsite.dashboard.overviews.resume import Resume
    from casperswebsite.dashboard.overviews.authors_page import AuthorsPage
    from casperswebsite.dashboard.overviews.storyguide import StoryGuide
    from casperswebsite.dashboard.overviews.shirt import Shirt

    Home.register()
    HowItsMade.register()
    Resume.register()
    AuthorsPage.register()
    StoryGuide.register()
    Shirt.register()

def run_dashboard():
    register_overviews()

    apps = {**{
        app_name: run_app_func for (app_name, run_app_func) in sum(OverviewBase.apps.values(), [])
    }, **{
        app_name.lower(): run_app_func for (app_name, run_app_func) in sum(OverviewBase.apps.values(), [])
    }}
    if IS_LOCAL:
        apps[""] = apps["Shirt"]  # Set initial site.
    else:
        apps[""] = apps["Home"]  # Set initial site.

    # Manage favicon
    server_kwargs = dict(
        port=5006,
        websocket_origin="*",
        static_dirs={"assets": f"{get_module_folder()}/static"},
        favicon="assets/favicon.ico",
        title="Casper's website"
    )

    if "windows" in system().lower():
        pn.serve(apps, threaded=True, **server_kwargs)
    else:
        pn.serve(apps, **server_kwargs)

if __name__ == "__main__":
    run_dashboard()