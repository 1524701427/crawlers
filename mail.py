#!/usr/bin/env python
# coding: utf-8

'''
发送邮件'''

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

import config


def mail_multipart(mail):
    server = smtplib.SMTP_SSL()
    for i in range(5):
        try:
            server.connect('smtp.exmail.qq.com', 465)
            server.login(
                config.QQ_MAIL_ACCOUNT,
                config.QQ_MAIL_PASSWORD)
            break
        except:
            continue
    else:
        raise StandardError(u'登录邮箱失败')
    if 'to' not in mail:
        raise StandardError(u'请指定收件人')
    multipart = MIMEMultipart()
    if 'attachment' in mail:
        file_path = mail['attachment']
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                file_body = MIMEBase('application', 'octet-stream')
                file_body.set_payload(data)
                file_name = os.path.basename(file_path)
                encode_base64(file_body)
                file_body.add_header(
                    'Content-Disposition', 'attachment', filename=file_name)
                multipart.attach(file_body)
        except IOError:
            raise StandardError(u'打开附件失败')
    if 'text' in mail:
        text = mail['text']
        text = MIMEText(text)
        multipart.attach(text)
    receipts = mail['to']
    sender = mail.get('from', config.QQ_MAIL_ACCOUNT)
    multipart['From'] = sender
    multipart['To'] = ','.join(receipts)
    multipart['Subject'] = mail.get('subject')

    for i in range(3):
        try:
            server.sendmail(sender, ','.join(receipts), multipart.as_string())
            break
        except:
            continue
    else:
        raise StandardError(u'发送邮件失败')


if __name__ == '__main__':
    mail = dict()
    mail['to'] = ['wanglanwei@weiche.cn']
    mail['text'] = '测试邮件'
    mail['attachment'] = 'requirements.txt'
    mail_multipart(mail)
