# -*- coding: utf-8 -*-

from __future__ import print_function


class ProxyError(StandardError):
    '''
    代理异常基类。'''
    def __init__(self, detail):
        super(ProxyError, self).__init__(self, detail)


class ProxyUnavaliableError(ProxyError):
    '''
    代理不可用。'''
    pass


class ProxyPoolEmptyError(ProxyError):
    '''代理池为空。'''
    pass


class ProxyTooLittleError(ProxyError):
    '''代理池中代理数量过少。'''
    pass
