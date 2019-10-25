import random
import re
import time

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(f'^{tekin_id} choose (?P<message>.*)$', flags=re.IGNORECASE)

def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    message = match.group('message')
    choices = message.split(",")
    num_ch = len(choices)

    if num_ch > 0:
      chosen = choices[random.randInt(num_ch)].strip()
      if chosen[:3] == "or ":
        chosen = chosen[3:].strip()
      return f'I am {100/num_ch + max([random.randint(0, 100-(100/num_ch)) for i in range(num_ch)])}% sure you should choose {chosen}.'

    else:
      return "There is nothing to choose"


def post(request, resp):
    return pu.post_plain_text(request, resp, pu.bot_auth())