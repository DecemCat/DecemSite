import tornado.web


class LoginHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        self.render("admin/login.html")

