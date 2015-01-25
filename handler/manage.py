__author__ = 'Administrator'
import tornado.web
import dao.dbase

class ManageHandler(tornado.web.RequestHandler, ):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._submenu = connection.db["submenu"]
        self._blogs = connection.db["blog"]

    def get(self, *args, **kwargs):
        tags = self._submenu.find()
        self.render('manage.html', tags=tags)