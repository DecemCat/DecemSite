__author__ = 'gavin'
import tornado.web


class NavModule(tornado.web.UIModule):
    def render(self, keyword):
        return self.render_string('module/nav.html', keyword=keyword)