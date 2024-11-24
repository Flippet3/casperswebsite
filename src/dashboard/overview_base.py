import json
import threading
import logging
from abc import ABC, abstractmethod
from collections import defaultdict

import panel as pn
from panel.template import BootstrapTemplate

from src.dashboard.template import get_custom_template
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
        # bootstrap = pn.template.bootstrap.BootstrapTemplate(title=cls.app_name)
        bootstrap = get_custom_template()
        menu_options = []
        for overview_category, overview_category_overviews in cls.apps.items():
            if len(overview_category_overviews) == 1:
                menu_options.append({
                    "label": overview_category_overviews[0][0],
                    "href": f"/{overview_category_overviews[0][0]}"
                })
            else:
                items = []
                for overview_category_overview in overview_category_overviews:
                    items.append({
                        "label": overview_category_overview[0],
                        "href": f"/{overview_category_overview[0]}"
                    })
                menu_options.append({
                    "label": overview_category,
                    "items": items
                })
        bootstrap.add_variable("menu_options", menu_options)
        bootstrap = cls.app_content(bootstrap)
        return bootstrap



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





