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

        if self.request.arguments.has_key("kw"):
            keyword = self.get_argument("kw")

        if self.request.arguments.has_key("page"):
            page = int(self.get_argument("page"))

        if not self.set_param(page, keyword, None):
            return

        self.get_process()
