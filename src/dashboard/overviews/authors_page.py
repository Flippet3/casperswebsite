import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate
from general_tools.general_tools import classproperty


class AuthorsPage(OverviewBase):
    overview_category = OverViewCategory.AuthorsPage

    @classproperty
    def app_name(cls):
        return "Author's_Page"

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        bootstrap.add_card("The Rhythm Of A Life")
        bootstrap.add_container(10)
        bootstrap.add_text("""The Rhythm of a Life" came to me while I was in Australia, where I'd unfold my foldable keyboard and type away on my phone in cafes and libraries.
        A lifelong love of poetry inspired me, but I wanted to challenge its conventions—transforming a poetry collection into a cohesive story.
        Each poem in the book is a chapter, weaving together the highs and lows of a life lived fully—birth to death—creating a narrative as rhythmic as its verse.
        <br><br>
        The book is available through Amazon in all countries, but <a href="https://www.amazon.com/dp/879753840X">here</a> is the link to the US store.
        <br><br>
        Some quotes to give an idea of what's in the book.
        <br>... With death’s clarity, I now see the beyond’s and before’s similarity.
        The difference is not in them; it is in you. ...
        <br>... Our default day had been so sweet, that we simply played it on repeat. ...
        <br>... It was an eternal drum that had played since birth of earth and sun.
        The knowledge in first and final hour: that it would end as it had begun. ...
        <br>... What can I do, what can I say, when my forever ever after will be taken away?
        <br>... How can my tears, be that of joy and fear, that of love and pain, that of loss and gain? ...
        <br>... What once excited, is now a bore, or worse, a chore. Or so I had thought too until fate had brought you. Suddenly it was the first time then, that it felt like the first time again.
        <br>... And now, with all I did and will do; by simply casting a glance at you; from my foundation, I finally unearth it; it’s all been so much more than worth it.
        """)
        bootstrap.add_container(2)
        bootstrap.add_image("https://m.media-amazon.com/images/I/611sECwxzsL._SY466_.jpg")

        bootstrap.add_card("My favourite books on writing")
        bootstrap.add_container(6)
        bootstrap.add_text("""While trying to be a writer for a year, I learned the depths of words and story structure.
        There's no one correct way of writing, but there sure are a lot of bad ones!
        Reading books on writing has been invaluable, three of them specifically.
        <br><br>On Writing: A Memoir of the Craft by Stephen King.
        Wonderfully writen, straight to the point, and inspirational for getting a good mindset for writing, not just as a hobby, but as a calling.
        <br><br>Save the Cat! Writes a Novel by Jessica Brody.
        To boldly go where none have gone before, it's crucial to know where some have gone before—lest you explore the already explored.
        I'm not sure if that makes sense, but in order to know what you're writing, it's good to know the history and patterns of writing.
        Reinventing the wheel is a fool's errand, and Jessica perfectly describes the wheels that already exist out there.
        And makes a compelling argument for being creative within patterns, rather than with patterns.
        <br><br>The Elements of Style by William Strunk Jr. and E.B. White.
        Writing is a window into a story.
        If words should evoke images and the imagination, then, by God, don't make your wordy windows tainted by purple prose or grammatical inconsistencies.
        The elements of style is a wonderful foundation of writing rules that unify your writing, such that meaning is never sacrificed.
        """)
        bootstrap.add_container(2)
        bootstrap.add_image("https://m.media-amazon.com/images/I/71nZU-k0pDL._SY466_.jpg")
        bootstrap.add_container(2)
        bootstrap.add_image("https://m.media-amazon.com/images/I/71FYfIkskdL._SY466_.jpg")
        bootstrap.add_container(2)
        bootstrap.add_image("https://m.media-amazon.com/images/I/71YA1iiEw7L._SY466_.jpg")

        return bootstrap
