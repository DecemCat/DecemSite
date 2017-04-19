import tornado.web
import dao.dbase
import pymongo

class IndexHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request,
                **kwargs)
        connection = dao.dbase.BaseDBSupport()
        self._blog = connection.db["posts"]

    @tornado.web.asynchronous
    def get(self):
        total_count = self._blog.find({}).count()
        if self.request.arguments.has_key("page"):
            page = int(self.get_argument("page"))
            if page == 0:
                page = total_count / 10 + 1 if total_count % 10 != 0 else 0
                self.redirect('index.html?page=' + str(page))
                return
        else:
            page = 1

        if total_count <= (page - 1) * 10:
            self.redirect('index.html?page=1')
            return

        posts = self._blog.find({}).sort('time', pymongo.DESCENDING).skip((page - 1) * 10).limit(10)
        if posts is None:
            posts = {}
        self.render('index.html', posts=posts, page=page)
