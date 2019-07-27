
import random
import re
import time
import os

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(f'{tekin_id} tell me a story', flags=re.IGNORECASE)

def process(request):
    return os.system("ruby generate.rb")


def post(request, response):
    return pu.post_plain_text(request, response, auth=pu.bot_auth())