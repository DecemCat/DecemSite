import pymongo
import tornado.web

import dao.dbase
import base


class NewBlogHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(NewBlogHandler, self).__init__(application, request, **kwargs)

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("admin/edit.html", tags=["Java", "C++"], taglist=["aaaa", "Python"])


class BlogManageHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(BlogManageHandler, self).__init__(application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._post = connection.db["posts"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = self._post.find({}, {"title":1, "time":1, "tags":1}).sort("time", pymongo.DESCENDING)
        self.render("admin/post.html", posts=posts)
