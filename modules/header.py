__author__ = 'gavin'
import tornado.web


class HeaderModule(tornado.web.UIModule):

    def render(self, heading, subheading):
        return self.render_string('module/header.html', heading=heading, subheading=subheading)
