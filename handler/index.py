import tornado.web
import dao.dbase
import pymongo

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        connection = dao.dbase.BaseDBSupport()
        blogs = connection.db["blog"].find({"type": 0}).sort("update_time", pymongo.DESCENDING).limit(10)
        lives = connection.db["blog"].find({"type": 1}).sort("update_time", pymongo.DESCENDING).limit(10)
        self.render('index.html', blogs=blogs, lives=lives)