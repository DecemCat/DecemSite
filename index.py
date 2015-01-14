import tornado.web
import dao.dbase

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        dbs = dao.dbase.BaseDBSupport()
        dbs.find('test', user='zhaohongwei')