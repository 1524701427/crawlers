#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
枚举类型的Python实现。'''

from __future__ import print_function

import re


class EnumMeta(type):
    '''
    枚举类型，元类，枚举类型的成员变量（类的属性）必须为大写格式。'''
    pattern = re.compile(r'^[A-Z]+$')

    def __new__(metacls, cls, bases, namespace):
        attr2value = dict()
        for k, v in namespace.iteritems():
            if k.startswith('_'):
                continue
            attr2value[k] = v
            if not metacls.pattern.match(k):
                raise AttributeError('%s should be written in upper case.' % k)
            if not isinstance(v, (int, long)):
                raise ValueError('only int/long.')
        attr2value['ALL_AVALIABLE_VALUES'] = sorted(attr2value.values())

        return type.__new__(metacls, cls, bases, attr2value)


class Enum(object):

    __metaclass__ = EnumMeta
