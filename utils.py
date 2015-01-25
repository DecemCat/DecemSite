__author__ = 'Administrator'
import tornado.web


class RequestHandler:
    @staticmethod
    def get_argument(request, key, default_val):
        assert isinstance(request, tornado.web.RequestHandler)
        value = default_val
        try:
            value = request.get_argument(key)
        except tornado.web.MissingArgumentError:
            value = default_val
        return value