# -*- coding: utf-8 -*-

import requests
from gevent import monkey
monkey.patch_all()  # noqa

from proxy import Proxy, ProxyPool

UA = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
    'Safari/537.36'
)


pool = ProxyPool()
pool.append(Proxy('106.46.136.46', 808))


class HttpClient(object):

    def __init__(self):
        self.session = requests.Session()

    @pool.proxy
    def fetch(self, url, method='GET', data=None, **options):
        params = dict()
        params['data'] = data
        params['headers'] = options.get('headers')
        params['cookies'] = options.get('cookies')
        req = requests.Request(method, url, **params)
        req = self.session.prepare_request(req)
        req.headers['User-Agent'] = UA
        proxy = options.get('proxy')
        if proxy is not None:
            proxy = {
                proxy.schema: '%s://%s:%d' % (
                    proxy.schema, proxy.host, proxy.port),
            }
        resp = self.session.send(req, proxies=proxy)
        return resp


if __name__ == '__main__':
    client = HttpClient()
    resp = client.fetch('http://www.baidu.com')
    print resp.text
