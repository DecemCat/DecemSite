import datetime
import json
import urllib2

import pymongo
import tornado.web
import logging
from bson.objectid import ObjectId

import base
import dao.dbase
from const import const

log = logging.getLogger("operation")


class NewBlogHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(NewBlogHandler, self).__init__(application, request, **kwargs)
        dbs = dao.dbase.BaseDBSupport()
        self._tags = dbs.db["tags"]
        self._config = dbs.db["config"]
        self._posts = dbs.db["posts"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        article_id = None
        try:
            article_id = self.get_argument("article_id")
        except tornado.web.MissingArgumentError:
            article_id = None

        post = const.INIT_POST
        if article_id is not None:
            post = self._posts.find_one({"_id": ObjectId(article_id)})

        taglist = []
        tags = self._tags.find({})
        if tags:
            for tag in tags:
                taglist.append(tag["name"])
        self.render("admin/edit.html", post=post, taglist=taglist, dealurl="edit.html")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        body = self.request.body
        data = json.loads(body)
        article_id = data.pop("_id")
        log.info("user %s create or updated article_id %s", self.current_user, article_id)

        tags = data["tags"]
        for tag in tags:
            if self._tags.find({"name": tag}).count() == 0:
                self._tags.insert_one({"name": tag})

        if article_id:
            self._posts.update({"_id": ObjectId(article_id)}, {"$set": data})
        else:
            data["time"] = datetime.datetime.now()
            data["author"] = "Gavin"
            result = self._posts.insert_one(data)
            url = 'http://www.0x12345.com/post/' + str(result.inserted_id) + '.html'
            baidu_url = self._config.find_one({'key': 'config.baidu.url'})['value']
            headers = {'Content-Type': 'text/plain'}
            req = urllib2.Request(baidu_url, url, headers)
            res = urllib2.urlopen(req)
            res.read()
        self.finish({"status": "ok", "redirect": "/manage/post.html"})


class BlogManageHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(BlogManageHandler, self).__init__(application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._post = connection.db["posts"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = self._post.find({}, {"title":1, "time":1, "tags":1}).sort("time", pymongo.DESCENDING)
        self.render("admin/post.html", posts=posts)


class DeleteBlogHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(DeleteBlogHandler, self).__init__(application, request, **kwargs)
        self._posts = dao.dbase.BaseDBSupport().db["posts"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        if self.request.arguments.has_key("article_id"):
            article_id = self.get_argument("article_id")
            log.info("user %s delete article_id %s", self.current_user, article_id)
            self._posts.delete_one({"_id": ObjectId(article_id)})
        self.redirect("/manage/post.html")
