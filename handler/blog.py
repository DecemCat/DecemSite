import tornado.web
import tornado.escape
import dao.dbase
import pymongo
import const
import urllib

from utils import RequestHandler
class BlogHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        connection = dao.dbase.BaseDBSupport()
        page = RequestHandler.get_argument(self, 'p', 1)
        type = RequestHandler.get_argument(self, 'type', 0)
        page = int(page)

        start = (page - 1) * const.PAGE_SIZE
        articles = connection.db["blog"].find({'type': 0}).sort("create_time", pymongo.ASCENDING).skip(start).limit(const.PAGE_SIZE)
        count = connection.db["blog"].find({'type': 0}).count()
        total_size = count / const.PAGE_SIZE
        remainder = count % const.PAGE_SIZE
        if remainder != 0:
            total_size = total_size + 1
        self.render('blog.html', articles=articles, page={"currentPage": page-1, "totalCount": total_size}, index=1)