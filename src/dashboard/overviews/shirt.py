import os
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from datetime import datetime

import panel as pn

from dashboard.overview_base import OverviewBase, OverViewCategory
from dashboard.template import CustomTemplate

thisdir = str(os.path.dirname(os.path.realpath(__file__)))


DATA_FOLDER = "Data"
PERSISTENCE_FILE = DATA_FOLDER + "/persistence_text.txt"
VISITOR_FILE = DATA_FOLDER + "/visitor_count.txt"
COMMENT_VISITOR_FILE = DATA_FOLDER + "/comment_section_visitor_count.txt"


messages = [
    "Hello!",
    "You've reached the website for my shirt. I'm not entirely sure what you were hoping to find here...",
    "But you curious you, saw a link on someone's shirt and fucking typed it in!",
    "I've got to commend you on your inquisitiveness.",
    "Sadly though, there's not much here.",
    "There's no link on where to get a shirt for yourself with my face on it",
    "No donation page to buy me a coffee; honestly I'm good caffeine-wise.",
    "Just nothing.",
    "Thanks for stopping by though!",
    "Feel free to say hi as well, I like a good chat.",
    "Unless I'm looking focussed or sad, or like I'm listening to some really good music and going up in it!",
    "Honestly probably you can tell if I'd be up for a little chat or no.",
    "I don't need to give you social lessons. You got this!",
    "Well.",
    "That's it.",
    "Nothing more here for you.",
    "I'm happy you stopped by though!",
    "Have a lovely day!",
    "...",
    "...",
    "Well well well.",
    "It's never enough right?",
    "You just love to dive down some rabbit hole don't jah?",
    "Well, if it's a rabbit hole you want... A rabbit hole I will give you!",
    "While I have your attention, let me ask you a question:",
    "How deep do you think this goes?",
    "How much effort do you think I've put into this little project?",
    "Surely this is no bottomless pit.",
    "At some point you've got to reach the end right?",
    "But when?",
    "All that you know, is that you're not there yet.",
    "I suppose this is a battle of attrition now.",
    "We'll see who can hold out the longest",
    "Having made it this far, you're a worthy foe at least.",
    "I've been waiting for this!",
    "Don't worry, I won't use dirty programming tricks.",
    "Nor will I use any AI generation or whatever to automatically generate these little prompts.",
    "In return I expect you to read all the prompts, not skipping through it all willy nilly",
    "It'll just be a monologue by a stranger who had a link on his shirt.",
    "That you get to read through.",
    "One message at the time. And so also.. Once upon a time...",
    "Nah I'm not gonna tell you an actual story.",
    "I'm sorry, I just can't.",
    "I consider myself a story teller, but only though speech. Not through text.",
    "I can share with you a poem that I wrote though.",
    "It's called:",
    "The man with the shirt",
    "And it goes as follows:",
    "I saw a man with a shirt",
    "It looked somewhat absurd",
    "In the spot where usually, a logo you'd place",
    "There was just this man's face",
    "Although when looking closer",
    "Giving his shirt a once over",
    "The man with the shirt",
    "Wore a shirt where",
    "He wore a shirt where",
    "He wore a shirt where",
    "He wore his face",
    "What a weird time and place",
    "To show off your face",
    "...",
    "Alright, not my best work.",
    "But hey, remember.. you're here on your free will.",
    "I didn't ask you to be here!",
    "Though I don't mind it :--)",
    "I feel like you might win this battle of attrition.",
    "I've said what I wanted to say.",
    "And much more beyond that.",
    "...",
    "...",
    "...",
    "common...",
    "go...",
    "Alright, dirty programming trick time.",
    "I'm gonna put a 1000 text messages in here counting up",
    "I'm sorry...",
    "You were doomed to never succeed here",
    "Though I'm proud of how far you came.",
    "I feel closer to you now.",
    "Although I have no idea who you are",
    "If you've got time to goof off for what seems like at least a couple minutes, in my book you're alright.",
    "I'm sorry it had to end this way...",
    "1",
    "2",
    "3",
    "4",
    "5",
    "7",
    "woops, skipped 6.",
    "6",
    "7",
    "Though I suppose I already did 7 right?",
    "So now I did it twice.",
    "Ugh.",
    "I'll start over.",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "...",
    "Do I do 7 again now, even though I did it twice last time?",
    "Anyways.. Truly... why are you still here?",
    "I told you I'd make you click through a 1000 useless numbers",
    "And you were like... Yeah, sure, let's go!",
    "Now I feel bad.",
    "You were willing to put in the time.",
    "And here I was, going to cheat you out of it...",
    "Alright, you know what.",
    "You win.",
    "That's right.",
    "You've done it.",
    "You've beat me.",
    "You're the better person",
    "Exactly what you've done, or what you've won, doesn't matter.",
    "Just know that you did.",
    "It's been a pleasure.",
    "You've unlocked...",
    "The super secret link to the comment section",
    "https://caspersweb.site/shirt?comments=True"
]

def obscure(data: int) -> str:
    return b64e(zlib.compress(str(data).encode(), 9)).decode()


def unobscure(obscured: str) -> int:
    return int(zlib.decompress(b64d(obscured.encode())).decode())


# Functions to control the persistence text
def get_persistence_text():
    with open(PERSISTENCE_FILE, "r") as f:
        output = f.read()
    return output


def add_persistence_text(text, add_timestamp=True):
    if len(text) > 0:
        with open(PERSISTENCE_FILE, 'a+') as f:
            if add_timestamp:
                f.write(f"Comment added on: {datetime.utcnow().isoformat()} (UTC)\n")
            f.write(text[0:1000] + "\n\n")


def clear_persistence_text():
    os.remove(PERSISTENCE_FILE)
    f = open(PERSISTENCE_FILE, "x")
    f.close()


def get_nr_visitors(comment_section=False) -> int:
    filepath = VISITOR_FILE if not comment_section else COMMENT_VISITOR_FILE
    with open(filepath, "r") as f:
        output = f.read()
    return int(output)


def set_nr_visitors(value: int, comment_section=False):
    filepath = VISITOR_FILE if not comment_section else COMMENT_VISITOR_FILE
    with open(filepath, "w") as f:
        f.write(str(value))


def create_data_folder_and_file():
    # Create all files required for persistance
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    for filepath, init_value in ((PERSISTENCE_FILE, ""), (VISITOR_FILE, "0"), (COMMENT_VISITOR_FILE, "0")):
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(init_value)

class Shirt(OverviewBase):
    overview_category = OverViewCategory.Shirt

    @classmethod
    def app_content(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        create_data_folder_and_file()
        session_args = {k: v[0].decode() for (k, v) in pn.state.session_args.items()}
        if "admin" in session_args:
            if session_args["admin"] == "supersecretpassword":
                return cls.run_admin_page(bootstrap)
        if "comments" in session_args:
            set_nr_visitors(get_nr_visitors(comment_section=True) + 1, comment_section=True)
            return cls.run_comment_section(bootstrap)

        set_nr_visitors(get_nr_visitors() + 1)

        html_pane = pn.pane.HTML(r"""
        <div class="customclass" style="font-size: large;">Something to start off with</div>
        """)
        start_message_id = 0 if "messageid" not in session_args else unobscure(session_args["messageid"])

        current_index = [start_message_id]

        button_holder = pn.Row(align='center', height=50, width=150)
        button1 = pn.widgets.Button(name="Next", height=50, width=150, align='center')
        button2 = pn.widgets.Button(name="TO THE COMMENTS!", height=50, width=150, align='center')
        button_holder.append(button1)

        def set_html_pane(*args):
            cridx = current_index[0]
            if not cridx > len(messages) - 1:
                current_index[0] += 1
                html_pane.object = fr"<div class='customclass' style='font-size: large;'>{messages[cridx]}</div>"
                pn.state.location.search = f"?messageid={obscure(cridx)}"
                if cridx == len(messages) - 1:
                    button_holder.clear()
                    button_holder.append(button2)

        set_html_pane()

        button1.on_click(set_html_pane)
        button2.js_on_click(code=f"window.open('//' + location.host + location.pathname + '?comments=True', '_self');")

        bootstrap.add_card("So you typed in the link, eh?")
        bootstrap.add_container(12)
        bootstrap.add_panel_component(html_pane)
        bootstrap.add_panel_component(button_holder)
        return bootstrap

    @classmethod
    def run_admin_page(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        persistence_text_field = pn.widgets.TextAreaInput(value=get_persistence_text())
        persistence_submit_button = pn.widgets.Button(name="Submit", width=50, css_classes=["standard-button"])

        viewing_info = pn.pane.Str(f"""number of visitors = {get_nr_visitors()}
    number of comments visitors = {get_nr_visitors(comment_section=True)}""", css_classes=["text-dark-background"])

        def on_persistence_submit_button(event):
            clear_persistence_text()
            add_persistence_text(persistence_text_field.value, add_timestamp=False)

        persistence_submit_button.on_click(on_persistence_submit_button)

        bootstrap.add_card("Admin Page.")
        bootstrap.add_container(12)
        bootstrap.add_panel_component(persistence_text_field)
        bootstrap.add_panel_component(persistence_submit_button)
        bootstrap.add_panel_component(viewing_info)
        return bootstrap

    @classmethod
    def run_comment_section(cls, bootstrap: CustomTemplate) -> CustomTemplate:
        # Populate the persistence tab with a widget that allows text input and a submit button to submit the text in the field. Also below it, show the inputs provided which will be logged in a txt file.
        persistence_text_field = pn.widgets.TextInput(placeholder="Type some text here...")
        persistence_submit_button = pn.widgets.Button(name="Submit", width=50, css_classes=["standard-button"])
        persistence_submissions_text = pn.pane.Str(get_persistence_text(), css_classes=["text-dark-background"])

        def on_persistence_submit_button(event):
            add_persistence_text(persistence_text_field.value)
            persistence_text_field.value = ""
            persistence_submissions_text.object = get_persistence_text()

        persistence_submit_button.on_click(on_persistence_submit_button)

        bootstrap.add_card("Super secret comment section")
        bootstrap.add_container(12)
        bootstrap.add_panel_component(persistence_text_field)
        bootstrap.add_panel_component(persistence_submit_button)
        bootstrap.add_panel_component(persistence_submissions_text)
        return bootstrap


