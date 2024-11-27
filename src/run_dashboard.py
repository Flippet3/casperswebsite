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

    # Manage favicon
    server_kwargs = dict(
        port=5006,
        websocket_origin="*",
        static_dirs={"assets": "./static"},
        favicon="assets/favicon.ico"
    )

    if "windows" in system().lower():
        pn.serve(apps, threaded=True, **server_kwargs)
    else:
        pn.serve(apps, **server_kwargs)

if __name__ == "__main__":
    run_dashboard()