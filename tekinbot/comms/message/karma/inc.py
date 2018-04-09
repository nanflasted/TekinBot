import re

from tekinbot.db.models.karma import Karma
from tekinbot.utils.config import tekin_id
from tekinbot.utils.db import get_session


comm_re = re.compile('(?P<target>.*)(\+\+|--)', flags=re.IGNORECASE)


def self_inc_check(match, request):
    return match.group('target') == f"<@{request['event']['user']}>"


def process(request):
    tokens = request['event']['text'].split(' ')
    matches = [re.match(
        '(?P<target>.*)(?P<inc>(\+\+|--))', t
    ) for t in tokens]
    matches = [m for m in matches if m is not None]

    sesh = get_session()

    src = 0
    tf = False
    for m in matches:
        if self_inc_check(m, request):
            continue
        t = m.group('target')
        if t == tekin_id:
            tf = True
        d = 1 if m.group('inc') == '++' else -1
        src += d
        qres = sesh.query(Karma).filter_by(user=t)
        if not qres.count():
            sesh.add(Karma(user=t, sent=0, received=d))
        else:
            qres.update({'received': Karma.received + d})
    src_user = f"<@{request['event']['user']}>"
    qres = sesh.query(Karma).filter_by(user=src_user)
    if not qres.count():
        sesh.add(Karma(user=src_user, sent=src, received=0))
    else:
        qres.update({'sent': Karma.sent + src})
    sesh.commit()
    sesh.close()
    return '/shrug :k:' if tf else ''


def post(request, resp):
    return resp or None
    # FIXME: return an empty resp if possible
