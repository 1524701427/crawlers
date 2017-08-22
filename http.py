# -*- coding: utf-8 -*-

"""通用爬虫Http客户端实现。"""

from __future__ import with_statement
from __future__ import print_function

import sys
import time
import traceback
import urllib
import urlparse

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects,
)

from core.exceptions import ProxyUnavaliableError

__version__ = '1.0.0'
__author__ = 'gatsby'
__email__ = 'dreamcatchwang1991@gmail.com'

try:
    import gevent
    sleep = gevent.sleep
except ImportError:
    sleep = time.sleep
    sys.stderr.write(traceback.format_exc())


class CrawlerHttpClient(object):
    '''初始化爬虫客户端。

    Args:
        default_headers (dict): 默认HTTP头信息。
        timeout (int): 默认请求超时时间，单位：秒。
        tries (int): 请求资源失败，重试次数。
        try_internal (int): 请求资源失败，重试间隔。
        proxies_pool (ProxyPool): 代理池对象。
    '''

    def __init__(
            self,
            default_headers=None,
            timeout=10,
            tries=3,
            try_internal=1,
            proxies_pool=None,
    ):
        self._tries = tries
        self._try_internal = try_internal
        self._timeout = timeout
        self._proxies_pool = proxies_pool
        if self._proxies_pool is not None:
            self._generator = \
                self._proxies_pool.iteritems(requests_style=True)

        self._last_active_time = int(time.time())
        self._count = 0

        self._s = requests.Session()
        self._s.max_redirects = 10  # 最大允许10次重定向

        if default_headers is not None:
            self._s.headers.update(default_headers)

    def get(self, url, data=None, timeout=None):
        '''
        获取URL标识的资源实体。

        Args:
            url (str): 标识资源实体的URL。
            data (dict): 请求参数。
            timeout (int): 请求超时时间。

        Returns:
            requests.Response: requests.Response对象。
        '''
        if not url.lower().startswith('http'):
            url = urlparse.urljoin(self._base_url, url)

        if data is not None:
            url = url + '?' + urllib.urlencode(data)

        proxies = None
        if hasattr(self, '_generator'):
            proxies = next(self._generator)

        req = requests.Request('GET', url=url)
        prepared_req = req.prepare()

        self.before_request(prepared_req)

        for i in range(self._tries):
            try:
                resp = self._s.send(
                    prepared_req,
                    proxies=proxies,
                    timeout=timeout or self._timeout,
                    allow_redirects=self._allow_redirects,
                )
                break

            except (ConnectionError, Timeout):
                sleep((i+1)*self._try_internal)
                continue

            except (HTTPError, TooManyRedirects):
                raise RuntimeError('Unavaliable url...')
        else:
            if proxies is not None:
                # TODO: add code. 向代理池反馈代理的可用性。
                raise ProxyUnavaliableError()
            raise RuntimeError('Bad network...')
        self.after_request(self._s, resp)

        return resp

    def before_request(self, prepared_req):
        '''
        Hook函数，每次HTTP请求前被调用。

        Args:
            prepared_req (requests.PreparedRequest): requests PreparedRequst对象。

        Returns:
            None
        '''
        pass

    def after_request(self, session, resp):
        '''
        Hook函数，每次HTTP请求后备调用。

        Args:
            session (requests.Session): requests Session对象。
            resp (requests.Response): requests.Response对象。

        Returns:
            None
        '''
        pass

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def login(
            self,
            user,
            password,
            captcha_recognize_callback=None,
            force=False,
    ):
        '''
        登录系统。

        Args:
            user (str): 登录账户。
            password (str): 登录密码。
            captcha_recognize_callback (method): 识别登录验证码的回调函数。
            force (bool): 默认login为lazy模式，force强制登录。

        Returns:
            bool: 标识是否登录成功。
        '''
        return True


if __name__ == '__main__':
    pass
