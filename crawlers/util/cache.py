# -*- coding: utf-8 -*-

"""本地缓存系统实现。"""

import os
import shelve

from core.metaclass import Final


class CacheFile(object):

    def __init__(self, cache_dir, cache_filename, default_values=None):
        self._cache_dir = cache_dir
        self._cache_filename = cache_filename
        self._default_values = default_values or dict()
        self._cache = shelve.open(
            os.path.join(self._cache_dir, self._cache_filename),
            flag='c',
            protocol=2,
            writeback=True)

    def flush(self):
        self._cache.sync()

    def __getattr__(self, attr):
        return self._cache[attr] if attr in self._cache else self._default_values[attr]  # noqa: E501

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            super(CacheFile, self).__setattr__(attr, value)
        else:
            self._cache[attr] = value

    def __setitem__(self, k, v):
        self._cache[k] = v

    def __getitem__(self, k):
        return self._cache.get(k)

    def __del__(self):
        self._cache.close()


class Cache(object):

    __metaclass__ = Final

    def __init__(self, cache_dir="./", default_values=None):
        cache_dir = os.path.join(os.path.abspath(cache_dir), '.cache')
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir, 777)
        self._cache_dir = cache_dir
        self._caches = dict()
        self._default_values = default_values or dict()

    def __getattr__(self, attr):
        if attr in self._caches:
            return self._caches[attr]
        else:
            cache = CacheFile(self._cache_dir, attr, self._default_values.get(attr))  # noqa: E501
            self._caches[attr] = cache
            return cache

    def clear(self, cache=None, ignore_error=False):
        if cache is None:
            for _, v in self._caches.items():
                del v
            __import__('shutil').rmtree(self._cache_dir)
        else:
            try:
                v = self._caches.get(cache)
                if v is not None:
                    del v
                os.remove(os.path.join(self._cache_dir, '%s.db' % cache))
            except IOError:
                if ignore_error is not True:
                    raise


if __name__ == "__main__":
    pass
