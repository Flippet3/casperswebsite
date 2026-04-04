from casperswebsite.dashbuilder.contract import (
    CardInfo,
    ContainerInfo,
    EmbedType,
    OverViewCategory,
    PageInfo,
)


class HowItsMadePage:
    def build_page(self) -> PageInfo:
        return PageInfo(
            category=OverViewCategory.HowItsMade,
            title="How it's made",
            cards=[
                CardInfo(
                    title="How it's made",
                    containers=[
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Text,
                            content="Magic.",
                        ),
                    ],
                ),
                CardInfo(
                    title="How it's really made",
                    containers=[
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Text,
                            content=(
                                "This website is built dynamically using Jinja2 and python.\n"
                                "         It is hosted on a small droplet (digital ocean) and uses Holoviz Panel to configure any interactive widgets.\n"
                                "         I've set-up a pipeline using Github Actions to automatically update this whenever I make a change to the repo.\n"
                                "         Oh yeah, the repo is public, and can be found <a href='https://github.com/Flippet3/casperswebsite'>here</a> if you'd like to take a look for yourself!"
                            ),
                        ),
                    ],
                ),
            ],
        )
