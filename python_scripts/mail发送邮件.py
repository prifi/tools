#!/usr/bin/env python
# coding:utf-8
# 通过163邮箱发送邮件
import smtplib, sys
from email.mime.text import MIMEText
from email.header import Header

# 收件人信息
to_user = sys.argv[1]
to_subject = sys.argv[2]
to_message = sys.argv[3]

# 第三方 SMTP 服务
mail_host = "smtp.163.com"         # 设置服务器
mail_user = "xxx@163.com"  # 用户名
mail_pass = ""     # 口令

sender = mail_user
sender_name = "monitor@zabbix.com"  # 显示名称

message = MIMEText(to_message, 'plain', 'utf-8')
message['From'] = "{0}<{1}>".format(sender_name ,sender)
message['To'] = to_user
message['Subject'] = Header(to_subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, to_user, message.as_string())
    print "邮件发送成功"
    smtpObj.quit()
    smtpObj.close()
except smtplib.SMTPException as e:
    print "Error: 无法发送邮件", e
