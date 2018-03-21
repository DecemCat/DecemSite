import datetime
import hashlib
import random
import string

import tornado.web
import dao.dbase

from handler.commutil.utils import EmailUtils


class LoginHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)
        self._user = dao.dbase.BaseDBSupport().db["user"]

    def get(self, *args, **kwargs):
        self.render("admin/login.html")

    def post(self, *args, **kwargs):
        emails = self.get_body_arguments("user")
        passwds = self.get_body_arguments("passwd")
        if not emails or not passwds:
            self.render("admin/login.html")
            return

        email = emails[0]
        passwd = passwds[0]
        user = self._user.find_one({"email": email})
        if not user:
            self.render("admin/login.html")
            return

        db_passwd = user["passwd"]
        if not db_passwd:
            self.render("admin/login.html")
            return

        passwd = hashlib.sha256(passwd).hexdigest()
        if passwd != db_passwd:
            self.render("admin/login.html")
            return

        user["passwd"] = None
        self._user.update({"email": email}, {"$set": {"update": datetime.datetime.now(), "passwd": None}})

        self.set_secure_cookie("user", email)
        ran = ''.join([random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']) for i in range(16)])
        token = hashlib.sha256(email + self.request.remote_ip).hexdigest() + ran
        self.set_secure_cookie("token", token)
        self._user.update({"email": email}, {"$set": {"token": token}})
        self.redirect("/manage/admin.html")


class LogoutHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LogoutHandler, self).__init__(application, request, **kwargs)
        self._user = dao.dbase.BaseDBSupport().db["user"]

    def get(self, *args, **kwargs):
        email = self.get_secure_cookie("user")
        self.clear_all_cookies()
        self._user.update({"email": email}, {"$set": {"token": ""}})
        self.render("admin/login.html")



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
        password = self._gen_password(20)
        EmailUtils.send_mail([email], "Your password this time!", password)
        password = hashlib.sha256(password).hexdigest()

        self._user.update({"email": email}, {"$set": {"update": datetime.datetime.now(), "passwd": password}})
        self.finish({"status": "ok"})

    def _gen_password(self, length):
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for i in range(length)])
