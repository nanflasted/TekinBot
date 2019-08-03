import re

import tekinbot.utils.post as pu
from tekinbot.db.models.what_say import WhatSay
from tekinbot.utils.config import tekin_id
from tekinbot.utils.db import get_session

comm_re = re.compile(
    f'{tekin_id} what can you say about (?P<subject>[\w\ \']+)($|\W*)',
    flags=re.IGNORECASE
)


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    subj = str(match.group('subject') or '').lower()

    sesh = get_session()

    qres = sesh.query(WhatSay).filter_by(subject=subj)
    if not qres.count():
        return f'It is {subj}.'
    description = qres.value('description')
    return f'{subj} {description}'


def post(request, resp):
    pu.post_plain_text(request, resp, auth=pu.bot_auth())
