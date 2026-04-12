from enum import Enum, auto
from typing import Protocol
from pydantic import BaseModel, Field


class OverViewCategory(Enum):
    Home = "Home"
    CV = "Résumé"
    HowItsMade = "How It's Made"
    AuthorsPage = "Author's Page"
    Tools = "Tools"
    Hidden = "Hidden"
    EnergySimulation = "Energy Simulation"


class EmbedType(Enum):
    Text = auto()
    Image = auto()
    Html = auto()


class ContainerInfo(BaseModel):
    width: int = Field(ge=1, le=12)
    embed_type: EmbedType
    content: str


class CardInfo(BaseModel):
    title: str
    containers: list[ContainerInfo]
    tag: str = ""
    style: str = ""
    header_style: str = ""
    body_style: str = ""


class PageInfo(BaseModel):
    category: OverViewCategory
    title: str
    cards: list[CardInfo]
    header_html: str = ""

    @property
    def href(self) -> str:
        return self.title.replace(" ", "_")


class Page(Protocol):
    def build_page(self) -> PageInfo: ...
