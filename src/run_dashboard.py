from platform import system

import panel as pn

from dashboard.overview_base import OverviewBase


def register_overviews():
    from dashboard.overviews.home import Home
    from dashboard.overviews.home2 import Home2
    from dashboard.overviews.howitsmade import HowItsMade
    from dashboard.overviews.resume import Resume

    Home.register()
    Home2.register()
    HowItsMade.register()
    Resume.register()

def run_dashboard():
    register_overviews()

    apps = {app_name: run_app_func for (app_name, run_app_func) in sum(OverviewBase.apps.values(), [])}
    apps[""] = apps["Resume"]

    if "windows" in system().lower():
        pn.serve(apps, port=80, threaded=True, websocket_origin="*", redirect="Home")
    else:
        pn.serve(apps, port=80, websocket_origin="*", redirect="Home")

    # if "windows" in system().lower():
    #     pn.serve(apps, port=5006, threaded=True, websocket_origin="*", index=get_base_folder() + "src/dashboard/index.html")
    # else:
    #     pn.serve(apps, port=5006, websocket_origin="*", index=get_base_folder() + "src/dashboard/index.html")

if __name__ == "__main__":
    run_dashboard()