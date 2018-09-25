import json
import subprocess

import requests
from pyramid.response import Response

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


def post_formatted_text(request, resp, auth, channel=None):
    headers = json_header(auth)
    content = {
        'channel': channel or request['event']['channel'],
        'as_user': False,
    }
    content.update(**resp)
    post_resp = requests.post(
        'https://slack.com/api/chat.postMessage',
        headers=headers,
        data=json.dumps(content),
    )
    return post_resp


def deploy_view(request):
    new_commit = subprocess.check_output(['git', 'rev-parse', 'master'])
    new_commit = new_commit.decode('utf-8').split('\n')[0]
    new_commit_msg = subprocess.check_output(
        ['git', 'log', '-1', '--pretty=%B'])
    new_commit_msg = new_commit_msg.decode('utf-8')

    deploy_channel = tekin_secrets('slack.deploy_channel')
    if not deploy_channel:
        return Response('deploy channel not configured, deploy not announced')
    deploy_message = (
        f'New commit new :tekin:! \n'
        f'A new version (SHA: {new_commit}) of TekinBot was just deployed! \n'
        f'The new version consists of the following changes: \n'
        f'{new_commit_msg}'
    )
    post_plain_text(
        request,
        deploy_message,
        app_auth(),
        channel=deploy_channel,
    )
    return Response()
