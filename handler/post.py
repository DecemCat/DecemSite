import threading

import bson.errors
import tornado.escape
import tornado.web

import dao.dbase
import list

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
        self.render('post.html', post=blogs[0])
