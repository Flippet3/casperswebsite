from datetime import datetime, date
import yaml

import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate
from general_tools.general_tools import get_base_folder


class Resume(OverviewBase):
    overview_category = OverViewCategory.CV
    # Image source: https://icons8.com/icon/set/graduate/material

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:

        def add_card(title: str, text: str, img_ref: str, skills: list[str]):
            bootstrap.add_card(title, skills=skills)
            bootstrap.add_container(10)
            bootstrap.add_text(text)
            bootstrap.add_container(2)
            bootstrap.add_image(img_ref)
            bootstrap.add_container(12)
            bootstrap.add_text(f"Skills: {', '.join(skills)}")

        def add_education_card(school: str, education_type: str, start_year: int, end_year: int, img_ref: str, text: str, skills: list[str]):
            add_card(
                f"({start_year} - {end_year}) <img src='https://img.icons8.com/?size=24&id=86200&format=png'> {education_type} - {school}",
                text, img_ref, skills
            )

        def add_job_card(company: str, role: str, start_year: int, end_year: int, img_ref: str, text: str, skills: list[str]):
            add_card(
                f"({start_year} - {end_year}) <img src='https://img.icons8.com/?size=24&id=xkZW9nXosg6X&format=png'> {company} - {role}",
                text, img_ref, skills
            )

        def add_award_card(award: str, year: int, img_ref: str, text: str, skills: list[str]):
            add_card(
                f"({year}) <img src='https://img.icons8.com/?size=24&id=85600&format=png'> {award}",
                text, img_ref, skills
            )

        def add_certificate_card(certificate: str, year: int, img_ref: str, text: str, skills: list[str]):
            add_card(
                f"({year}) <img src='https://img.icons8.com/?size=24&id=6857&format=png'> {certificate}",
                text, img_ref, skills
            )

        def add_project_card(project: str, year: int, img_ref: str, text: str, skills: list[str]):
            add_card(
                f"({year}) <img src='https://img.icons8.com/?size=24&id=85878&format=png'> {project}",
                text, img_ref, skills
            )

        with open(get_base_folder() + "dashboard/overviews/resume.yaml", "r") as o:
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

        job_cards = sorted(filter(lambda x: x["type"] == "job", cards), key=lambda x: x["start"],
                                 reverse=True)
        for card in job_cards:
            add_job_card(card["company"], card["role"], card["start"].year, card["end"].year,
                               card["img_ref"], card["text"], card["skills"])

        education_cards = sorted(filter(lambda x: x["type"] == "education", cards), key=lambda x: x["start"], reverse=True)
        for card in education_cards:
            add_education_card(card["school"], card["education_type"], card["start"].year, card["end"].year, card["img_ref"], card["text"], card["skills"])

        certificate_cards = sorted(filter(lambda x: x["type"] == "certificate", cards), key=lambda x: x["year"], reverse=True)
        for card in certificate_cards:
            add_certificate_card(card["certificate"], card["year"].year, card["img_ref"], card["text"], card["skills"])

        award_cards = sorted(filter(lambda x: x["type"] == "award", cards), key=lambda x: x["year"], reverse=True)
        for card in award_cards:
            add_award_card(card["award"], card["year"].year, card["img_ref"], card["text"], card["skills"])

        project_cards = sorted(filter(lambda x: x["type"] == "project", cards), key=lambda x: x["year"], reverse=True)
        for card in project_cards:
            add_project_card(card["project"], card["year"].year, card["img_ref"], card["text"], card["skills"])

        return bootstrap
