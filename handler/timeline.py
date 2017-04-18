# coding=utf-8
__author__ = 'gavin'
import tornado.web
import dao.dbase
import json


class TimeLineHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(TimeLineHandler, self).__init__(application, request, **kwargs)
        self._timeline = dao.dbase.BaseDBSupport().db["timeline"]
        self._config = dao.dbase.BaseDBSupport().db["config"]

    def get(self, *args, **kwargs):
        timeline = {}
        timeline["headline"] = self._config.find_one({"key": "timeline.headline"})["value"]
        timeline["type"] = "default"
        timeline["text"] = self._config.find_one({"key": "timeline.text"})["value"]
        timeline["startDate"] = self._config.find_one({"key": "timeline.startdate"})["value"]
        dates = []
        sources = self._timeline.find({})
        for source in sources:
            source.pop("_id")
            dates.append(source)

        timeline["date"] = dates
        self.render("timeline.html", source=json.dumps({"timeline": timeline}, ensure_ascii=False))
