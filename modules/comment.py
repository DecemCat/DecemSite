__author__ = 'gavin'
import tornado.web


class CommentModule(tornado.web.UIModule):
    def __init__(self, handler):
        super(CommentModule, self).__init__(handler)

    def render(self, article_id):
        return self.render_string('module/comment.html')
