__author__ = 'gavin'
import tornado.web


class SlideSearchModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/slideSearch.html')