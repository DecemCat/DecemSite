__author__ = 'gavin'
import tornado.web


class CommendModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/commend.html')