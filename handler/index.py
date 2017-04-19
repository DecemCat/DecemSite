import tornado.web
import list

class IndexHandler(list.ListHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request,
                **kwargs)
        self.init()

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        keyword = None
        page = 1
        tag = None

        if self.request.arguments.has_key("keyword"):
            keyword = self.get_argument("keyword")

        if self.request.arguments.has_key("page"):
            page = int(self.get_argument("page"))

        if self.request.arguments.has_key("tag"):
            tag = self.get_argument("tag")

        if not self.set_param(page, keyword, tag):
            return

        self.get_process()
