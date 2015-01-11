#!/usr/bin/env python
#-*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

import sys
import os
sys.path.append("%s/../"%os.path.dirname(os.path.realpath(__file__)))

class mailLib():
    def simple_text_mail_send(self, subject, content, from_mail_addr, to_mail_addr, mail_server):
        mail = MIMEMultipart()
        mail["Subject"] = subject

        content = MIMEText(content,'html','utf-8')
        mail.attach(content)


        mail["From"]=from_mail_addr
        mail["To"]=to_mail_addr
        smtp=smtplib.SMTP(mail_server)
        smtp.sendmail(mail["From"], mail["To"].split(","), mail.as_string())
        smtp.quit()
    def has_attach_mail_send(self, subject,attach_file,content,from_mail_addr,to_mail_addr,mail_server):
        mail = MIMEMultipart()
        mail["Subject"] = subject

        att = MIMEText(open(attach_file, 'rb').read(), 'base64', 'gb2312')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = "attachment; filename="+attach_file    #这里的filename可以任意写，写什么名字，邮件中显示什么名字
        mail.attach(att)

        content = MIMEText(content,'html','utf-8')
        mail.attach(content)


        mail["From"]=from_mail_addr
        mail["To"]=to_mail_addr
        smtp=smtplib.SMTP(mail_server)
        smtp.sendmail(mail["From"], mail["To"].split(","), mail.as_string())
        smtp.quit()

if __name__ == '__main__':
    subject = u"【BME任务配置告警】任务配置ERROR"
    content = u"任务配置ERROR，请检查"
    from_mail_addr = u"yangjun03@baidu.com"
    to_mail_addr = u"yangjun03@baidu.com"
    mail_server = u"mail2-in.baidu.com"

    maillib = mailLib()
    maillib.simple_text_mail_send(subject, content, from_mail_addr, to_mail_addr, mail_server)

