__author__ = 'gavin'
import tornado.web


class SpreadModule(tornado.web.UIModule):
    def render(self):
        self.render_string('module/spread.html')