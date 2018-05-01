import argparse
import json
import threading

from pyramid.config import Configurator
from pyramid.response import Response

import tekinbot.comms as comms
import tekinbot.utils.db as du
from tekinbot.utils.post import deploy_view


def tekin_args():
    parser = argparse.ArgumentParser(
        description='TekinBot Server'
    )
    parser.add_argument(
        '--dry-run', dest='dry_run', action='store_true',
        help=('set up Tekin for dry running; Tekin will print all '
              'posting actions to stdout, instead of sending Requests'
              ),
    )
    parser.add_argument(
        '--no-db', dest='nodb', action='store_true',
        help=('tekin will not read or write anything to database, '
              'everything will be performed either in a dry run fashion '
              'or in memory'
              ),
    )
    parser.add_argument(
        '--port', dest='port', type=int,
        default=9340, help='the port which tekin listens to',
    )
    return parser.parse_args()


def async_execute(req, dry_run=False):
    result = comms.process(req)
    if dry_run:
        print(result)
    else:
        comms.post(req, result)


def dry_main(request):
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
        exec_thread = threading.Thread(target=async_execute, args=(req, True))
        exec_thread.start()
        return Response('Received', 200)
    except Exception as e:
        print(str(e))


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
        exec_thread = threading.Thread(target=async_execute, args=(req, False))
        exec_thread.start()
        return Response('Received', 200)
    except Exception as e:
        print(str(e))


def create_application(dry_run=False, nodb=False):
    du.tekin_db_init(nodb)
    with Configurator() as config:
        config.add_route('main', '/')
        config.add_view(dry_main if dry_run else main, route_name='main')
        config.add_route('deploy', '/deploy')
        config.add_view(deploy_view, route_name="deploy")
        return config.make_wsgi_app()


wsgi_app = create_application()


if __name__ == '__main__':
    args = tekin_args()
    app = create_application(args.dry_run, args.nodb)
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', args.port, app)
    server.serve_forever()
