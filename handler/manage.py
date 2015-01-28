__author__ = 'Administrator'
import tornado.web
import dao.dbase
import datetime
import urllib

from utils import RequestHandler

class ManageHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._submenu = connection.db["submenu"]
        self._blogs = connection.db["blog"]
        self._login = connection.db["login"]

    def get(self, *args, **kwargs):
        username = self.get_secure_cookie("username")
        user = self._login.find({'cookie': username})
        if user is None or user.count() == 0:
            self.render('login.html')
            return
        tags = self._submenu.find()
        self.render('manage.html', tags=tags)

class PostHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._blogs = connection.db["blog"]

    def post(self, *args, **kwargs):
        title = RequestHandler.get_argument(self, 'title')
        content = RequestHandler.get_argument(self, 'content')
        content = content[1:len(content)-1]
        content = content.replace('\\\"', '"')
        type = RequestHandler.get_argument(self, 'type')
        typei = int(type)
        tags = RequestHandler.get_argument(self, 'tags')
        if title is None or len(title)==0 or content is None or type is None or tags is None or len(content)==0 or len(type)==0:
            raise tornado.web.HTTPError(400)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._blogs.insert({'title': title, 'content': content, 'type': typei, 'tags': tags, 'author': 'gavin', 'comments': 0, 'create_time':current_date, 'update_time': current_date})
