__author__ = 'gavin'
import tornado.web
import dao.dbase
import const


class AboutHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(AboutHandler, self).__init__(application, request, **kwargs)
        self._static = dao.dbase.BaseDBSupport().db["static"]

    def get(self, *args, **kwargs):
        init_dict = const.INIT_STATIC.copy()
        init_dict.update({"type": "about"})
        static = self._static.find_one({"type":"about"}) or init_dict
        self.render("static.html", static=static)


class LifeHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LifeHandler, self).__init__(application, request, **kwargs)
        self._static = dao.dbase.BaseDBSupport().db["static"]

    def get(self, *args, **kwargs):
        init_dict = const.INIT_STATIC.copy()
        init_dict.update({"type": "life"})
        static = self._static.find_one({"type":"life"}) or init_dict
        self.render("static.html", static=static)
