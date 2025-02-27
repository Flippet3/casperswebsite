import logging
from abc import ABC, abstractmethod
from collections import defaultdict

import panel as pn

from dashboard.template import get_custom_template, CustomTemplate
from general_tools.general_tools import classproperty


class OverViewCategory:
    Home = "Home"
    CV = "Résumé"
    HowItsMade = "How It's Made"
    AuthorsPage = "Author's Page"
    Tools = "Tools"
    Shirt = "Shirt"

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
        bootstrap = get_custom_template()
        menu_options = []
        for overview_category, overview_category_overviews in cls.apps.items():
            if overview_category == OverViewCategory.Shirt:
                continue
            if len(overview_category_overviews) == 1:
                menu_options.append({
                    "label": str(overview_category).replace("_", " "),
                    "href": f"/{overview_category_overviews[0][0]}"
                })
            else:
                items = []
                for overview_category_overview in overview_category_overviews:
                    items.append({
                        "label": overview_category_overview[0].replace("_", " "),
                        "href": f"/{overview_category_overview[0]}"
                    })
                menu_options.append({
                    "label": overview_category.replace("_", " "),
                    "items": items
                })
        bootstrap.add_variable("menu_options", menu_options)
        bootstrap = cls.app_content(bootstrap)
        bootstrap.resolve_cards()
        return bootstrap

    @classmethod
    def register(cls):
        print(f"Registering {cls.app_name}")
        cls.apps[cls.overview_category].append((cls.app_name, cls.run_app))

    @classmethod
    @abstractmethod
    def app_content(cls, bootstrap_template: CustomTemplate) -> CustomTemplate:
        pass

    @classmethod
    def serve(cls):
        cls.register()
        pn.serve({cls.app_name: cls.run_app}, port=8000, threaded=True, websocket_origin="*")





