import random
import re
import time

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(f'^{tekin_id} choose (?P<message>.*)$', flags=re.IGNORECASE)

def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    message = match.group('message')

    if message:
      choices = message.split(",")
      num_ch = len(choices)
      # Choose an option randomly
      chosen = random.choice(choices).strip()
      # Remove or if needed
      if chosen[:3] == "or ":
        chosen = chosen[3:].strip()
      # Come up with a valid chance
      chance = 100/num_ch + max([
          random.randint(0, 100-(100/num_ch)) for _ in range(num_ch)
        ])
      return f'I am {chance}% sure you should choose {chosen}.'

    else:
      return "There is nothing to choose."


def post(request, resp):
    return pu.post_plain_text(request, resp, pu.bot_auth())