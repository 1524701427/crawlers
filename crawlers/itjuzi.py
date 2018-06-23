# -*- coding: utf-8 -*-

"""爬取it桔子项目的爬虫。"""

from __future__ import print_function


from const import (
    HttpStatus,
)
from util.uapool import DeviceType, UAPool
from util.http import HttpClient


class ItjuziCrawler(object):

    ItjuziHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',  # noqa: E501
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Referer': 'https://www.itjuzi.com/user/login',
    }

    # 登录地址
    login_url = 'https://www.itjuzi.com/user/login?redirect=&flag=&radar_coupon='  # noqa: E501

    def __init__(self, username, password):
        self.httpclient = HttpClient(default_headers=self.ItjuziHeaders)
        self.username = username
        self.password = password
        self.uapool = UAPool(DeviceType.PC)

    def login(self):
        """登录IT桔子。"""
        data = {
            'identity': self.username,
            'password': self.password,
            'submit': '',
            'page': '',
            'url': '',
        }
        resp = self.httpclient.post(self.login_url, data=data, verify=False)
        if resp is not None and resp.status_code == HttpStatus.StatusOk:
            print('SUCCEED! ===================================>')  # noqa
            for cookie in resp.cookies:
                print('%s=%s' % (cookie.name, cookie.value))
            print('END==============')

    def run(self):
        """运行。"""
        page = 1
        url_tpl = 'http://radar.itjuzi.com/company/infonew?page=%(page)d'
        quit = False
        while not quit:
            url = url_tpl % dict(page=page)
            resp = self.httpclient.get(url, headers={'User-Agent': self.uapool.pick()})  # noqa: E501
            if resp is not None:
                try:
                    rows = resp.json()['data']['rows']
                    for row in rows:
                        print('>>>', row)
                except KeyError as e:
                    print(e)
                    continue
            page += 1
            if page >= 2:
                break


if __name__ == '__main__':
    pass
