from collections import defaultdict
import os

from casperswebsite.dashbuilder.contract import OverViewCategory, Page


def render_pages(pages: list[Page]) -> dict[str, str]:
    page_infos = [page.build_page() for page in pages]

    menu_options = []
    categories_map = defaultdict(list)
    for page_info in page_infos:
        categories_map[page_info.category].append(page_info)
    for overview_category, category_pages in categories_map.items():
        if overview_category == OverViewCategory.Hidden:
            continue
        if len(category_pages) == 1:
            menu_options.append(
                {
                    "label": overview_category.value,
                    "href": "/" + category_pages[0].href,
                }
            )
        else:
            items = []
            for category_page in category_pages:
                items.append(
                    {"label": category_page.title, "href": "/" + category_page.href}
                )
            menu_options.append({"label": overview_category.value, "items": items})

    from jinja2 import Environment, FileSystemLoader

    template_dir = os.path.dirname(__file__)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("index.html")

    rendered_pages = {}

    for page_info in page_infos:
        rendered = template.render(
            title=page_info.title,
            header_html=page_info.header_html,
            menu_options=menu_options if page_info.category != OverViewCategory.Hidden else [],
            cards=page_info.cards,
        )
        rendered_pages[page_info.href] = rendered
    return rendered_pages
