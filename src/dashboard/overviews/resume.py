from datetime import datetime, date
import yaml

import panel as pn
from bokeh.models import CustomJS

from src.dashboard.overview_base import OverviewBase, OverViewCategory
from src.dashboard.template import CustomTemplate
from src.general_tools.general_tools import get_base_folder


class Resume(OverviewBase):
    overview_category = OverViewCategory.CV

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        def add_education_card(school: str, education_type: str, start_year: int, end_year: int, img_ref: str, text: str, skills: list[str]):
            bootstrap.add_card(f"({start_year} - {end_year}) Education - {education_type} - {school}", skills=skills)
            bootstrap.add_container(10)
            bootstrap.add_text(text)
            bootstrap.add_container(2)
            bootstrap.add_image(img_ref)
            bootstrap.add_container(12)
            bootstrap.add_text(f"Skills: {', '.join(skills)}")

        with open(get_base_folder() + "dashboard\\overviews\\resume.yaml", "r") as o:
            cards = yaml.load(o, yaml.SafeLoader)["cards"]

        all_skills = sorted(set(sum(map(lambda x: x["skills"], cards), [])))

        multi_choice = pn.widgets.MultiChoice(value=[], options=all_skills)

        custom_js = """
        const selected_skills = cb_obj.value;
        const cards = document.getElementsByClassName('card');
        for (let card of cards) {
            const cardSkills = card.dataset.skills ? card.dataset.skills.split(',') : [];
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

        multi_choice.jscallback(value=custom_js)

        bootstrap.add_card("Select skills", skills=all_skills)
        bootstrap.add_container(12)
        bootstrap.add_text("Select the skills here that you are interested in, and, below, you'll only see the cards that are of interest to those specific skills.")
        bootstrap.add_panel_component(multi_choice)

        education_cards = sorted(filter(lambda x: x["type"] == "education", cards), key=lambda x: x["start"], reverse=True)
        for card in education_cards:
            add_education_card(card["school"], card["education_type"], card["start"].year, card["end"].year, card["img_ref"], card["text"], card["skills"])

        return bootstrap
