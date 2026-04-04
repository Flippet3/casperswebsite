from casperswebsite.dashbuilder.contract import (
    CardInfo,
    ContainerInfo,
    EmbedType,
    OverViewCategory,
    PageInfo,
)


class HomePage:
    def build_page(self) -> PageInfo:
        return PageInfo(
            category=OverViewCategory.Home,
            title="Home",
            cards=[
                CardInfo(
                    title="Intro",
                    containers=[
                        ContainerInfo(
                            width=6,
                            embed_type=EmbedType.Text,
                            content="Hello -- welcome to my website! My name is Casper and I'm a Dutch guy living in Denmark. For those interested in how I made this website, check out the 'how it's made' page. For those interested in why I made this website, I can't help you -- it just kind of happened.",
                        ),
                        ContainerInfo(
                            width=6,
                            embed_type=EmbedType.Image,
                            content="https://s13.gifyu.com/images/bqbsp.gif",
                        ),
                    ],
                )
            ],
        )
