import tornado.web


class ContactManageHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(ContactManageHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        self.render("admin/edit.html")
