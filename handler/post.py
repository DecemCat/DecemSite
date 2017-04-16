import datetime
import threading

import bson.errors
import pymongo
import tornado.escape
import tornado.web

import const
import dao.dbase

comment_lock = threading.RLock()
from bson import ObjectId


class BlogHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._posts = connection.db["posts"]

    def get(self, blog_id):
        try:
            objid = ObjectId(blog_id)
        except bson.errors.InvalidId:
            raise tornado.web.HTTPError(404)

        blogs = self._posts.find({'_id': ObjectId(blog_id)})
        if blogs.count() == 0:
            raise tornado.web.HTTPError(404)
        posts = self._posts.find({"article_id": blog_id})
        self.render('post.html', blog=blogs[0], index=1, posts=posts)
