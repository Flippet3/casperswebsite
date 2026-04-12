from __future__ import annotations

import html
import re
from collections.abc import Sequence
from dataclasses import dataclass

from bokeh.embed import components
from bokeh.layouts import column, row
from bokeh.models.layouts import Column
from bokeh.models import Button, CustomJS, Div, TextInput

from casperswebsite.dashbuilder.contract import (
    CardInfo,
    ContainerInfo,
    EmbedType,
    OverViewCategory,
    PageInfo,
)


def _safe_paragraph(text: str) -> str:
    return "<p>" + html.escape(text).replace("\n", "<br>\n") + "</p>"


# Python allows ``(?i)`` etc. at the start of a pattern; JS needs the second
# ``RegExp`` argument instead (inline ``(?i)`` is not portable and throws).
_INLINE_FLAGS = re.compile(r"^\(\?([imsux]+)\)")


def _js_regexp_source_and_flags(pattern: str) -> tuple[str, str]:
    m = _INLINE_FLAGS.match(pattern)
    if not m:
        return pattern, ""
    letters = m.group(1).lower()
    # ``x`` (verbose) has no JS equivalent; ``i``, ``m``, ``s``, ``u`` do.
    js_flags = "".join(dict.fromkeys(c for c in letters if c in "imsu"))
    return pattern[m.end() :], js_flags


@dataclass(frozen=True)
class FlowStep:
    """One gated question. Client-side check only (answers appear in page JS).

    ``rules`` maps regex source strings to ``(is_correct, message)``. Patterns are
    tried in dict order; the first match wins. Leading Python inline flags like
    ``(?i)`` are converted for JavaScript (passed as ``RegExp`` flags, not left in
    the source string). If nothing matches, the answer is treated as wrong and a
    default sad response is shown.
    """

    question: str
    rules: dict[str, tuple[bool, str]]


def build_gated_flow(
    steps: Sequence[FlowStep],
    *,
    final_image: str,
    final_image_alt: str = "",
) -> Column:
    """Stack of question rows; each unlocks the next via ``CustomJS`` on Submit."""

    if not final_image:
        msg = "final_image must be a non-empty URL or path"
        raise ValueError(msg)

    safe_src = html.escape(final_image, quote=True)
    safe_alt = html.escape(final_image_alt, quote=True)
    final_div = Div(
        text=f'<p><img src="{safe_src}" alt="{safe_alt}" style="max-width:100%;height:auto;"/></p>',
        sizing_mode="stretch_width",
    )
    final_wrap = column(final_div, sizing_mode="stretch_width", visible=len(steps) == 0,)

    stage_columns: list[column] = [final_wrap]

    for i, step in zip(reversed(range(len(steps))), reversed(steps)):
        q_div = Div(text=_safe_paragraph(step.question), sizing_mode="stretch_width")
        inp = TextInput(value="", title="", sizing_mode="stretch_width")
        btn = Button(label="Submit", button_type="primary", width=100)
        feedback = Div(text="", sizing_mode="stretch_width", visible=False)

        stage_body = column(
            q_div,
            row(inp, btn, sizing_mode="stretch_width"),
            feedback,
            sizing_mode="stretch_width",
        )
        stage_col = column(stage_body, sizing_mode="stretch_width", visible=(i == 0))
        stage_columns.insert(0, stage_col)

        patterns: list[str] = []
        regexp_flags: list[str] = []
        correct_flags: list[bool] = []
        reply_html: list[str] = []
        for pat, (ok, msg) in step.rules.items():
            body, fl = _js_regexp_source_and_flags(pat)
            patterns.append(body)
            regexp_flags.append(fl)
            correct_flags.append(ok)
            reply_html.append(_safe_paragraph(msg))
        no_match_html = _safe_paragraph(":(")

        btn.js_on_click(
            CustomJS(
                args=dict(
                    input=inp,
                    feedback=feedback,
                    submit=btn,
                    patterns=patterns,
                    regexp_flags=regexp_flags,
                    correct_flags=correct_flags,
                    replies=reply_html,
                    no_match_html=no_match_html,
                    next_stage=stage_columns[1],
                ),
                code="""
                const v = (input.value || "").trim();
                for (let i = 0; i < patterns.length; i++) {
                    const re = new RegExp(patterns[i], regexp_flags[i] || "");
                    if (re.test(v)) {
                        feedback.visible = true;
                        feedback.text = replies[i] || "";
                        if (correct_flags[i]) {
                            input.disabled = true;
                            submit.disabled = true;
                            next_stage.visible = true;
                        }
                        return;
                    }
                }
                feedback.visible = true;
                feedback.text = no_match_html;
                """,
            )
        )

    return column(*stage_columns, sizing_mode="stretch_width")


class Jasmin:
    def build_page(self) -> PageInfo:
        layout = build_gated_flow(
            [
                FlowStep(
                    question="What's your name?",
                    rules={
                        r"(?i)^.+\s.+$": (
                            False,
                            "First name *and* last name? What kind of high horse were you born on top of?!",
                        ),
                        r"(?i)^jasmin$": (False, "Omg, that's, like, such a crazy name. I thought you were skinnier than that S____y. If you have more than two dimensions, I don't want you on this page."),
                        r"(?i)^jas$": (
                            False,
                            "Jas? Bit casual, no?",
                        ),
                        r"(?i)^stace?y$": (
                            True,
                            "Omg, you betch, you look so skinny!",
                        ),
                        r"(?i)^caim[aá]n$": (
                            False,
                            "Cute, but no - not how your Peruvian family knows you."
                        ),
                        r"(?i)^casper$": (
                            False,
                            "No! That's me, you goofball!"
                        ),

                        r".*": (False, "I'm not sure this site was made for you. Go away!")
                    },
                ),
                FlowStep(
                    question="How old are you?",
                    rules={
                        r"^25$": (False, "Stop living in the past..."),
                        r"^26$": (True, "Too cool for school, but not cool enough for bridge club. What a beautiful age!"),
                        r"^30$": (False, "You wish! Only a select really cool group of people are this age."),
                        r"^(2[7-9]|[3-9][0-9]|[1-9][0-9]{2,})$": (False, "Hold your horses, you're not there yet!"),
                        r"^([1]?[0-9]|2[0-4])$": (False, "I heard a click from your knee when you stood up. I don't buy it."),
                        r".*": (False, "I only understand numbers. :("),
                    },
                ),
                FlowStep(
                    question="What's the ideal age?",
                    rules={
                        r"^25$": (False, "Sooooooo 2025."),
                        r"^26$": (False, "Almost. Second best, I'd say! I mean, it's good, but it's not the peak of humanity."),
                        r"^30$": (True, "Your words, not mine..."),
                        r"^([3-9][0-9]|[1-9][0-9]{2,})$": (False, "Naah, way to old!"),
                        r"^([1]?[0-9]|2[0-9])$": (False, "Not wise enough..."),
                        r".*": (False, "I only understand numbers. :("),
                    },
                ),
                FlowStep(
                    question="Where do you live?",
                    rules={
                        r"(?i)\b(uk|england|brittany|london)\b": (
                            True, 
                            "You tea slurper!"
                        ),
                        r"(?i)\b(nl|netherlands|the netherlands|holland)\b": (
                            False,
                            "Yeah?! Where's your orange afro? I don't buy it!"
                        ),
                        r"(?i)\b(dk|denmark)\b": (
                            False,
                            "Mhm, visiting a farmor doesn't count."
                        ),
                        r"(?i)\b(peru|pe)\b": (
                            False,
                            "¡Hola, Peruano! ¿Do you like blood clams?"
                        ),
                        r".*": (False, "Never heard of it. Do they even have tea there?"),
                    },
                ),
                FlowStep(
                    question="How many days have we known each other?",
                    rules={
                        r"^([1-9][0-9]{0,2}|1[0-4][0-9]{2})$": (False, "Much longer..."),
                        r"^(1[5][0-9]{2}|16[0-4][0-9])$": (False, "Almost!"),
                        r"^1702$": (True, "Yep! I had to scroll for 15 minutes through facebook messages to see our first message..."),
                        r"^(16[5-9][0-9]|17[0-4][0-9]|1750)$": (True, "Close enough! It's 1702 - I had to scroll for 15 minutes through facebook messages to see our first message..."),
                        r"^(17[5-9][0-9]|18[0-9]{2}|19[0-9]{2}|[2-9][0-9]{3,}|[1-9][0-9]{4,})$": (False, "not there (yet) 👉👈"),
                        r".*": (False, "I only understand numbers. :("),
                    },
                ),
                FlowStep(
                    question="What was your first message to me?",
                    rules={
                        r"(?i)^sorry who are you\?$": (
                            True,
                            "Damn... did you also scroll for 15 minutes?"
                        ),
                        r".*": (True, "It was 'Sorry who are you?'"),
                    },
                ),
                FlowStep(
                    question="What was the third?",
                    rules={
                        r"(?i)^message failed\. you will be reported to the police if this harrassment continues\.$": (
                            True,
                            "Jep... that was pretty fucking tough."
                        ),
                        r".*": (True, "It was 'Message failed. You will be reported to the police if this harrassment continues.' Not sure why I kept messaging at this point."),
                    },
                ),
                FlowStep(
                    question="And the fourth? (last I'll ask about)",
                    rules={
                        r"(?i)^Please click here to join the sex offenders register: www\.cantbearoundkids\.com$": (
                            True,
                            "I'm phenomenal with kids, if you must know."
                        ),
                        r".*": (True, "It was 'Please click here to join the sex offenders register: www.cantbearoundkids.com'. It linked to a website with just my face for some reason?"),
                    },
                ),
                FlowStep(
                    question="Okay, but it did get better from there. Like, are you super important to me now?",
                    rules={
                        r"(?i)^yes$": (
                            True,
                            "Big ego, huh?"
                        ),
                        r"(?i)^no$": (
                            False,
                            "Try again!"
                        ),
                        r".*": (False, "Please answer yes or no."),
                    },
                ),
                FlowStep(
                    question="Am I super happy to have you in my life, even if only a few times a year?",
                    rules={
                        r"(?i)^yes$": (
                            True,
                            "Sjeesh, ever heard of humble?"
                        ),
                        r"(?i)^no$": (
                            False,
                            "Try again!"
                        ),
                        r".*": (False, "Please answer yes or no."),
                    },
                ),
                FlowStep(
                    question="Let's try something less personal. To goof or not to goof?",
                    rules={
                        r"(?i)^(?:to )?goof$": (
                            True,
                            "XD XD XD ROFL"
                        ),
                        r"(?i)^not to goof$": (
                            False,
                            "But why not goof :(?"
                        ),
                        r".*": (False, "Please answer 'to goof' or 'not to goof'."),
                    },
                ),
                FlowStep(
                    question="Imagine you'd ranked all of your friends by how much they mean to you -- what's the name of someone who would definitely make it in the top 300?",
                    rules={
                        r"(?i)casper": (
                            True, 
                            "😳 - Happy birthday! Thinking of you x."
                        ),
                        r".*": (False, "Mhm, not the one I'm after."),
                    },
                ),
            ],
            final_image="../static/egg.png",
            final_image_alt="celebration",
        )
        script, div = components(layout)

        return PageInfo(
            category=OverViewCategory.Hidden,
            title="Jasmin",
            header_html=f"{script}",
            cards=[
                CardInfo(
                    title="Flow",
                    containers=[
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Text,
                            content="Welcome to a super straight-forward quiz. There's no easter eggs in any of the questions at all, so there's no need to be smart or cheeky -- just answer normally!",
                        ),
                        ContainerInfo(
                            width=12,
                            embed_type=EmbedType.Html,
                            content=div,
                        ),
                    ],
                )
            ],
        )
