# -*- coding: utf-8 -*-

import sys
import time
import random
import binascii
from abc import ABCMeta, abstractmethod
from functools import wraps

from requests import exceptions


class DataSource(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, count):
        raise NotImplementedError()

    @abstractmethod
    def stream(self, **options):
        raise NotImplementedError()


class Proxy(object):

    def __init__(
            self, host, port,
            schema='http', user=None, passwd=None, weight=0):
        self.schema = schema
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.weight = weight

    def __hash__(self):
        identifier = [self.schema, self.host, str(self.port)]
        identifier = ','.join(identifier)
        return binascii.crc32(identifier)

    def __repr__(self):
        return '<%s object at 0x%x>' % (
            self.__class__.__name__, id(self),
        )

    def __getitem__(self, key):
        return self.__getattribute__(key)


class ProxyPool(object):

    def __init__(
            self, datasource, poolsize=30, **options):
        assert poolsize > 0
        assert datasource
        self.poolsize = poolsize
        self.tries = options.get('tries', 3)
        self.datasource = datasource
        self.pool = []

    def peek(self):
        if not self.pool:
            raise IndexError()
        return random.choice(self.pool)

    def remove(self, item):
        self.pool.remove(item)

    def pop(self):
        self.pool.pop(0)

    def refresh(self):
        if self.datasource is not None:
            self.pool = []
            self.pool.extend(self.datasource.get(self.poolsize))

    def append(self, proxy, sort=False):
        self.pool.append(proxy)
        if sort is True:
            self.pool.sort(
                key=lambda o: o.weight, reverse=True,
            )

    def proxy(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(self.tries):
                try:
                    params = dict()
                    params['proxy'] = host = self.peek()
                    params.update(kwargs)
                    res = func(*args, **params)
                except (exceptions.ConnectTimeout, exceptions.ConnectionError):
                    sys.stderr.write('retry...\n')
                    self.remove(host)
                    time.sleep(0.5)
                    continue
                return res
        return wrapper


if __name__ == '__main__':
    pass
