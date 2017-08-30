#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""爬取it桔子项目的爬虫。"""

from util import error
from util.cache import Cache


cache = Cache()


def get_last_id():
    return cache.itjuzi.last_id


def set_last_id(last_id):
    cache.itjuzi.last_id = last_id
