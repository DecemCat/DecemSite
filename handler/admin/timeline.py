import tornado.web
from bson.objectid import ObjectId

import const
import dao.dbase
import base

class TimelineHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(TimelineHandler, self).__init__(application, request, **kwargs)
        self._timeline = dao.dbase.BaseDBSupport().db["timeline"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        timelines = self._timeline.find({})
        self.render("admin/timeline.html", timelines=timelines)


class AddTimelineHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(AddTimelineHandler, self).__init__(application, request, **kwargs)
        self._timeline = dao.dbase.BaseDBSupport().db["timeline"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        timeline = const.INIT_TIMELINE
        tmid = None
        if self.request.arguments.has_key("id"):
            tmid = self.get_argument("id")

        if tmid:
            timeline = self._timeline.find_one({"_id": ObjectId(tmid)})

        self.render("admin/addline.html", timeline=timeline)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        tmid = self.get_argument("_id")
        headline = self.get_argument("headline")
        startDate = self.get_argument("startDate")
        endDate = self.get_argument("endDate")
        text = self.get_argument("text")
        media = self.get_argument("media")
        credit = self.get_argument("credit")
        caption = self.get_argument("caption")
        timeline = {"headline": headline, "startDate": startDate, "endDate": endDate, "text": text, "asset": {"media": media, "credit": credit, "caption": caption}}
        if tmid:
            self._timeline.update({"_id": ObjectId(tmid)}, {"$set": timeline})
        else:
            self._timeline.insert(timeline)

        self.redirect("/manage/life.html")

class DelTimelineHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(DelTimelineHandler, self).__init__(application, request, **kwargs)
        self._timeline = dao.dbase.BaseDBSupport().db["timeline"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        tmid = self.get_argument("id")
        if tmid:
            self._timeline.delte_one({"_id": ObjectId(tmid)})

        self.redirect("/manage/life.html")
