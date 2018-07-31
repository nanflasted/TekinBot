import functools
import re

import wikipedia
from wikipedia import DisambiguationError

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id


comm_re = re.compile(f'^{tekin_id} (what|who) is (?P<message>.*)$', re.IGNORECASE)


@functools.lru_cache()
def search_and_cache(message):
    try:
        return wikipedia.page(message), []
    except DisambiguationError as e:
        return wikipedia.page(e.options[0]), e.options[1:]


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    message = match.group('message')
    if not wikipedia.search(message):
        return f'I can\'t possibly know what {message} is'

    page, disambi = search_and_cache(message)
    if len(disambi) > 5:
        disambi = disambi[:4]
    disambi = '' if not disambi else ', '.join(
        disambi[:-1]) + ' or ' + disambi[-1]
    summary = page.summary.split('. ')[0]
    if not disambi:
        return f'{summary}, see {page.url} for more'
    else:
        return (f'assuming {message} means {page.title}, {summary}\n'
                f'see {page.url} for more\n'
                f'try asking about {disambi} if that\'s not it'
                )


def post(request, resp):
    return pu.post_plain_text(request, resp, pu.bot_auth())
