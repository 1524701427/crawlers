# -*- coding: utf-8 -*-

import time
import random
import binascii
from functools import wraps
from collections import deque
from abc import ABCMeta, abstractmethod

from requests import exceptions


class DataSource(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, count):
        raise NotImplementedError()

    @abstractmethod
    def stream(self):
        raise NotImplementedError()

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        raise StopIteration()


class Proxy(object):

    def __init__(
            self, host, port,
            schema='http', user='', passwd='', weight=0):
        self.schema = schema
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.weight = weight

    def __hash__(self):
        identifier = filter(
            None,
            [self.schema, self.host, str(self.port), self.user, self.passwd])
        identifier = ','.join(identifier)
        return binascii.crc32(identifier)

    def __repr__(self):
        return '<%s object at 0x%x>' % (
            self.__class__.__name__, id(self),
        )

    def __str__(self):
        auth_part = ''
        if self.user and self.passwd:
            auth_part = '%s:%s@' % (self.user, self.passwd)
        return '%s://%s%s:%d' % (self.schema, auth_part, self.host, self.port)

    def __getitem__(self, key):
        return self.__getattribute__(key)


class ProxyPool(object):

    def __init__(
            self, datasource, poolsize=30, **options):
        assert datasource
        self.poolsize = poolsize
        self.tries = options.get('tries', 3)
        self.datasource = datasource
        self.pool = deque()

    def _sort(self, reverse=True):
        self.pool.sort(
            key=lambda o: o.weight, reverse=reverse,
        )

    def peek(self):
        if not self.pool:
            raise IndexError()
        return random.choice(self.pool)

    def remove(self, item):
        self.pool.remove(item)

    def pop(self):
        self.pool.popleft()

    def refresh(self):
        if self.datasource is not None:
            stream = self.datasource.stream()
            self.pool = deque()
            for i in xrange(self.poolsize):
                proxy = next(stream)
                self.pool.append(proxy)
            self._sort

    def append(self, proxy, sort=False):
        self.pool.append(proxy)
        if sort is True:
            self._sort()

    def proxy(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = None
            for i in range(self.tries):
                try:
                    params = dict()
                    params['proxy'] = host = self.peek()
                    params.update(kwargs)
                    res = func(*args, **params)
                    break
                except (exceptions.ConnectTimeout, exceptions.ConnectionError):
                    time.sleep(0.5)
                    continue
            else:
                self.pool.remove(host)
            return res
        return wrapper


if __name__ == '__main__':
    pass
