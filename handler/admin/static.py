__author__ = 'gavin'
import datetime
import logging

import tornado.web

import base
import dao.dbase
from const import const

log = logging.getLogger("operation")


class AboutMgrHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(AboutMgrHandler, self).__init__(application, request, **kwargs)
        self._static = dao.dbase.BaseDBSupport().db["static"]
        self._config = dao.dbase.BaseDBSupport().db["config"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        init_dict = const.INIT_STATIC.copy()
        init_dict.update({"type": "about"})
        static = self._static.find_one({"type":"about"}) or init_dict
        introduce = self._config.find_one({"key": "info.introduce"})["value"]
        self.render("admin/static.html", static=static, introduce=introduce)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        title = self.get_body_argument("title")
        content = self.get_body_argument("content")
        introduce = self.get_body_argument("introduce")
        if not title or not content:
            self.finish({"status": "fail"})

        log.info("user %s updated the about pages", self.current_user)
        time = datetime.datetime.now()
        self._static.update({"type": "about"}, {"$set": {"title": title, "content": content, "time": time, "type": "about"}}, upsert=True)
        self._config.update({"key": "info.introduce"}, {"$set": {"value": introduce}})
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
        log.info("user %s updated the life pages", self.current_user)
        self._static.update({"type": "life"}, {"$set": {"title": title, "content": content, "time": time, "type": "life"}}, upsert=True)
        self.finish({"status": "ok", "redirect": "/life.html"})
