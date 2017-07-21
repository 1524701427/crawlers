# -*- coding: utf-8 -*-

import os
import shevle


class CacheFile(object):
    """缓存文件对象。

    Args:
        cache_dir (str): 文件所在目录。
        cache_file_name (str): 文件名称，不带扩展名。

    Returns:
        None
    """
    def __init__(self, cache_dir, cache_file_name):
        self._cache_dir = os.path.abspath(cache_dir)
        self._cache_file_name = cache_file_name
        self._cache = shevle.open(
            os.path.join(cache_dir, cache_file_name))

    def flush(self):
        """将数据刷新到缓存文件中。
        """
        self._cache.sync()

    def __setitem__(self, k, v):
        """代理shevle。"""
        self._cache[k] = v

    def __getitem__(self, k):
        """代理shevle。"""
        return self._cache[k]

    def __del__(self):
        """关闭Cache文件。"""
        self._cache.close()


class Cache(object):
    """爬虫缓存系统。

    Args:
        cache_dir (str): 缓存数据的目录。

    Returns:
        None
    """

    def __init__(self, cache_dir="./"):
        if not os.path.exists(cache_dir):
            os.mkdir(os.path.join(cache_dir, ".cache"))
        self._cache_dir = cache_dir
        self._object_cache = dict()

    def __getattr__(self, attr):
        """通过属性来访问相应APP。

        Args:
            attr (str): 属性名，一般是爬虫APP名，如itjuzi。

        Returns:
            None
        """
        if attr in self._object_cache:
            return self._object_cache[attr]
        cache = CacheFile(self._cache_dir, attr)
        self._object_cache[attr] = cache
        return cache
