"""Final transformation passes that work solely on text."""

import re

from marysue.objects import Object
from marysue.state import State


def proofread(text):
    text = text.replace("`", "'")

    dingus = State(Object(names=('dingus',)))
    verbs = []
    for k, v in dingus.saids.iteritems():
        verbs.extend(list(v))
    for k, v in dingus.shouteds.iteritems():
        verbs.extend(list(v))
    
    for verb in verbs:
        text = text.replace(verb + ' he', 'he ' + verb)
        text = text.replace(verb + ' she', 'she ' + verb)

    return text


def word_count(text):
    return len([
        z for z in re.split(r'\s', text) if z not in ('', '-', '#', '##', '###')
    ])
