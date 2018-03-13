# -*- coding: utf-8 -*-

"""常用装饰器。"""

from __future__ import print_function

import time
import functools
import fcntl
import os


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        t1 = time.time()
        print(">>>", t1 - t0)
        return res
    return wrapper


def singleton(pid_filename):
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
