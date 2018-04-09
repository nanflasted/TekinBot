import re

import tekinbot.utils.post as pu
from tekinbot.comms.message.theme import theme
from tekinbot.utils.config import tekin_id


comm_re = re.compile(
    f'{tekin_id} post (me )?(the )?(thread )?theme',
    flags=re.IGNORECASE
)


def process(request):
    curr = theme.theme
    if not curr:
        return 'Either there was no theme, or I\'ve forgotten about it'
    return curr


def post(request, response):
    return pu.post_plain_text(request, response, auth=pu.bot_auth())
