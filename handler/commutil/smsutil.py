# coding=utf-8
import urllib
import urllib2

import dao.dbase
import logging
from encrypt import AESUtil

log = logging.getLogger("run")


class SMSSender:
    def __init__(self):
        self._config = dao.dbase.BaseDBSupport().db["config"]
        sms_code = self._config.find_one({'key': 'sms.code'})["value"]
        key = self._config.find_one({"key": "security.key"})["value"]
        iv = self._config.find_one({"key": "security.iv"})["value"]

        self.token = AESUtil.decrypt(key, sms_code, iv)
        self.url = self._config.find_one({'key': 'sms.url'})["value"]
        self._smsrecord = dao.dbase.BaseDBSupport().db['smsrecord']


    def send_sms(self, code, receiver):
        host = self.url
        path = '/singleSendSms'
        method = 'GET'
        appcode = self.token
        querys = 'ParamString=%7B%22code%22%3A%22' + code + '%22%7D&RecNum=' + receiver + '&SignName=' + urllib.quote('九三散人') + '&TemplateCode=SMS_67655025'

        url = host + path + '?' + querys
        request = urllib2.Request(url)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        response = urllib2.urlopen(request)
        content = response.read()
        log.info("send sms to %s response %s", receiver, content)
        if (content):
            self._smsrecord.insert_one({'code': code, 'receiver': receiver, 'result': content})

