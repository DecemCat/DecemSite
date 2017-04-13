import tornado.web
import dao.dbase
import pymongo

class IndexHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request,
                **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._blog = connection.db["blog"]
    @tornado.web.asynchronous
    def get(self):
        articles = self._blog.find({'index',1}).sort('lastUpdated',
                pymongo.DESCENDING)
        if articles is None:
            articles = {}
        self.render('index.html', articles=articles)
