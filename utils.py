__author__ = 'Administrator'
import smtplib
from email.mime.text import MIMEText


mailto_list = ["admin@wb4m.com"]
mail_host = "smtp.ym.163.com"
mail_user = "account@wb4m.com"
mail_pass = "zhaohongwei"
mail_postfix = "wb4m.com"
class EmailUtils:
    @staticmethod
    def send_mail(to_list,sub,content):
        me="wb4m"+"<"+mail_user+">"
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
        except Exception, e:
            print str(e)
            return False