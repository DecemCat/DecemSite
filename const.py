class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const (%s)" % name
        self.__dict__[name] = value


const = _const()

const.HANDLER_CONF = "handler.conf"
const.MODULE_CONF = "module.conf"
const.SERVER_CONF = "server.conf"

const.HANDLER_SECTION = "handlers"
const.SERVER_SECTION = "server"
const.UIMODULE_SECTION = "uimodules"
const.DBS_SECTION = "db"

const.SERVER_IP = "ip"
const.SERVER_PORT = "port"

const.DBIP = "dbip"
const.DBPORT = "dbport"
const.DBNAME = "dbname"
const.DBUSER = "dbuser"
const.DBPASS = "dbpass"


const.INIT_STATIC = {"title":"", "content": "", "time": ""}
const.INIT_POST = {"_id": "","title": "", "content":"", "time": "", "tags": [], "brief":""}
const.INIT_TIMELINE = {"_id": "","headline": "", "text":"", "startDate": "", "endDate": "", "asset":{"media":"", "credit":"", "caption": ""}}

const.PAGE_SIZE = 5
