# -*- coding: utf-8 -*-

import time
import collections

import requests

from const import (
    PROXY_AVALIABLE,
    PROXY_UNAVALIABLE,
)


class Proxy(object):
    """代理。"""

    def __init__(self, schema, host, port, user=None, password=None):
        self.schema = schema
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.status = PROXY_AVALIABLE

    def update(self, status):
        assert status in (PROXY_AVALIABLE, PROXY_UNAVALIABLE), u'无效的代理状态'
        self.status = status

    @property
    def request_proxy_style(self):
        """返回Python requests风格的代理"""
        return {self.schema: str(self)}

    def __str__(self):
        parts = []
        parts.append('%s://' % self.schema)
        if self.user and self.password:
            parts.append('%s@%s:' % (self.user, self.password))
        parts.append('%s:%d' % (self.host, self.port))
        return ''.join(parts)


class ProxyPool(object):
    """Http代理池。"""

    def __init__(self, poolsize=None, dynamic_loader=None):
        self.pool = collections.deque(maxlen=poolsize)
        self.dynamic_loader = dynamic_loader
        self.idx = 0

    def extend(self, proxies):
        self.pool.extend(list(proxies))

    def remove(self, proxy):
        self.pool.pop(proxy)

    def fresh(self):
        self.extend(self.dynamic_loader.refresh())

    def rotate(self):
        proxy = self.pool[self.idx]
        self.idx = (self.idx + 1) % len(self.pool)
        return proxy


class HttpClient(object):
    """爬虫用Http客户端。"""

    def __init__(self, default_headers=None, retries=3, internal=0.5):
        self.retries = retries
        self.internal = 3
        self.session = requests.Session()
        if default_headers is not None:
            self.session.headers.update(default_headers)

    def get(self, url, proxies=None, headers=None):
        options = dict()
        schema2proxy = dict(verify=False)
        if proxies is not None:
            for proxy in proxies:
                schema2proxy.update(proxy)
        options['proxies'] = proxies or None
        if headers is not None:
            self.session.headers.update(headers)
        for i in range(1, self.retries+1):
            try:
                resp = self.session.get(url, **options)
                break
            except:
                time.sleep(self.internal*i)
                continue
        else:
            raise RuntimeError(u"请求资源失败！")
        return resp

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)


if __name__ == '__main__':
    pass
