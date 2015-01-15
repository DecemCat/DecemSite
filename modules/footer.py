__author__ = 'gavin'
import tornado.web


class FooterModule(tornado.web.UIModule):
    def render(self):
        self.render_string('module/footer.html')