import functools
import re

from wiktionaryparser import WiktionaryParser

import tekinbot.utils.post as pu
from tekinbot.comms.message import what_is
from tekinbot.utils.config import tekin_id


comm_re = re.compile(
    f'^{tekin_id} define (?P<message>.*)$', flags=re.IGNORECASE)


@functools.lru_cache(maxsize=1)
def parser():
    return WiktionaryParser()


def process(request):
    message = re.fullmatch(
        comm_re, request['event']['text']
    ).group('message')
    if len(message.split(' ')) > 1:
        return what_is.process(request)
    word = parser().fetch(message)

    if not word:
        return f'Not sure how to define {message}'
    else:
        word = word[0]
    # the wiktionary parser has some problems in parsing the definitions
    # change this part after submitting the pull request

    # split(\n)[0] will always be the tense/form of the word
    # e.g. and etc. mess with the split('.') so we take em out,
    # since we don't need what's after anyways
    defs = ['"' + d['text'].split(', e.g.')[0].split(', etc')[0].split(
        '\n')[1].split('.')[0] + '"' for d in word['definitions']]
    extra = '' if len(defs) <= 1 else ', or '.join([''] + defs[1:])
    return (
        f'{message} usually means {defs[0]}{extra}'
    )


def post(request, resp):
    return pu.post_plain_text(request, resp, pu.bot_auth())
