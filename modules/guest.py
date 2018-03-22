import datetime
import random
import string

import dao.dbase
from handler.commutil.encrypt import AESUtil
from handler.commutil.smsutil import SMSSender


class Guest:
    def __init__(self, phone):
        self._phone = phone
        self._guest = dao.dbase.BaseDBSupport().db['guest']
        self._sender = SMSSender()

    def get_guest(self, cookie, ip):
        if not cookie or not ip:
            return None

        guest = self._guest.find_one({"phone": self._phone, "status": "1"})
        if not guest:
            return None

        if guest['ip'] != ip:
            return None

        passwd = guest["passwd"]
        try:
            en = AESUtil.decrypt(passwd, cookie, "www.0x12345.com")
            if en == self._phone:
                return guest
        except:
            pass

        return None

    def create_guest(self, name, ip):
        chars = string.digits
        code = ''.join([random.choice(chars) for i in range(6)])
        passwd = ''.join([random.choice(string.digits) for i in range(24)])
        pre_guest = self._guest.find_one({'phone': self._phone})
        self._sender.send_sms(code, self._phone)
        if pre_guest:
            self._guest.update_one({'phone': self._phone}, {'$set': {'name': name, 'ip': ip, 'status': '0', 'passwd': passwd, 'code': code, 'chance': 0}})
            return pre_guest
        else:
            guest = {'guest': name, 'passwd': passwd, 'time': datetime.datetime.now(), 'phone': self._phone, 'ip': ip, 'status': '0', 'code': code, 'chance': 0}
            self._guest.insert_one(guest)
            return guest

    def confirm_guest(self, code):
        if not code:
            return False

        guest = self._guest.find_one({'phone': self._phone})
        if not guest:
            return False

        if guest['code'] == code:
            del guest['code']
            guest['status'] = '1'
            self._guest.update_one({'phone': self._phone}, {'$set': {'status': '1'}, '$unset': {'code': ''}})
            return True

        if guest["chance"] > 1:
            self._guest.update_one({"_id": guest['_id']}, {'$set': {'status': '2'}, '$unset': {'code': ''}})
            return False

        self._guest.update_one({"_id": guest['_id']}, {"$set": {"chance": guest["chance"] + 1}})
        return False
