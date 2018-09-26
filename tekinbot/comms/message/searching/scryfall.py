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
scryfall_favicon = 'https://assets.scryfall.com/favicon.ico'
mtg_colours = {
    'W': '#F8E7B9',
    'U': '#B3CEEA',
    'B': '#A69F9D',
    'R': '#EA9F82',
    'G': '#C4D3CA',
    'C': '#FFFFFF',
}


def search(query, exact):
    search_payload = {"exact" if exact else "fuzzy": query}
    search_resp = requests.get(
        link_stem, params=search_payload
    )

    if search_resp.status_code == 404:
        return {'text': (
            'Can\'t find the said card, or there are multiple matches. '
            'Try to be more precise. Anyway, here is me in the Multiverse: '
            f'{tekin_planeswalker}'
        )}
    elif not search_resp.ok:
        return {'text': 'I can\'t into internetz'}

    try:
        resp = search_resp.json()

        text = (
            f'I did a scry 1 and found {resp["name"]} based on the search '
            f'query:\n{resp["scryfall_uri"]}.\nTry to be more '
            'precise if this is not it.'
        )

        colour = resp.get('color_identity')
        colour = 'C' if not colour else colour[0]

        attachment = {
            'fallback': text,
            'author_name': 'Scryfall:TM: brought to you by Tekin',
            'author_link': f'{resp["scryfall_uri"]}',
            'author_icon': f'{scryfall_favicon}',
            'pretext': f'I did a scry 1 and found {resp["name"]}',
            'image_url': (
                '{url}'.format(url=resp["image_uris"]["normal"])
            ) if resp["layout"] != "transform" else (
                '\n'.join([
                    face['image_uris']['normal'] for face in resp['card_faces']
                ])
            ),
            'color': mtg_colours[colour],
            'fields': [
                {'title': 'Name', 'value': f'{resp["name"]}', 'short': True},
                {'title': 'Mana', 'value': '{}'.format(
                    resp["mana_cost"] if resp['layout'] != 'transform' else (
                        ' // '.join([face['mana_cost']
                                     for face in resp['card_faces']])
                    )), 'short': True},
                {'title': 'Type Line',
                    'value': f'{resp["type_line"]}', 'short': True},
                {'title': 'Set', 'value': f'{resp["set"]}', 'short': True},
                {'title': 'Text', 'value': '{}'.format(
                    resp['oracle_text'] if resp['layout'] == 'normal' else (
                        '\n'.join([face['oracle_text']
                                   for face in resp['card_faces']])
                    )
                )}
            ]
        }
        return {'attachments': [attachment]}

    except Exception as e:
        print(e)
        return {'text': 'Can\'t find the said card.'}


def process(request):
    match = re.fullmatch(comm_re, request['event']['text'])
    query = match.group('query') or match.group('query_bk')
    exact = bool(match.group('exact') or match.group('exact_bk'))

    if not query:
        return {'text': 'What exactly are you looking for?'}

    return search(query, exact)


def post(request, resp):
    return pu.post_formatted_text(request, resp, auth=pu.bot_auth())
