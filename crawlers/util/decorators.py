# -*- coding: utf-8 -*-

"""常用装饰器。"""

from __future__ import print_function

import time
import functools
import traceback
import fcntl
import os

from util.mail import mail_multipart


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        t1 = time.time()
        print("time coast: ", t1 - t0)
        return res
    return wrapper


def singleton(pid_filename):
    """单例模式"""
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            pid = str(os.getpid())
            pidfile = open(pid_filename, 'a+')
            try:
                fcntl.flock(pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                return
            pidfile.seek(0)
            pidfile.truncate()
            pidfile.write(pid)
            pidfile.flush()
            pidfile.seek(0)

            ret = f(*args, **kwargs)

            try:
                pidfile.close()
            except IOError, err:
                if err.errno != 9:
                    return
            os.remove(pid_filename)
            return ret
        return decorated
    return decorator


def retry(times=3):
    """重试执行"""
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            res = None
            if times <= 0:
                return res
            for i in range(times):
                try:
                    res = f(*args, **kwargs)
                except:
                    print('retry...')
                    continue
            else:
                print('retry failed...')
            return res
        return decorated
    return decorator


def caught_exception(receipts, subject=u'爬虫异常'):
    """捕获异常"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                res = f(*args, **kwargs)
                return res
            except:
                email = dict()
                email['to'] = receipts
                email['subject'] = subject
                email['html'] = traceback.format_exc()
                mail_multipart(email)
        return wrapper
    return decorator
