import asyncmongo
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
            self._db = asyncmongo.Client(pool_id='wb4m',
                                         host='127.0.0.1',
                                         port=27017,
                                         maxconnections=50,
                                         dbname=self._dbname,
                                         dbuser=self._dbuser,
                                         dbpass=self._dbpass
                                         )
        return self._db


    def find(self, table, limit=1, **param):
        conn = self.db.connection(collectionname=table)
        conn.find(param, callback=self._on_find)


    def _on_find(self, response, error):
        print(error)
        print(response)