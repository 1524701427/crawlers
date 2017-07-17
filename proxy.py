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
