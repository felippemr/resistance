# coding: utf-8
import tornado.ioloop
import tornado.web
from urls import URLS
from settings import get_app_settings, APP_PORT


def make_app():
    return tornado.web.Application(
        URLS, **get_app_settings()
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(APP_PORT)
    tornado.ioloop.IOLoop.current().start()
    tornado.ioloop.set_blocking_log_threshold(0.50)
