# coding=utf-8
import dao.dbase
import urllib, urllib2, sys

class SMSSender:
    def __init__(self):
        self._comment = dao.dbase.BaseDBSupport().db["config"]
        self.account = self._comment.find_one({'key': 'sms.account'})["value"]
        self.token = self._comment.find_one({'key': 'sms.code'})["value"]
        self.url = self._comment.find_one({'key': 'sms.url'})["value"]
        self.appid = self._comment.find_one({'key': 'sms.appid'})["value"]
        self._smsrecord = dao.dbase.BaseDBSupport().db['smsrecord']


    def sendSMS(self, code, receiver):
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
        if (content):
            self._smsrecord.insert_one({'code': code, 'receiver': receiver, 'result': content})

