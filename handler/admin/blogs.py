import tornado.web


class BlogManageHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BlogManageHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        self.render("admin/blogs.html")
