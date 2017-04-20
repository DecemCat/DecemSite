__author__ = 'gavin'
import tornado.web


class NavModule(tornado.web.UIModule):
    def render(self, keyword):
        return self.render_string('module/nav.html', keyword=keyword)


class AdminNavModule(tornado.web.UIModule):
    def render(self, index):
        return self.render_string('module/adminnav.html', index=index)
