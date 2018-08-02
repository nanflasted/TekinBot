import importlib
import json
import re


__all__ = [
    'define',
    'echo',
    'foaas',
    'roll',
    'what_is',
    'searching.youtube', 'searching.pic', 'searching.scryfall',
    'karma.inc', 'karma.check',
    'theme.theme', 'theme.check', 'theme.refute',
]


comms_dict = {}


def _warn_bork_comm(m, attr):

    # TODO: better warning
    print(f'comm {m.__name__} is borken: lacking {attr}, pls fix')


def process(request):
    # return responses, in tuples: (regex_obj, response)
    # responses are always in a list, if empty list, no response
    resps = []
    print(comms_dict.keys())
    for r in comms_dict:
        try:
            if re.match(r, request['event']['text']):
                resps.append((r, comms_dict[r].process(request)))
        except Exception as e:
            print(e)
    return resps


def post(request, resps):
    post_resps = []
    for reg, resp in resps:
        try:
            post_resps.append(comms_dict[reg].post(request, resp))
        except Exception as e:
            print(e)
    try:
        if bool([p for p in post_resps if (
            p is not None and not json.loads(p.text)['ok']
        )]):
            print('some posting failed')
            return False
    except Exception as e:
        print(e)
        return False
    return True


for v in __all__:
    try:
        m = importlib.import_module(f'tekinbot.comms.message.{v}')
        comms_dict[m.comm_re] = m
    except ModuleNotFoundError:
        print(
            f'message command {v} defined but not implemented'
        )
    except AttributeError as ae:
        _warn_bork_comm(m, 'comm_re')
        print(ae)
    except re.error:
        print(f'comm {v} has an invalid regex')
    except Exception as e:
        print(e)
