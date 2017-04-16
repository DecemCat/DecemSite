__author__ = 'Administrator'
import tornado.web

import base
import dao.dbase


class AdminHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._login = connection.db["login"]
        self._submenu = connection.db["submenu"]

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/admin.html')
