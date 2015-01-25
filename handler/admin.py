__author__ = 'Administrator'
import tornado.web
import dao.dbase
import datetime
import string
import random

from utils import EmailUtils
from utils import RequestHandler

class AdminHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def _gen_password(self, length):
        chars=string.ascii_letters+string.digits
        return ''.join([random.choice(chars) for i in range(length)])

    def post(self, *args, **kwargs):
        connection = dao.dbase.BaseDBSupport()
        mac = RequestHandler.get_argument(self, 'u1', None)
        username = RequestHandler.get_argument(self, 'u2', None)
        password = RequestHandler.get_argument(self, 'u3', None)
        logout = RequestHandler.get_argument(self, 'logout', 0)
        if logout == 1:
            connection.db["login"].remove({'username': username})
            self.render("login.html")
            return

        if mac is None or username is None or password is None:
            self.render('login.html')
            return

        if mac == 1:
            password = self._gen_password(10)
            EmailUtils.send_mail("admin@wb4m.com", "Password for this time", password)
            time = datetime.datetime.now()
            connection.db["login"].insert({'mac': mac, 'username': username, 'password': password, 'create_time': time})
            self.render('login.html')
            return


        users = connection.db["login"].find({'username': username, 'password': password})
        if users.count() > 0:
            cookie = username + datetime.time.strftime()
            self.set_secure_cookie('username', cookie)
            connection.db["login"].update({'_id', users[0]['_id']}, {'cookie': cookie})
            self.render("manage.html")
            return

        self.render("login.html")

