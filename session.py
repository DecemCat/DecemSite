__author__ = 'Administrator'
import os
import time
import hashlib
class SessionManagerBase(object):
    """session manager�Ļ���"""
    def generate_session_id(self, salt):
        """����Ψһ��session_id"""
        rand = os.urandom(16)
        now = time.time()
        return hashlib.sha1("%s%s%s" %(rand, now, salt)).hexdigest()

    def create_new(self, session_id):
        """������session����session������ʱ"""
        pass

    def save_session(self, session):
        """����session"""
        pass

    def load_session(self, session_id = None):
        """����session_id load session"""
        pass


class MongoSessionManager(SessionManagerBase):
    def __init__(self, db, collection_name='sessions', **kw):
        """session ����mongodbΪ��˱��棬 Ĭ���Ǵ��� sessions ������"""
        self._collection = db[collection_name]

    def create_new(self, session_id):
        return BaseSession(session_id, self, {})

    def save_session(self, session):
        """����session ��mongodb"""
        self._collection.save({'_id' : session.get_session_id(), 'data' : session})

    def load_session(self, session_id = None):
        data = {} # Ĭ��Ϊ��session
        if session_id:
            # ��session ���͵���
            session_data = self._collection.find_one({'_id' : session_id})
            if session_data:
                # ��ֹ��������
                data = session_data['data']

        return BaseSession(session_id, self, data)

class BaseSession(dict):
    def __init__(self, session_id = '', mgr = None, data = {}):
        self.__session_id = session_id
        self.__mgr = mgr
        self.update(data)
        self.__change = False # СС���Ż��� ���sessionû�иı䣬 �Ͳ��ñ�����

    def get_session_id(self):
        return self.__session_id

    def save(self):
        if self.__change:
            self.__mgr.save_session(self)
            self.__change = False

    # ------------------------------------------
    # ʹ��session[key] ��key������ʱ����None�� ��ֹ�����쳣
    def __missing__(self, key):
        return None

    def __delitem__(self, key):
        if key in self:
            del self[key]
            self.__change = True

    def __setitem__(self, key, val):
        self.__change = True
        super(BaseSession, self).__setitem__(key, val)