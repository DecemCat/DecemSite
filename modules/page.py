__author__ = 'gavin'
import tornado.web


class PageModule(tornado.web.UIModule):
    def render(self, page, index):
        link = ""
        if index == 1:
            link = "blog.html"
        else:
            link = "life.html"
        return self.render_string('module/page.html', page=page, link=link)