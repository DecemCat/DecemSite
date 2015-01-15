__author__ = 'gavin'
import tornado.web


class SlideArchiveModule(tornado.web.UIModule):
    def render(self):
        self.render_string('module/slideArchive.html')