import re

import tekinbot.utils.post as pu
from tekinbot.db.models.karma import Karma
from tekinbot.utils.config import tekin_id
from tekinbot.utils.db import get_session


comm_re = re.compile(f'{tekin_id} karma (?P<un>.*)', flags=re.IGNORECASE)
resp_tmpl = '{} has a karma of {}, and gave out {} amount of karma.'


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    un = match.group('un')
    sesh = get_session()
    qres = sesh.query(Karma).filter_by(user=un)
    return resp_tmpl.format(un, 0, 0) if not qres.count() else (
        resp_tmpl.format(un, qres.value('received'), qres.value('sent'))
    )
    sesh.close()


def post(request, resp):
    pu.post_plain_text(request, resp, auth=pu.bot_auth())
