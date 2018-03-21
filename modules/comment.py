__author__ = 'gavin'
import datetime
import json

import tornado.web
from bson.objectid import ObjectId

import dao.dbase
from guest import Guest
from handler.commutil.encrypt import AESUtil


class CommentModule(tornado.web.UIModule):
    def __init__(self, handler):
        super(CommentModule, self).__init__(handler)
        self._comment = dao.dbase.BaseDBSupport().db["comment"]

    def render(self, article_id):
        cookie = None
        phone = None
        dbcomments = self._comment.find({"article_id": str(article_id), "status": "1"})
        comments = []
        for dbcomment in dbcomments:
            comments.append(dbcomment)

        com2del = []
        for comment in comments:
            if comment.has_key("parent_id") and comment["parent_id"] is not None:
                com2del.append(comment)
                cm = self._find_byid(comments, comment["parent_id"])
                if not cm.has_key("subcomment"):
                    cm["subcomment"] = []
                cm["subcomment"].append(comment)

        for com in com2del:
            comments.remove(com)

        cookie = self.handler.get_secure_cookie('guest')
        phone = self.handler.get_secure_cookie('phone')
        name = None
        if cookie and phone:
            guest = Guest(phone)
            gg = guest.get_guest(cookie, self.request.remote_ip)
            if gg and gg.has_key('guest'):
                name = gg['guest']

        return self.render_string('module/comment.html', comments=comments, article_id=article_id, guest=name, phone=phone)

    def _find_byid(self, comments, id):
        for comment in comments:
            if ObjectId(id) == comment["_id"]:
                return comment
        return None


class CommentHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(CommentHandler, self).__init__(application, request, **kwargs)
        self._comment = dao.dbase.BaseDBSupport().db["comment"]

    def post(self, *args, **kwargs):
        article_id = self.get_body_argument("article_id")
        user = self.get_body_argument("user")
        phone = self.get_body_argument("phone")
        content = self.get_body_argument("content")
        if not article_id or not user or not phone or not content:
            return

        try:
            parent_id = self.get_body_argument("parent_id")
        except tornado.web.MissingArgumentError:
            parent_id = None

        try:
            comment_id = self.get_body_argument("comment_id")
        except tornado.web.MissingArgumentError:
            comment_id = None


        guest = Guest(phone)
        if phone == self.get_secure_cookie('phone'):
            cookie = self.get_secure_cookie('guest')
            gg = guest.get_guest(cookie, self.request.remote_ip)
            if gg is not None:
                user = gg['guest']
                comment = {"article_id": article_id, "user": gg['guest'], "guest": gg['_id'], "content": content, "isauthor": "0", "time": datetime.datetime.now(), "status": "1"}
                if parent_id is not None:
                    comment["parent_id"] = parent_id

                if comment_id is not None:
                    comment["comment_id"] = comment_id
                self._comment.insert(comment)
                result = {"ret": "1"}
                result["id"] = str(comment["_id"])
                self.finish(json.dumps(result))
                return

        gg = guest.create_guest(user, self.request.remote_ip)
        comment = {"article_id": article_id, "user": gg['guest'], "guest": gg['_id'], "content": content, "isauthor": "0", "time": datetime.datetime.now(), "status": "0"}
        if parent_id is not None:
            comment["parent_id"] = parent_id

        if comment_id is not None:
            comment["comment_id"] = comment_id

        self._comment.insert(comment)
        result = {"ret": "0"}
        result["id"] = str(comment["_id"])
        self.finish(json.dumps(result))

class CommentConfirmHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(CommentConfirmHandler, self).__init__(application, request, **kwargs)
        self._comment = dao.dbase.BaseDBSupport().db["comment"]
        self._guest = dao.dbase.BaseDBSupport().db['guest']

    def post(self, *args, **kwargs):
        sms = self.get_body_argument("sms")
        comment_id = self.get_body_argument("commentId")
        cm = self._comment.find_one({"_id": ObjectId(comment_id), "status": "0"})
        if not cm:
            self.finish({"status": "ok"})
            return

        gg = self._guest.find_one({'_id': cm['guest']})
        if not gg:
            self.finish({"status": "fail"})
            return

        phone = gg['phone']
        guest = Guest(phone)
        if guest.confirm_guest(sms):
            self._comment.update_one({"_id": ObjectId(comment_id)}, {"$set": {"status": "1"}})
            passwd = gg['passwd']
            cookie = AESUtil.encrypt(passwd, phone, 'www.0x12345.com')
            self.set_secure_cookie('guest', cookie, expires_days=365)
            self.set_secure_cookie('phone', phone, expires_days=365)
            self.finish({"status": "ok"})
            return

        self.finish({"status":"fail"})
