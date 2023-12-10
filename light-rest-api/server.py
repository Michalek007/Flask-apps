from gevent.monkey import patch_all; patch_all()
from app import app, deploy_app_views
from app.periodic_tasks import deploy_scheduler
from gevent import pywsgi

server_wsgi = pywsgi.WSGIServer(listener=(tuple(app.config['LISTENER'].values())), application=app)


def run(server):
    return server.serve_forever()


if __name__ == '__main__':
    deploy_app_views()
    deploy_scheduler()
    run(server_wsgi)
