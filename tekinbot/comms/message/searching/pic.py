import random
import re

import requests
from bs4 import BeautifulSoup

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id


comm_re = re.compile(
    f'^{tekin_id} :?pic(ture)? (me)?'
    f'(?P<exact> exactly|)(: |:| )(?P<query>.*)$',
    flags=re.IGNORECASE
)

res_stem = 'https://www.google.com/search'

header = {
    'User-Agent': 'Mozilla/5.0 AppleWebKit/534.13 Safari/534.13'
}


def extract_search_res(parsed):
    hrefs = [
        tag.get('href') for tag in parsed.find_all(
            'a'
        ) if (
            u'imgurl' in tag.get('href')
        )][:20]
    hrefs = [
        re.search('imgurl=(?P<url>.+?)(?=&)', h).group('url') for h in hrefs
    ]
    return [h for h in hrefs if bool(h)]


def search(query, exact):
    search_payload = {
        'q': query.encode('utf-8'),
        'hl': 'en',
        'tbm': 'isch',
    }
    search_resp = requests.get(res_stem, params=search_payload, headers=header)

    if not search_resp.ok:
        return 'I can\'t into internetz'
    parsed = BeautifulSoup(search_resp.text, "html.parser")

    # magic
    search_res = extract_search_res(parsed)
    if not search_res:
        return (
            'Somehow, I can\'t find anything; '
            'anyways, here\'s Wonderwall: '
            'https://www.youtube.com/watch?v=bx1Bh8ZvH84'
        )
    return search_res[0] if exact else random.choice(search_res)


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    query = match.group('query')
    exact = bool(match.group('exact'))

    if not query:
        return 'What exactly are you looking for?'

    return search(query, exact)


def post(request, resp):
    return pu.post_plain_text(request, resp, auth=pu.bot_auth())
