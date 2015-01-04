import asyncmongo
import tornado.web

class IndexHanlder(tornado.web.RequestHandler):
	@property
	def db(self):
		if not hasattr(self, '_db'):
			self._db = asyncmongo.Client(pool_id='wb4m', host='127.0.0.1', port=27017, maxcached=10, maxconnections=50, dbname='wb4m')
		return self._db

	@tornado.web.asynchronous
	def get:



