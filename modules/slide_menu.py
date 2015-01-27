__author__ = 'gavin'
import tornado.web
import dao.dbase


class SlideMenuModule(tornado.web.UIModule):
    def __init__(self, handler):
        tornado.web.UIModule.__init__(self, handler)
        connection = dao.dbase.BaseDBSupport()
        self._submenu = connection.db["submenu"]
    def render(self):
        tags = self._submenu.find()
        return self.render_string('module/slideMenu.html', tags = tags)