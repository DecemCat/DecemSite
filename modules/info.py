__author__ = 'gavin'
import tornado.web
import dao.dbase


class InfoModule(tornado.web.UIModule):
    def __init__(self, handler):
        super(InfoModule, self).__init__(handler)
        self._config = dao.dbase.BaseDBSupport().db["config"]

    def render(self):
        introduce = self._config.find_one({"key": "info.introduce"})["value"]
        return self.render_string('module/info.html', introduce=introduce)