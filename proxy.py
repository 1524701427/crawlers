# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function

from collections import deque


class ProxyPoolEmptyError(StandardError):
    '''代理池为空。'''
    pass


class ProxyPool(object):
    '''代理池对象'''

    def __init__(self, max_size=None):
        '''
        初始化代理池。

        Args:
            max_size (int): 指定代理池容量。

        Returns:
            None
        '''
        self._max_size = max_size
        self._pool = deque(maxlen=max_size)

    def fetch(self):
        '''
        获取代理。'''
