# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function

import sys
import csv
import traceback
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
    '''代理池对象, 非线程安全。'''

    def __init__(self, max_size=None, strategy=None):
        '''
        初始化代理池。

        Args:
            max_size (int): 指定代理池容量, None - 不限容量。
            strategy (ProxyFetchStrategy): 从代理池取代理的策略。

        Returns:
            None
        '''
        self._max_size = max_size
        self._pool = deque(maxlen=max_size)
        self._strategy = strategy(self._pool)

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
            proxy = self._strategy.fetch()
            if requests_style is True:
                proxy = {schema_type2schema[proxy['schema']]: proxy['url']}
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
        assert proxy['schema'] in SchemaType.ALL_AVALIABLE_VALUES
        if 'url' not in proxy:
            proxy['url'] = self.format_proxy(proxy)
        self._pool.append(proxy)

    def load_from_csv(
            self,
            csv_file,
            columns=None,
            delimiter=',',
            quotechar='|',
    ):
        '''
        从CSV文件中加载代理。

        Args:
            csv_file (str): 指定CSV文件路径。
            columns (list): 指定CSV文件的列名。
            delimiter (str): 指定CSV文件的分隔符，默认为逗号（comma）。
            quotechar (str): 引用字符，默认为'|'。

        Returns:
            None
        '''
        try:
            with open(csv_file, 'rb') as f:
                if columns is None:
                    columns = ['schema', 'user', 'password', 'host', 'port']
                reader = csv.reader(
                    f, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC)  # noqa
                for row in reader:
                    proxy = dict()
                    for k, idx in zip(columns, range(len(columns))):
                        v = row[idx]
                        if isinstance(v, float):
                            v = int(v)
                        proxy[k] = v
                    self.push(proxy)
        except IOError:
            traceback.print_exc(file=sys.stderr)

    def iteritems(self, requests_style=False):
        try:
            while True:
                yield self.fetch(requests_style)
        except:
            raise StopIteration()


class ProxyFetchStrategy(object):
    '''
    代理获取策略。'''

    def fetch(self):
        raise NotImplementedError()


class ProxyCycleFetchStrategy(ProxyFetchStrategy):
    '''队列轮询策略。'''

    def __init__(self, pool):
        '''
        构造队列轮询策略。

        Args:
            pool (deque): 代理池。
        '''
        super(ProxyCycleFetchStrategy, self).__init__()
        self._pool = pool
        self._pos = 0

    def fetch(self):
        self._pos = self._pos % len(self._pool)
        element = self._pool[self._pos]
        self._pos += 1
        return element


if __name__ == '__main__':
    pass
