import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import config
import const

from config import ConfigReader

if __name__ == '__main__':
	cr = ConfigReader()
	handlers = cr.readAll(const.HANDLER_CONF, const.HANDLER_SECTION)
	modules = cr.readAsDic(const.MODULE_CONF, const.UIMODULE_SECTION)
	app = tornado.web.Application(
			handlers = handlers,
			template_path = os.path.join(os.path.dirname(__file__), 'templates'),
			static_path = os.path.join(os.path.dirname(__file__), 'static'),
			ui_modules = modules
			)
	server = tornado.httpserver.HTTPServer(app)
	server.listen(cr.read(const.SERVER_CONF, const.SERVER_SECTION, const.SERVER_PORT))
	tornado.ioloop.IOLoop.instance().start()
