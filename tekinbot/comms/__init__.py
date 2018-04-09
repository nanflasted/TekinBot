import importlib
# from pyramid.response import Response
# import sys: TODO print the errors to stderr

__all__ = [
    'message',
    #    'member_joined_channel',
    #    'member_left_channel',
]


comms_dict = {}


def process(request):

    if 'username' in request['event'] and (
        request['event']['username'] == 'TekinBot'
    ):
        return ''
    req_type = request['event']['type']
    try:
        return comms_dict[req_type].process(request)
    except KeyError:
        print(
            f'the commands for event type {req_type} are not implemented',
            204
        )


def post(request, resps):

    req_type = request['event']['type']
    try:
        return comms_dict[req_type].post(request, resps)
    except KeyError:
        print(
            f'the commands for event type {req_type} are not implemented',
            204
        )


for v in __all__:
    try:
        m = importlib.import_module(f'tekinbot.comms.{v}')
        comms_dict[v] = m
    except ModuleNotFoundError:
        # fixme: handle this better, e.g.,
        # raise NotImplementedError(
        print(
            f'event level module {v} defined but not implemented'
        )
    except ImportError:
        print(
            f'event level module {v} found but cannot be imported,'
            f'maybe check dependency?'
        )
    except Exception as e:
        print(e)
