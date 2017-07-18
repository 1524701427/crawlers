# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function

from collections import deque

from core.enum import Enum
from core.exceptions import ProxyPoolEmptyError


class SchemaType(Enum):
    '''schema类型。'''
    HTTP = 0  # HTTP协议
    HTTPS = 1  # HTTPS协议

schema_type2schema = {
    SchemaType.HTTP: 'http',
    SchemaType.HTTPS: 'https',
}


class ProxyPool(object):
    '''代理池对象'''

    def __init__(self, max_size=None, strategy=None):
        '''
        初始化代理池。

        Args:
            max_size (int): 指定代理池容量, None - 不限容量。
            strategy (object): 从代理池取代理的策略。

        Returns:
            None
        '''
        self._max_size = max_size
        self._pool = deque(maxlen=max_size)
        self._strategy = strategy

    @classmethod
    def format_proxy(self, proxy):
        '''
        将proxy格式化为http://user@pass:host:port的格式。

        Args:
            proxy (dict): 代理。

        Returns:
            str - 代理。
        '''
        schema = schema_type2schema[proxy['schema']]
        auth_part = ''
        if 'user' in proxy and 'password' in proxy:
            auth_part = '%s@%s:' % (proxy['user'], proxy['password'])
        port_part = ''
        if 'port' in proxy:
            port_part = ':%d' % proxy['port']
        return ''.join([schema, '://', auth_part, proxy['host'], port_part])

    def fetch(self, requests_style=False):
        '''
        从代理池中获取一个代理。

        Args:
            requests_style (bool): 是否使用requests风格的proxy。

        Returns:
            dict: 描述代理的字典。
        '''
        try:
            pass
        except IndexError:
            raise ProxyPoolEmptyError()

    def push(self, proxy, **kwargs):
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


def ProxyFetchStrategy(object):
    '''
    代理获取策略。'''
    pass


class ProxyCycleFetchStrategy(ProxyFetchStrategy):
    '''队列轮询策略。'''

    def __init__(self, pool):
        '''
        构造队列轮询策略。

        Args:
            pool (deque): 代理池。
        '''


if __name__ == '__main__':
    pool = ProxyPool()
    pool.push(dict(schema=1, host='127.0.0.1', port=9000))
    print(pool.fetch(requests_style=True))
