from platform import system

import panel as pn

from dashboard.overview_base import OverviewBase


def register_overviews():
    from dashboard.overviews.home import Home
    from dashboard.overviews.howitsmade import HowItsMade
    from dashboard.overviews.resume import Resume

    Home.register()
    HowItsMade.register()
    Resume.register()

def run_dashboard():
    register_overviews()

    apps = {app_name: run_app_func for (app_name, run_app_func) in sum(OverviewBase.apps.values(), [])}
    apps[""] = apps["Resume"]  # Set initial site.

    if "windows" in system().lower():
        pn.serve(apps, port=5006, threaded=True, websocket_origin="*", redirect="Home")
    else:
        pn.serve(apps, port=5006, websocket_origin="*", redirect="Home")

if __name__ == "__main__":
    run_dashboard()