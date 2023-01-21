from flask import Flask
from redis.client import Redis


def main():
    from .config import load_config
    config = load_config()

    from .tonapi import Tonapi
    tonapi = Tonapi(config.TONAPI_KEY)

    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB
    )

    app = Flask(__name__)
    app.config["redis"] = redis
    app.config["tonapi"] = tonapi

    from . import views
    views.register(app)

    from gevent.pywsgi import WSGIServer
    server = WSGIServer(('', 5000), app)
    server.serve_forever()


if __name__ == '__main__':
    main()
