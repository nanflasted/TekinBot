import random
import re

import requests

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(
    f'{tekin_id} tell (?P<target1>.*) to f[uv]ck off|'
    '.*f[uv]ck( you| off),? (?P<target>[\w| \']*).*',
    flags=re.IGNORECASE
)


accepted_tmpls = [
    [
        {'name': 'Company', 'field': 'company'},
        {'name': 'From', 'field': 'from'}
    ],
    [{'name': 'From', 'field': 'from'}],
    [{'name': 'Name', 'field': 'name'}, {'name': 'From', 'field': 'from'}],
]
url_stem = 'https://www.foaas.com{}'
url_tmpl = [o['url'] for o in (
    requests.get(url_stem.format('/operations')).json()
) if any(
    [t == o['fields'] for t in accepted_tmpls]
)
]
header = {'Accept': 'application/json'}
add_name_tmpl = ['yo {target}: {msg}', '{target}, {msg}']


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    target = match.group('target') or match.group('target1')
    if not target:
        return ''
    url = url_stem.format(random.choice(url_tmpl))
    add_name = not re.search('(name|company)', url)
    url = re.sub(r'(:name|:company)', target, url)
    url = re.sub(r':from', 'tekin', url)
    msg = requests.get(url, headers=header).json()['message']
    return random.choice(add_name_tmpl).format(
        target=target, msg=msg
    ) if add_name else msg


def post(request, resp):
    return pu.post_plain_text(request, resp, auth=pu.bot_auth())
