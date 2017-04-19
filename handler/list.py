# coding=utf-8
import tornado.web
import re

import dao.dbase
PAGE_SIZE = 5


class ListHandler(tornado.web.RequestHandler):
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
        if keyword:
            self._keyword = keyword

        self._tag = tag

        if page is None:
            self._page = 1
        else:
            total_count = self._posts.find(self.get_condition()).count()
            if page == 0:
                page = total_count / PAGE_SIZE + 1 if total_count % PAGE_SIZE != 0 else 0
                self.redirect(self._get_url(page, keyword, tag))
                return False
            if page != 1 and total_count <= (page - 1) * PAGE_SIZE:
                self.redirect(self._get_url(1, keyword, tag))
                return False
            self._page = page

        return True

    def get_process(self):
        posts = self._posts.find(self.get_condition()).skip(self.get_skip()).limit(self.get_limit())
        self.render('index.html', posts=posts, page=self._page, keyword=self._keyword, ct=self._tag)

    def get_skip(self):
        return (self._page - 1) * PAGE_SIZE

    def get_limit(self):
        return PAGE_SIZE

    def get_condition(self):
        condition = {}
        if self._keyword:
            condition["$or"] = [{"title": re.compile(self._keyword)}, {"content": re.compile(self._keyword)}]
        if self._tag:
            condition["tags"] = {"$elemMatch": {"$eq": self._tag}}

        return condition
