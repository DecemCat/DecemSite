__author__ = 'gavin'
import tornado.web


class InfoModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/info.html')