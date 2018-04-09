import re

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(f'^{tekin_id} echo (?P<message>.*)$', flags=re.IGNORECASE)


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    message = match.group('message')
    return message


def post(request, resp):
    return pu.post_plain_text(request, resp, pu.bot_auth())
