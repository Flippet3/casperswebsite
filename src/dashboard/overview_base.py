import json
import threading
import logging
from abc import ABC, abstractmethod
from collections import defaultdict

import panel as pn
from panel.template import BootstrapTemplate

from src.general_tools.general_tools import IS_LOCAL, classproperty
from src.data.shared_cache import SharedCache

class OverViewCategory:
    Home = "Home"
    CV = "CV"

class OverviewBase(ABC):
    _apps = defaultdict(list)
    deeplink_content = {}

    @classproperty
    def logger(cls):
        logging.getLogger("website")

    @classproperty
    def app_name(cls):
        return "".join(sum(([char] if char.islower() else ["_" + char] for char in cls.__name__), []))[1:]

    @property
    @abstractmethod
    def overview_category(self):
        pass

    @classproperty
    def apps(cls):
        return cls._apps

    @classmethod
    def run_app(cls):
        bootstrap = pn.template.bootstrap.BootstrapTemplate(title=cls.app_name)
        bootstrap.sidebar_width = 230

        # cls.deeplink_content = {k: json.loads(v[0].decode()) for (k, v) in pn.state.session_args.items()}
        # deep_link_button = pn.widgets.Button(name="deeplink", button_type="primary", sizing_mode="stretch_width")
        # bootstrap.sidebar.append(deep_link_button)

        def add_app_button(app_name):
            btn = pn.widgets.Button(name=app_name.replace("_", " "), button_type="primary", sizing_mode="stretch_width")
            btn.js_on_click(
                code=f"window.open('//' + location.host + location.pathname.split('/').slice(0, -1).join() + '/{app_name}', '_self');"
            )
            bootstrap.sidebar.append(btn)

        for overview_category, overview_category_overviews in cls.apps.items():
            if overview_category != OverViewCategory.Home:
                bootstrap.sidebar.append(pn.pane.Str(overview_category, css_classes=["custon-str-pane"], height=80))
            for overview_category_overview in overview_category_overviews:
                add_app_button(overview_category_overview[0])

        bootstrap = cls.app_content(bootstrap)

        def get_link_ab_func(a, b):
            def link_func(_):
                a.value = json.dumps(b.value)
                return link_func

        for key in list(cls.deeplink_content.keys()).copy():
            if not hasattr(cls.deeplink_content[key], "value"):
                del cls.deeplink_content[key]
                continue
            trigger_widget = cls.deeplink_content[key]
            implements_value_widget = pn.widgets.TextInput(value=json.dumps(trigger_widget.value), width=0, height=0)
            cls.deeplink_content[key] = implements_value_widget
            bootstrap.sidebar.append(implements_value_widget)
            trigger_widget.param.watch(get_link_ab_func(cls.deeplink_content[key], trigger_widget), ["value"])

            # prepend = "" if IS_LOCAL else "https://"
            # postpend = "" if not cls.deeplink_content else \
            #     "'?' + " + " +  '&' + ".join(f"'{key}=' + {key.value}" for key in cls.deeplink_content)
            # deep_link_button.js_on_click(
            #     cls.deeplink_content,
            #     code=f"navigator.clipboard.writeText('{prepend}' + location.host + location.pathname + {postpend});"
            # )

        return bootstrap

    @classmethod
    def register(cls):
        print(f"Registering {cls.app_name}")
        cls.apps[cls.overview_category].append((cls.app_name, cls.run_app))

    @classmethod
    @abstractmethod
    def app_content(cls, bootstrapTemplate) -> BootstrapTemplate:
        pass

    @classmethod
    def serve(cls):
        cls.register()
        pn.serve({cls.app_name: cls.run_app}, port=8000, threaded=True, websocket_origin="*")





