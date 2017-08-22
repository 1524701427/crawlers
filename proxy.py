# -*- coding: utf-8 -*-

"""通用Proxy代理库实现。"""

from __future__ import with_statement
from __future__ import print_function

import hashlib
from collections import deque

from core.enum import Enum
from core.exceptions import ProxyPoolEmptyError


class SchemaType(Enum):
    HTTP = 'http'  # HTTP协议
    HTTPS = 'https'  # HTTPS协议


class Proxy(object):
    """通用代理对象实现。

    Args:
        schema (str): 制定代理schema，默认为'http'或'https'。
        user (str): 用户名。
        password (str): 用户密码。
        host (str): 代理主机。
        port (int): 代理端口。
    """
    def __init__(self, schema, user, password, host, port):
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
    """通用代理池实现。"""


if __name__ == '__main__':
    proxy = Proxy.from_dict({
        'schema': 'http',
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'port': 1080,
    })
    print(repr(proxy))
    print(proxy.dict)
