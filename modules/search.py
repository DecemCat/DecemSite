__author__ = 'gavin'
import tornado.web


class SearchModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('module/search.html')
