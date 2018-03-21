__author__ = 'gavin'
import pymongo
import tornado.web

import dao.dbase


class CommendModule(tornado.web.UIModule):
    def __init__(self, handler):
        super(CommendModule, self).__init__(handler)
        self._posts = dao.dbase.BaseDBSupport().db["posts"]
        self._comment = dao.dbase.BaseDBSupport().db["comment"]

    def render(self):
        posts = self._posts.find({}, {"title": "1"}).sort("time", pymongo.DESCENDING).limit(10)
        comments = []
        for post in posts:
            post["comments"] = self._comment.find({"article_id": str(post["_id"])}).count()
            comments.append(post)
        return self.render_string('module/commend.html', commends=comments)