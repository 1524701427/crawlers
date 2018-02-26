# -*- coding: utf-8 -*-

"""爬取铅笔道项目的爬虫。"""

from __future__ import print_function


import time
from http import HttpClient
from const import (
    HTTP_OK,
)


class QianBiDaoCrawler(object):

    QianBiDaoAppHeaders = {
        'User-Agent': 'PencilNews/1.3.0 (iPhone; iOS 11.2.5; Scale/2.00)',
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Authority': 'api.pencilnews.cn',
    }

    def __init__(self, username, password):
        self.httpclient = HttpClient(default_headers=self.QianBiDaoAppHeaders)
        self.username = username
        self.password = password
        self.token = ""

    def login(self):
        """登录铅笔道"""
        data = dict(username=self.username, password=self.password)
        resp = self.httpclient.post(
            'https://api.pencilnews.cn/user/login',
            data=data,
            verify=False)  # 关闭HTTPS证书验证
        if resp and resp.status_code == HTTP_OK:
            ret = resp.json()
            if ret and ret['message'] == 'SUCCESS':
                self.token = ret['data']['user']['token']
        return self.token

    def run(self):
        """爬虫运行"""
        page = 1
        url_tpl = 'https://api.pencilnews.cn/pay-project/list?page=%(page)d'
        projects = list()
        headers = [u'项目名称', u'所属领域', u'']
        while True:
            url = url_tpl % dict(page=page)
            resp = self.httpclient.get(url, headers=dict(token=self.token))
            if resp:
                project = dict()
                project['id'] = ''
                project['name'] = u''
                project['description'] = u''
                projects.append(project)
            time.sleep(1)
            page += 1


if __name__ == '__main__':
    cralwer = QianBiDaoCrawler('18766121367', 'lyr910216')
    cralwer.run()
