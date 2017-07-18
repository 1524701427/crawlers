# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function

from random import randint
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

schema_type2schema = {
    SchemaType.HTTP: 'http',
    SchemaType.HTTPS: 'https',
}


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

    def fetch(self, random=True, requests_style=False, remove=False):
        '''
        从代理池中获取一个代理。

        Args:
            random (bool): 是否随机获取。
            requests_style (bool): 是否使用requests风格的proxy。
            remove (bool): 是否从代理池中取走。

        Returns:
            dict: 描述代理的字典。
        '''
        try:
            index = 0
            if random is True and len(self._pool):
                index = randint(0, len(self._pool)-1)
            proxy = self._pool[index]
            if remove is True:
                del self._pool[index]
            if requests_style is True:
                proxy = {schema_type2schema[proxy['schema']]: self.format_proxy(proxy)}  # noqa
            return proxy
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


if __name__ == '__main__':
    pool = ProxyPool()
    pool.push(dict(schema=1, host='127.0.0.1', port=9000))
    print(pool.fetch(requests_style=True))
