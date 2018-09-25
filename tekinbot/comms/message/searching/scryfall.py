import re

import requests

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id


comm_re = re.compile(
    f'(^{tekin_id} :?(mtg me|mtg)'
    f'(?P<exact> exactly|)(: |:| )(?P<query>.*)$|'
    f'^.*\[\[(?P<exact_bk>!)?(?P<query_bk>.*)\]\].*$)',
    flags=re.IGNORECASE
)


link_stem = 'https://api.scryfall.com/cards/named'
tekin_planeswalker = 'https://i.imgur.com/9agLW68.png'


def search(query, exact):
    search_payload = {"exact" if exact else "fuzzy": query}
    search_resp = requests.get(
        link_stem, params=search_payload
    )

    if search_resp.status_code == 404:
        return (
            'Can\'t find the said card, or there are multiple matches. '
            'Try to be more precise. Anyway, here is me in the Multiverse: '
            f'{tekin_planeswalker}'
        )
    elif not search_resp.ok:
        return 'I can\'t into internetz'

    try:
        resp = search_resp.json()
        return (
            f'I did a scry 1 and found {resp["name"]} based on the search '
            f'query:\n{resp["image_uris"]["large"]}. Try to be more '
            'precise if this is not it.'
        )
    except Exception as e:
        print(e)
        return 'Can\'t find the said card.'


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    query = match.group('query') or match.group('query_bk')
    exact = bool(match.group('exact') or match.group('exact_bk'))

    if not query:
        return 'What exactly are you looking for?'

    return search(query, exact)


def post(request, resp):
    return pu.post_plain_text(request, resp, auth=pu.bot_auth())
