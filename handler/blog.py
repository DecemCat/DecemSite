import tornado.web
import tornado.escape
import dao.dbase
import pymongo
import const
import bson.errors
import utils
import threading
import datetime

comment_lock = threading.RLock()
from utils import RequestHandler
from bson import ObjectId
class BlogHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._blog = connection.db["blog"]

    def get(self, *args, **kwargs):
        page = RequestHandler.get_argument(self, 'p', 1)
        type = RequestHandler.get_argument(self, 'type', 0)
        page = int(page)

        start = (page - 1) * const.PAGE_SIZE
        articles = self._blog.find({'type': 0}).sort("create_time", pymongo.DESCENDING).skip(start).limit(const.PAGE_SIZE)
        count = self._blog.find({'type': 0}).count()
        total_size = count / const.PAGE_SIZE
        remainder = count % const.PAGE_SIZE
        if remainder != 0:
            total_size = total_size + 1
        self.render('blog.html', articles=articles, page={"currentPage": page-1, "totalCount": total_size}, index=1)

class BlogDetailHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._blog = connection.db["blog"]
        self._posts = connection.db["posts"]

    def get(self, blog_id):
        try:
            objid = ObjectId(blog_id)
        except bson.errors.InvalidId:
            raise tornado.web.HTTPError(404)

        blogs = self._blog.find({'_id': ObjectId(blog_id)})
        if blogs.count() == 0:
            raise tornado.web.HTTPError(404)
        posts = self._posts.find({"article_id": blog_id})
        self.render('blog_detail.html', blog=blogs[0], index=1, posts=posts)

    def post(self, blog_id):
        author = utils.RequestHandler.get_argument(self, "author")
        email = utils.RequestHandler.get_argument(self, "email")
        content = utils.RequestHandler.get_argument(self, "content")

        _id = None
        try:
            _id = ObjectId(blog_id)
        except:
            raise tornado.web.HTTPError(400)

        comment_lock.acquire()
        blogs = self._blog.find({"_id": _id})
        if blogs is None or blogs.count() == 0:
            comment_lock.release()
            raise tornado.web.HTTPError(400)

        comments = blogs[0]['comments']
        comments += 1
        self._blog.update({"_id": blogs[0]["_id"]}, {'$set': {"comments": comments}})
        comment_lock.release()

        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        self._posts.insert({"article_id": blog_id, "author": author, "email": email, "content": content, "floor": comments, "post_time": current_date})


