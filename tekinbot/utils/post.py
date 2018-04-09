import json

import requests

from tekinbot.utils.config import tekin_secrets


def dunno():
    return 'Not sure if I understood that'


def app_auth():
    return tekin_secrets('slack.app_auth')


def bot_auth():
    return tekin_secrets('slack.bot_auth')


def json_header(auth):
    return {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {auth}',
    }


def post_plain_text(request, resp, auth, channel=None):
    headers = json_header(auth)
    content = {
        'channel': channel or request['event']['channel'],
        'text': resp,
        'as_user': False,
    }
    post_resp = requests.post(
        'https://slack.com/api/chat.postMessage',
        headers=headers,
        data=json.dumps(content),
    )
    return post_resp
