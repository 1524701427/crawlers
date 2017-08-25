# -*- coding: utf-8 -*-

"""通用Proxy代理库实现。"""

from __future__ import with_statement
from __future__ import print_function

import sys
import json
import hashlib
import traceback
from collections import deque

from core.enum import Enum


class SchemaType(Enum):
    HTTP = 'http'  # HTTP协议
    HTTPS = 'https'  # HTTPS协议


class Proxy(object):
    """通用代理对象实现。

    Args:
        host (str): 代理主机。
        port (int): 代理端口。
        schema (str): 制定代理schema，默认为'http'或'https'。
        user (str): 用户名，默认为''。
        password (str): 用户密码，默认为''。
    """
    def __init__(self,  host, port, schema='http', user='', password=''):
        assert schema in SchemaType.ALL_AVALIABLE_VALUES
        assert host

        super(Proxy, self).__init__()
        self.schema = schema
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.hashcode = hashlib.md5(','.join([
            self.schema,
            self.user,
            self.password,
            self.host,
            str(self.port)])).hexdigest()

    @classmethod
    def from_dict(cls, d):
        # 可以考虑加入更多的序列化支持。
        keys = ['schema', 'user', 'password', 'host', 'port']
        for k in keys:
            if k not in d:
                raise KeyError(k)
        inst = object.__new__(cls)
        cls.__init__(inst, *[d[k] for k in keys])
        return inst

    @property
    def dict(self):
        d = dict()
        for k in ['schema', 'user', 'password', 'host', 'port']:
            d[k] = getattr(self, k)
        return d

    def __repr__(self):
        return '<Proxy object at 0x%x, hashcode %s>' % (id(self), self.hashcode)  # noqa: E501

    def __str__(self):
        url = '%s://' % self.schema
        if self.user and self.password:
            url += '%s@%s:' % (self.user, self.password)
        url += self.host
        if self.port:
            url += ':%d' % self.port
        return url


class ProxyPool(object):
    """通用代理池实现。

    Args:
        max_size (int): 尺寸。
    """
    def __init__(self, max_size=None):
        self.max_size = max_size
        self.pool = deque(maxlen=max_size)
        self.cursor = 0

    def push(self, proxy):
        self.pool.append(proxy)

    def cycle(self):
        """循环队列生成器。"""
        while True:
            if not self.pool:
                raise StopIteration
            yield self.pool[self.cursor]
            self.cursor = (self.cursor + 1) % len(self.pool)

    def load_from_json(self, json_file):
        """从json文件中加载代理列表。"""
        try:
            with open(json_file, 'rt') as f:
                data = json.loads(f.read())
                for proxy in data:
                    self.pool.append(Proxy.from_dict(proxy))
        except IOError:
            sys.stderr.write(traceback.format_exc())

    def load_from_list(self, proxies):
        """从列表中加载代理。"""
        for proxy in proxies:
            if not isinstance(proxy, Proxy):
                continue
            self.pool.append(proxy)

    def feedback(self, proxy):
        """代理可用性，可靠性等，反馈。"""
        # hashcode用来快速查找，下面的host，port判断是为了防止避免哈希冲突。
        for _proxy in self.pool:
            if proxy.hashcode == _proxy.hashcode \
                    and proxy.host == _proxy.host \
                    and proxy.port == _proxy.port:
                self.pool.remove(_proxy)


if __name__ == '__main__':
    # 从网页上抓取一部分免费代理。
    proxy1 = Proxy('114.85.113.31', 53281)
    proxy2 = Proxy('223.13.69.86', 8118)
    proxy3 = Proxy('101.68.73.54', 53281)
    pool = ProxyPool()
    pool.load_from_list([proxy1, proxy2, proxy3])
    for proxy in pool.cycle():
        print(proxy)
