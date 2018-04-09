import functools
import os

import yaml


TEKIN_SECRET_FILE = os.path.expanduser('~/.tekin-secrets.yaml')

tekin_id = '<@U12345678>'


@functools.lru_cache()
def tekin_secret_dict():
    with open(TEKIN_SECRET_FILE) as f:
        tekin_secret_dict = yaml.safe_load(f)
    return tekin_secret_dict


def tekin_secrets(key_name):
    key_seq = key_name.split('.')
    v = tekin_secret_dict()
    for k in key_seq:
        try:
            v = v[k]
        except KeyError:
            raise KeyError(f'key {key_name} is not found in Tekin\'s secrets')
    return v
