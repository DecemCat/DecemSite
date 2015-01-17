import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('blog.html', menus=[{'name': 'Index', 'link': '#'}], articles=[], page=None)