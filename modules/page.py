__author__ = 'gavin'
import tornado.web


class PageModule(tornado.web.UIModule):
    def render(self, page):
        return self.render_string('module/page.html', page=page)