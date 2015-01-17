__author__ = 'gavin'
import tornado.web


class SlideMenuModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/slideMenu.html')