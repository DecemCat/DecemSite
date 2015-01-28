__author__ = 'gavin'
import tornado.web


class ArticleModule(tornado.web.UIModule):
    def render(self, article, index):
        link = ""
        if index == 1:
            link = "blog"
        else:
            link = "life"

        return self.render_string('module/article.html', article=article, link=link)