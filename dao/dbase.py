import pymongo
import const
import threading

from config import ConfigReader
Lock = threading.Lock()


class BaseDBSupport(object):
    __instance = None

    def __init__(self):
        cr = ConfigReader()
        self._dbip = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBIP)
        self._dbport = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBPORT)
        self._dbname = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBNAME)
        self._dbuser = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBUSER)
        self._dbpass = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBPASS)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(BaseDBSupport, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance

    @property
    def db(self):
        if not hasattr(self, '_db'):
            conn = pymongo.MongoClient(self._dbip, int(self._dbport))
            self._db = conn[self._dbname]
            self._db.authenticate(self._dbuser, self._dbpass)
        return self._db
