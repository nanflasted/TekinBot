import json
import threading
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response

import tekinbot.comms as comms
import tekinbot.utils.db as du


def async_execute(req):
    result = comms.process(req)
    comms.post(req, result)


def main(request):
    try:
        try:
            req = json.loads(request.body, encoding=request.charset)
            print(req)
            # handle slack api's challenge
            if 'challenge' in req:
                return Response(req['challenge'], 200)
        except Exception as json_e:
            print(str(json_e))
            return Response(f'failed:{str(json_e)}', 400)
        # cheap threading solution: we don't need multiprocessing
        # because this is not computationally intensive
        exec_thread = threading.Thread(target=async_execute, args=(req,))
        exec_thread.start()
        return Response('Received', 200)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    du.tekin_db_init()
    with Configurator() as config:
        config.add_route('main', '/')
        config.add_view(main, route_name='main')
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 9338, app)
    server.serve_forever()
