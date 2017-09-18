# -*- coding: utf-8 -*-

'''
常用装饰器。'''

import time
import functools


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        t1 = time.time()
        print(t1 - t0)
        return res
    return wrapper
