import functools
import os

import yaml


TEKIN_SECRET_FILE = os.path.expanduser('~/.tekin-secrets.yaml')

tekin_id = '<@U12345678>'


@functools.lru_cache()
def tekin_secret_dict():
    try:
        with open(TEKIN_SECRET_FILE) as f:
            tekin_secret_dict = yaml.safe_load(f)
        return tekin_secret_dict
    except FileNotFoundError:
        print('Tekin\'s secrets file not found!')
        return {}


def tekin_secrets(key_name):
    key_seq = key_name.split('.')
    v = tekin_secret_dict()
    for k in key_seq:
        v.get(key_name)
        if not v:
            return ''
    return v
