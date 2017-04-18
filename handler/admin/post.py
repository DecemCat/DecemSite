import pymongo
import tornado.web
import datetime
import json

import dao.dbase
import base
import const


class NewBlogHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(NewBlogHandler, self).__init__(application, request, **kwargs)
        dbs = dao.dbase.BaseDBSupport()
        self._tags = dbs.db["tags"]
        self._posts = dbs.db["posts"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        taglist = []
        tags = self._tags.find({})
        if tags:
            for tag in tags:
                taglist.append(tag["name"])
        self.render("admin/edit.html", post=const.INIT_POST, taglist=taglist, dealurl="new.html")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        body = self.request.body
        data = json.loads(body)
        data["author"] = "Gavin"
        data["time"] = datetime.datetime.now()

        tags = data["tags"]
        for tag in tags:
            if self._tags.find({"name": tag}).count() == 0:
                self._tags.insert_one({"name": tag})

        result = self._posts.insert_one(data)
        self.finish({"status": "ok", "redirect": ""})


class BlogManageHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(BlogManageHandler, self).__init__(application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._post = connection.db["posts"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = self._post.find({}, {"title":1, "time":1, "tags":1}).sort("time", pymongo.DESCENDING)
        self.render("admin/post.html", posts=posts)
