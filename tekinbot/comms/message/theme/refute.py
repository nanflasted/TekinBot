import re

import tekinbot.utils.post as pu
from tekinbot.comms.message.theme import theme
from tekinbot.utils.config import tekin_id


comm_re = re.compile(
    f'{tekin_id} refute:? (theme )?(because )?(?P<reason>.*)',
    flags=re.IGNORECASE,
)


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    reason = match.group('reason')
    return (
        f'{theme.theme}\nthis theme has been refuted'
        ' for the following reason(s):\n'
        f' <@{request["event"]["user"]}>: {reason}'
    )


def post(request, response):
    theme.theme = None
    return pu.post_plain_text(
        request, response, auth=pu.bot_auth(),
        channel='G82FD53CL'
    )
