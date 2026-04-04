import yaml
from datetime import date

from bokeh.models import MultiChoice, CustomJS, Div
from bokeh.layouts import column
from bokeh.embed import components

from casperswebsite.dashbuilder.contract import (
    CardInfo,
    ContainerInfo,
    EmbedType,
    OverViewCategory,
    PageInfo,
)
from casperswebsite.general_tools import get_module_folder

with open(get_module_folder() + "dashboard/pages/resume.yaml", "r") as o:
    cards = yaml.load(o, yaml.SafeLoader)["cards"]

all_skills = sorted(set(skill for card in cards for skill in card["skills"]))


def _resume_bokeh_component():
    # This Bokeh component creates a MultiChoice skill filter and injects customJS into frontend
    multi_choice = MultiChoice(value=[], options=all_skills, width=400, title="Skills")
    js_code = """
    const selected_skills = this.value;
    const cards = document.getElementsByClassName('card');
    for (let card of cards) {
        const cardSkills = card.attributes.tag ? card.attributes.tag.value.split(',') : [];
        const match = selected_skills.length === 0 || selected_skills.some(skill => cardSkills.includes(skill));
        card.style.display = match ? '' : 'none';

        // Update corresponding navigation link
        const cardId = card.id;
        const navLink = document.querySelector(`a[data-card-id="${cardId}"]`);
        if (navLink) {
            navLink.style.display = match ? '' : 'none';
        }
    }
    """
    multi_choice.js_on_change("value", CustomJS(code=js_code))
    message = Div(
        text="<b>Click the box below to select the skills that you are interested in, and filter for relevant cards.</b>"
    )

    layout = column(message, multi_choice, sizing_mode="stretch_width")
    return components(layout)


class ResumePage:
    def build_page(self) -> PageInfo:
        bokeh_script, bokeh_div = _resume_bokeh_component()

        # skills selector 'card'
        selector_card = CardInfo(
            title="Select skills",
            containers=[
                ContainerInfo(
                    width=12,
                    embed_type=EmbedType.Html,
                    content=bokeh_div,
                )
            ],
            tag=",".join(all_skills),
        )

        # icon, title_template, year_attr, entity_fields mapping per card type
        _CARD_TYPE_CONFIG = {
            "job": {
                "icon": "xkZW9nXosg6X",
                "title_template": "({start} - {end}) {company} - {role}",
                "year_attr": ["start", "end"],
                "entity_fields": ["company", "role"],
            },
            "education": {
                "icon": "86200",
                "title_template": "({start} - {end}) {education_type} - {school}",
                "year_attr": ["start", "end"],
                "entity_fields": ["education_type", "school"],
            },
            "certificate": {
                "icon": "6857",
                "title_template": "({year}) {certificate}",
                "year_attr": ["year"],
                "entity_fields": ["certificate"],
            },
            "award": {
                "icon": "85600",
                "title_template": "({year}) {award}",
                "year_attr": ["year"],
                "entity_fields": ["award"],
            },
            "project": {
                "icon": "85878",
                "title_template": "({year}) {project}",
                "year_attr": ["year"],
                "entity_fields": ["project"],
            },
        }

        def _make_card(card, card_type):
            cfg = _CARD_TYPE_CONFIG[card_type]
            icon_url = f"https://img.icons8.com/?size=24&id={cfg['icon']}&format=png"

            # Gather year values safely (handle start.year, end.year vs year.year)
            def get_year(val):
                return val.year if hasattr(val, "year") else val

            years = [get_year(card[y]) for y in cfg["year_attr"]]
            # Map years into the template
            title_vars = {k: card[k] for k in cfg["entity_fields"]}
            # Fill in 'start' and 'end' (if needed) for jobs/education
            for year, yattr in zip(years, cfg["year_attr"]):
                title_vars[yattr] = year
            # Compose the title
            title = f"<img src='{icon_url}'> " + cfg["title_template"].format(
                **title_vars
            )
            return CardInfo(
                title=title,
                containers=[
                    ContainerInfo(
                        width=10,
                        embed_type=EmbedType.Text,
                        content=card["text"],
                    ),
                    ContainerInfo(
                        width=2,
                        embed_type=EmbedType.Image,
                        content=card["img_ref"],
                    ),
                    ContainerInfo(
                        width=12,
                        embed_type=EmbedType.Text,
                        content=f"Skills: {', '.join(card['skills'])}",
                    ),
                ],
                tag=",".join(card["skills"]),
            )

        # We'll sort and process cards as in the original logic
        job_cards = sorted(
            [card for card in cards if card["type"] == "job"],
            key=lambda x: x["start"],
            reverse=True,
        )
        for job_card in job_cards:
            if job_card["end"] == "current":
                job_card["end"] = date.today()
        education_cards = sorted(
            [card for card in cards if card["type"] == "education"],
            key=lambda x: x["start"],
            reverse=True,
        )
        certificate_cards = sorted(
            [card for card in cards if card["type"] == "certificate"],
            key=lambda x: x["year"],
            reverse=True,
        )
        award_cards = sorted(
            [card for card in cards if card["type"] == "award"],
            key=lambda x: x["year"],
            reverse=True,
        )
        project_cards = sorted(
            [card for card in cards if card["type"] == "project"],
            key=lambda x: x["year"],
            reverse=True,
        )

        # Replace original card makers with use of _make_card
        def _make_job_card(card):
            return _make_card(card, "job")

        def _make_education_card(card):
            return _make_card(card, "education")

        def _make_certificate_card(card):
            return _make_card(card, "certificate")

        def _make_award_card(card):
            return _make_card(card, "award")

        def _make_project_card(card):
            return _make_card(card, "project")

        # Compose all cards
        card_infos = [selector_card]
        card_infos.extend([_make_job_card(card) for card in job_cards])
        card_infos.extend([_make_education_card(card) for card in education_cards])
        card_infos.extend([_make_certificate_card(card) for card in certificate_cards])
        card_infos.extend([_make_award_card(card) for card in award_cards])
        card_infos.extend([_make_project_card(card) for card in project_cards])

        return PageInfo(
            category=OverViewCategory.CV,
            title="Résumé",
            header_html=bokeh_script,
            cards=card_infos,
        )
