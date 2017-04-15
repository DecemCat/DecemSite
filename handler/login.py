import tornado.web
import string
import random
import dao.dbase
import datetime


class LoginHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        self.render("admin/login.html")

    def post(self, *args, **kwargs):
        pass


class PasswordHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(PasswordHandler, self).__init__(application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._user = connection.db["user"]

    def post(self, *args, **kwargs):
        email = self.get_body_argument("email")
        if email is None:
            return

        email_count = self._user.find({"email": email}).count()
        if email_count == 0:
            return
        password = self._gen_password(10)
        self._user.update({"email": email}, {"$set": {"update": datetime.datetime.now(), "passwd": password}})

    def _gen_password(self, length):
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for i in range(length)])
