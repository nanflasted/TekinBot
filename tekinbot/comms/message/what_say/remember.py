import re

import tekinbot.utils.post as pu
from tekinbot.db.models.what_say import WhatSay
from tekinbot.utils.config import tekin_id
from tekinbot.utils.db import get_session


aux_verbs = 'is|are|was|were|be|am'
comm_re = re.compile(
    f'{tekin_id} remember that (?P<subject>[\w\ \']+?) '
    f'(?P<description>({aux_verbs}) .*)',
    flags=re.IGNORECASE,
)


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    subject = match.group('subject') or ''
    description = match.group('description') or 'nothing'

    if not subject:  # somehow
        return f'Hold up, what is {description} now?'

    sesh = get_session()

    qres = sesh.query(WhatSay).filter_by(subject=subject)
    if not qres.count():
        sesh.add(WhatSay(subject=subject, description=description))
    else:
        qres.update({'description': description})
    sesh.commit()
    sesh.close()

    return (
        ':k:, understood: \n'
        f'{subject} {description}. \n'
        ':this::tbh:'
    )


def post(request, resp):
    pu.post_plain_text(request, resp, auth=pu.bot_auth())
