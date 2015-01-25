__author__ = 'Administrator'
import tornado.web

class AboutHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('about.html', articles=[])