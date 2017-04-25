__author__ = 'Administrator'
import smtplib
import dao.dbase
import traceback
from email.mime.text import MIMEText

class EmailUtils:
    @staticmethod
    def send_mail(to_list,sub,content):
        _config = dao.dbase.BaseDBSupport().db["config"]
        mail_host = _config.find_one({"key": "email.smtp.server"})["value"]
        mail_user = _config.find_one({"key": "email.username"})["value"]
        mail_pass = _config.find_one({"key": "email.password"})["value"]
        me="0x12345"+"<"+mail_user+">"
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except:
            traceback.print_exc()
            return False
