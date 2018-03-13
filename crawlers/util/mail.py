# coding: utf-8

"""发送电子邮件。"""

import os
import time
import smtplib
import mimetypes
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

import config


def mail_multipart(mail, **kwargs):
    # mail.update(kwargs)  # enable key words arguments support.

    server = smtplib.SMTP_SSL()
    for i in range(5):
        try:
            server.connect('smtp.exmail.qq.com', 465)
            server.login(
                config.QQ_MAIL_ACCOUNT,
                config.QQ_MAIL_PASSWORD)
            break
        except:
            time.sleep(1)
            continue
    else:
        raise StandardError(u'登录邮箱失败')
    if 'to' not in mail:
        raise StandardError(u'请指定收件人')
    multipart = MIMEMultipart()
    if 'attachment' in mail:
        file_paths = mail['attachment']
        for file_path in file_paths:
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                    file_name = os.path.basename(file_path)
                    content_type = mimetypes.guess_type(file_name)[0]
                    if content_type is None:
                        content_type = 'application/octet-stream'
                    file_body = MIMEBase(*content_type.split('/'))
                    file_body.set_payload(data)
                    file_body.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=str(Header(file_name, 'UTF-8')))
                    encode_base64(file_body)
                    multipart.attach(file_body)
            except IOError:
                continue
    if 'text' in mail:
        text = mail['text']  # utf-8 charset limited.
        text = MIMEText(text, 'plain', 'utf-8')
        multipart.attach(text)
    if 'html' in mail:
        html = mail['html']
        html = MIMEText(html, 'html', 'utf-8')
        multipart.attach(html)
    receipts = mail['to']
    sender = mail.get('from', config.QQ_MAIL_ACCOUNT)
    multipart['From'] = sender
    multipart['To'] = ','.join(receipts)
    multipart['Subject'] = mail.get('subject')

    for i in range(3):
        try:
            server.sendmail(
                sender, ','.join(receipts), multipart.as_string())
            break
        except:
            continue
    else:
        raise StandardError(u'发送邮件失败')
    server.close()


if __name__ == '__main__':
    pass
