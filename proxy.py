# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function

from random import choice
from collections import deque


class ProxyUnavaliableError(StandardError):
    '''
    代理不可用。'''
    pass


class ProxyPoolEmptyError(StandardError):
    '''代理池为空。'''
    pass


class SchemaType:
    '''schema类型。'''
    ALL = 0  # 全部类型
    HTTP = 1  # HTTP协议
    HTTPS = 2  # HTTPS协议


class ProxyPool(object):
    '''代理池对象'''

    def __init__(self, max_size=None):
        '''
        初始化代理池。

        Args:
            max_size (int): 指定代理池容量, None - 不限容量。

        Returns:
            None
        '''
        self._max_size = max_size
        self._pool = deque(maxlen=max_size)

    def fetch(self, random=True):
        '''
        从代理池中获取一个代理。

        Args:
            random (bool): 是否随机获取。
        '''
        try:
            if random is True:
                proxy = choice(self._pool)
            else:
                proxy = self._pool.pop_left()
            return proxy
        except IndexError:
            raise ProxyPoolEmptyError()

    def push(self, proxy):
        '''
        向代理池中增加一个代理。

        Args:
            proxy (dict): 代表代理的字典。

        Returns:
            None

        Demo:
            >> pool = ProxyPool()
            >> proxy = dict(
            >>      schema=SchemaType.HTTP, host='127.0.0.1', port=9000,
            >>      user='user', password='password')
            >> pool.push(proxy)

        '''
        self._pool.append(proxy)
