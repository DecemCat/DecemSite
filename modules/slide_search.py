__author__ = 'gavin'
import tornado.web


class SlideSearchModule(tornado.web.UIModule):
    def render(self):
        self.render_string('module/slideSearch.html')