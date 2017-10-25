# -*- coding: utf-8 -*-

import json
import time
import collections

import requests


class Proxy(object):
    """代理。"""
    ST_AVALIABLE = 0
    ST_UNAVALIABLE = 1

    def __init__(self, schema, host, port, user=None, password=None):
        self.schema = schema
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.status = self.ST_AVALIABLE

    def update(self, status):
        self.status = status

    @property
    def request_proxy_style(self):
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


class FileLoader(object):
    """从文件中加载。"""

    def __init__(self, file_path):
        super(FileLoader, self).__init__()
        self.f = open(file_path, 'rt')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.f.close()
        except:
            pass
        self.f = None

    def __iter__(self):
        return self

    def next(self):
        try:
            return json.loads(next(self.f))
        except StopIteration:
            raise


class HttpClient(object):
    """爬虫用Http客户端。"""

    def __init__(self, default_headers=None, retries=3, internal=0.5):
        self.retries = retries
        self.internal = 3
        self.session = requests.Session()
        if default_headers is not None:
            self.session.headers.update(default_headers)

    def get(self, url, proxies=None):
        options = dict()
        options['proxies'] = proxies.request_proxy_style if proxies is not None else None  # noqa: E501
        for i in range(1, self.retries+1):
            try:
                resp = self.session.get(url, **options)
                break
            except:
                time.sleep(self.internal*i)
                continue
        else:
            raise RuntimeError("bad network...")
        return resp


if __name__ == '__main__':
    httpclient = HttpClient()
