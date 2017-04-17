import tornado.web
import dao.dbase
import pymongo

class IndexHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request,
                **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._blog = connection.db["posts"]
    @tornado.web.asynchronous
    def get(self):
        posts = self._blog.find({}).sort('time', pymongo.DESCENDING)
        if posts is None:
            posts = {}
        self.render('index.html', posts=posts)
