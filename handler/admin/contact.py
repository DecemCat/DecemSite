import tornado.web
import base


class ContactManageHandler(base.BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(ContactManageHandler, self).__init__(application, request, **kwargs)

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("admin/edit.html")
