__author__ = 'Administrator'
import smtplib
import traceback
from email.mime.text import MIMEText
import logging

import dao.dbase
from encrypt import AESUtil

log = logging.getLogger("run")


class EmailUtils:
    @staticmethod
    def send_mail(to_list,sub,content):
        log.info("start send email %s to %s", sub, to_list)
        _config = dao.dbase.BaseDBSupport().db["config"]
        mail_host = _config.find_one({"key": "email.smtp.server"})["value"]
        mail_user = _config.find_one({"key": "email.username"})["value"]
        mail_pass = _config.find_one({"key": "email.password"})["value"]
        key = _config.find_one({"key": "security.key"})["value"]
        iv = _config.find_one({"key": "security.iv"})["value"]
        mail_pass = AESUtil.decrypt(key, mail_pass, iv)

        me="0x12345"+"<"+mail_user+">"
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP_SSL()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception,e:
            log.error("send email to %s failed, exception: %s", to_list, e.message)
            traceback.print_exc()
            return False
