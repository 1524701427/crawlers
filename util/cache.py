# -*- coding: utf-8 -*-

import os
import shelve

from core.metaclass import Final


class CacheFile(object):
    """缓存文件对象。

    Args:
        cache_dir (str): 文件所在目录。
        cache_file_name (str): 文件名称，不带扩展名。

    Returns:
        None
    """
    def __init__(self, cache_dir, cache_file_name):
        self._cache_dir = cache_dir
        self._cache_file_name = cache_file_name
        self._cache = shelve.open(
            os.path.join(cache_dir, cache_file_name),
            flag='c', protocol=2, writeback=True,
        )

    def flush(self):
        """将数据刷新到缓存文件中。 """
        self._cache.sync()

    def __getattr__(self, attr):
        """支持通过'.'访问成员。"""
        return self._cache[attr]

    def __setattr__(self, attr, value):
        """支持通过'.'设置成员值。"""
        if attr.startswith('_'):
            super(CacheFile, self).__setattr__(attr, value)
        else:
            self._cache[attr] = value

    def __setitem__(self, k, v):
        """代理shevle。"""
        self._cache[k] = v

    def __getitem__(self, k):
        """代理shevle。 """
        return self._cache.get(k)

    def __del__(self):
        """关闭Cache文件。 """
        self._cache.close()


class Cache(object):
    """爬虫缓存系统。

    Args:
        cache_dir (str): 缓存数据的目录。

    Returns:
        None

    Demo:
        >> cache = Cache()
        >> cache.itjuzi['last_id'] = '1000'
        >> cache.itjuzi.flush()
        >> print(cache.itjuzi['last_id'])
    """
    __metaclass__ = Final

    def __init__(self, cache_dir="./"):
        cache_dir = os.path.join(os.path.abspath(cache_dir), '.cache')
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
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
        else:
            cache = CacheFile(self._cache_dir, attr)
            self._object_cache[attr] = cache
            return cache

    def __del__(self):
        """析构方法，关闭所有Cache文件。"""
        for _, v in self._object_cache.items():
            del v

if __name__ == "__main__":
    cache = Cache()
    cache.itjuzi['last_id'] = 0
    cache.itjuzi.last_id = 1000
    cache.itjuzi.flush()
