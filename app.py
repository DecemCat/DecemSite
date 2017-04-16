import os
import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import const
import importlib

from config import ConfigReader


def convert_arr(handlers):
    last_arr = []
    for handler in handlers:
        hans = handler[1].split(":")
        last_arr.append((handler[0], getattr(importlib.import_module(hans[0]), hans[1])))
    last_arr.append((r'/favicon.ico', tornado.web.StaticFileHandler, {"path":""}))
    return last_arr


def convert_dict(modules):
    last_dict = {}
    for (key, value) in modules.items():
        hans = value.split(":")
        last_dict[key] = getattr(importlib.import_module(hans[0]), hans[1])
    return last_dict


if __name__ == '__main__':
    cr = ConfigReader()
    handlers = cr.readAll(const.HANDLER_CONF, const.HANDLER_SECTION)
    modules = cr.readAsDic(const.MODULE_CONF, const.UIMODULE_SECTION)

    app = tornado.web.Application(
        handlers=convert_arr(handlers),
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        ui_modules=convert_dict(modules),
        cookie_secret=os.urandom(10),
        login_url="/login.html"
    )
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(cr.read(const.SERVER_CONF, const.SERVER_SECTION, const.SERVER_PORT))
    tornado.ioloop.IOLoop.instance().start()
