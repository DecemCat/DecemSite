__author__ = 'gavin'
import tornado.web


class ArticleModule(tornado.web.UIModule):
    def render(self, article):
        return self.render_string('module/article.html', article=article)