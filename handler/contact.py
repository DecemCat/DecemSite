__author__ = 'Administrator'
import tornado.web

class ContactHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('contact.html', articles=[])