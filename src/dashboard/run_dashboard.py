from platform import system

import panel as pn

from src.dashboard.overview_base import OverviewBase


def register_overviews():
    from src.dashboard.overviews.home import Home
    from src.dashboard.overviews.home2 import Home2

    Home.register()
    Home2.register()

def run_dashboard():
    register_overviews()

    apps = {app_name: run_app_func for (app_name, run_app_func) in sum(OverviewBase.apps.values(), [])}

    if "windows" in system().lower():
        pn.serve(apps, port=5006, threaded=True, websocket_origin="*")
    else:
        pn.serve(apps, port=5006, websocket_origin="*")

    # if "windows" in system().lower():
    #     pn.serve(apps, port=5006, threaded=True, websocket_origin="*", index=get_base_folder() + "src/dashboard/index.html")
    # else:
    #     pn.serve(apps, port=5006, websocket_origin="*", index=get_base_folder() + "src/dashboard/index.html")

if __name__ == "__main__":
    run_dashboard()