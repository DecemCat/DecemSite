# coding=utf-8
import tornado.web
import re

import dao.dbase


class ListHander(tornado.web.RequestHandler):
    def init(self):
        self._page = None
        self._tag = None
        self._keyword = None
        self._posts = dao.dbase.BaseDBSupport().db["posts"]

    def _get_url(self, page, keyword, tag):
        url = "index.html?page=" + str(page)
        if keyword:
            url += "&keyword=" + keyword
        if tag:
            url += "&tag=" + tag
        return url

    def set_param(self, page, keyword, tag):
        if page is None:
            self._page = 1
        else:
            total_count = self._posts.find({}).count()
            if page == 0:
                page = total_count / 10 + 1 if total_count % 10 != 0 else 0
                self.redirect(self._get_url(page, keyword, tag))
                return False
            if page != 1 and total_count <= (page - 1) * 10:
                self.redirect(self._get_url(1, keyword, tag))
                return False
            self._page = page

        if keyword:
            self._keyword = keyword.trip()

        self._tag = tag
        return True

    def get_process(self):
        posts = self._posts.find(self.get_condition()).skip(self.get_skip()).limit(self.get_limit())
        self.render('index.html', posts=posts, page=self._page, keyword=self._keyword, tag=self._tag)

    def get_skip(self):
        return (self._page - 1) * 10

    def get_limit(self):
        return 10

    def get_condition(self):
        condition = {}
        if self._keyword:
            condition["$or"] = [{"title": re.compile(self._keyword)}, {"content": re.compile(self._keyword)}]
        if self._tag:
            condition["tags"] = {"$elemMatch": {"$eq": self._tag}}

        return condition
