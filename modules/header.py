__author__ = 'gavin'
import tornado.web
import dao.dbase

class HeaderModule(tornado.web.UIModule, dao.dbase.BaseDBSupport):
    def __init__(self, modules):
        dao.dbase.BaseDBSupport.__init__(self)
        tornado.web.UIModule.__init__(self, modules)

    def render(self, index):
        menus = self.db['menu'].find()
        return self.render_string('module/nav.html', menus=menus, index=index)
