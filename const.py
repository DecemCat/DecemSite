class _const:
	class ConstError(TypeError): pass
	def __setattr__(self, name, value):
		if self.__dict__.has_key(name):
			raise self.ConstError, "Can't rebind const (%s)" % name
		self.__dict__[name] = value

_const.HANDLER_CONF = "handler.conf"
_const.MODULE_CONF = "module.conf"
_const.SERVER_CONF = "server.conf"

_const.HANDLER_SECTION = "handlers"
_const.SERVER_SECTION = "server"
_const.UIMODULE_SECTION = "uimodules"
_const.DBS_SECTION = "db"

_const.SERVER_IP = "ip"
_const.SERVER_PORT = "port"

_const.DBNAME = "dbname"
_const.DBUSER = "dbuser"
_const.DBPASS = "dbpass"
import sys
sys.modules[__name__] = _const()

