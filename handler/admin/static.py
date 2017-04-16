__author__ = 'gavin'
import tornado.web
import datetime

import const
import dao.dbase
import base


class AboutMgrHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(AboutMgrHandler, self).__init__(application, request, **kwargs)
        self._static = dao.dbase.BaseDBSupport().db["static"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        init_dict = const.INIT_STATIC.copy()
        init_dict.update({"type": "about"})
        static = self._static.find_one({"type":"about"}) or init_dict
        self.render("admin/static.html", static=static)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        titles = self.get_body_arguments("title")
        contents = self.get_body_arguments("content")
        if not titles or not contents:
            self.finish({"status": "fail"})

        title = titles[0]
        content = contents[0]
        time = datetime.datetime.now()
        self._static.update({"type": "about"}, {"$set": {"title": title, "content": content, "time": time, "type": "about"}}, upsert=True)
        self.finish({"status": "ok", "redirect": "/about.html"})


class LifeMgrHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(LifeMgrHandler, self).__init__(application, request, **kwargs)
        self._static = dao.dbase.BaseDBSupport().db["static"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        init_dict = const.INIT_STATIC.copy()
        init_dict.update({"type": "life"})
        static = self._static.find_one({"type":"live"}) or init_dict
        self.render("admin/static.html", static=static)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        titles = self.get_body_arguments("title")
        contents = self.get_body_arguments("content")
        if not titles or not contents:
            self.finish({"status": "fail"})

        title = titles[0]
        content = contents[0]
        time = datetime.datetime.now()
        self._static.update({"type": "life"}, {"$set": {"title": title, "content": content, "time": time, "type": "life"}}, upsert=True)
        self.finish({"status": "ok", "redirect": "/life.html"})
