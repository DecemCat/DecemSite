__author__ = 'gavin'
import tornado.web


class TagModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/tags.html')