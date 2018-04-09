import re

import tekinbot.utils.post as pu
from tekinbot.comms.message.searching import youtube
from tekinbot.utils.config import tekin_id

comm_re = re.compile(
    f'({tekin_id} )?(set )?thread theme:? ?<?(?P<link>[^>]*)>?',
    flags=re.IGNORECASE
)


theme = None


is_url = re.compile(
    '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?'
    '[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
)


def process(request):
    global theme
    match = re.fullmatch(comm_re, request['event']['text'])
    theme = match.group('link')
    if not re.fullmatch(is_url, theme):
        theme = youtube.search(theme, exact=True)
    return f'OK, thread theme is now {theme}'


def post(request, response):
    return pu.post_plain_text(request, response, auth=pu.bot_auth())
