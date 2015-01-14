import asyncmongo

class BaseDBSupport:
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(pool_id='wb4mdb', host='127.0.0.1', port=27017, maxconnections=50, dbname='wb4m')
        return self._db


    def find(self, table, limit=1, **param):
        conn = self.db.connection(collectionname=table)
        conn.find(param, callback=self._on_find)


    def _on_find(self, response, error):
        print(error)
        print(response)