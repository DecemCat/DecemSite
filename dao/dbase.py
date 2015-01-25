import pymongo
import const

from config import ConfigReader

class BaseDBSupport:
    def __init__(self):
        cr = ConfigReader()
        self._dbname = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBNAME)
        self._dbuser = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBUSER)
        self._dbpass = cr.read(const.SERVER_CONF, const.DBS_SECTION, const.DBPASS)

    @property
    def db(self):
        if not hasattr(self, '_db'):
            cr = ConfigReader()
            conn = pymongo.Connection('127.0.0.1', 27017)
            self._db = conn[self._dbname]
            self._db.authenticate(self._dbuser, self._dbpass)
        return self._db