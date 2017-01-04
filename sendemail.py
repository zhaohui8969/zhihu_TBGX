# coding:utf-8
import smtplib
from email.mime.text import MIMEText
import sys
import json

with open('conf.json') as fop:
    conf = json.loads(fop.read())

smtp_server = conf['smtp_server']

mail_sender = conf['mail_sender']
mail_reciver = conf['mail_reciver']

login_name = mail_sender
login_passwd = conf['login_passwd']


def sendmail(title, content, debug_level=0):
    msg = MIMEText(content, 'html', 'utf-8')  # 设置正文为符合邮件格式的HTML内容
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg['subject'] = title  # 设置邮件标题
    msg['from'] = mail_sender  # 设置发送人
    msg['to'] = mail_reciver  # 设置接收人
    # print content
    server = smtplib.SMTP(smtp_server)
    server.set_debuglevel(debug_level)
    server.ehlo(mail_sender)
    server.login(login_name, login_passwd)
    server.sendmail(mail_sender, mail_reciver, msg.as_string())
    server.quit()


if __name__ == '__main__':
    argv = sys.argv
    msg = argv[1]
    sendmail(u'知乎特别关心邮件测试', msg, 1)
