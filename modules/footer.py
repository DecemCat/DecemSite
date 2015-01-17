__author__ = 'gavin'
import tornado.web


class FooterModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/footer.html')