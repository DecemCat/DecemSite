__author__ = 'gavin'
import tornado.web

import dao.dbase


class TagModule(tornado.web.UIModule):
    def __init__(self, handler):
        super(TagModule, self).__init__(handler)
        self._tags = dao.dbase.BaseDBSupport().db["tags"]
        self._posts = dao.dbase.BaseDBSupport().db["posts"]

    def render(self):
        atags = self._tags.find({})
        tags = []
        for atag in atags:
            atag["count"] = self._posts.find({"tags": {"$elemMatch": {"$eq": atag["name"]}}}).count()
            tags.append(atag)
        return self.render_string('module/tags.html', tags=tags)