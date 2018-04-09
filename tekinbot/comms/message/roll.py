import random
import re
import time

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id


comm_re = f'{tekin_id} roll (?P<num_d>[\d]+) ?d(?P<d_type>[\d]+).*'
random.seed(time.time())


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    num_d = int(match.group('num_d'))
    d_type = int(match.group('d_type'))

    if num_d > 100:
        return 'Ehh I don\'t have this many dice to roll; I\'ve only got :100:'

    rolls = [random.randint(1, d_type) for i in range(num_d)]
    return f'Here\'s the roll: {rolls}'


def post(request, response):
    return pu.post_plain_text(request, response, auth=pu.bot_auth())
