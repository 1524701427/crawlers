#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
枚举类型的Python实现。'''

import re


class EnumMeta(type):
    '''
    枚举类型，元类，枚举类型的成员变量（类的属性）必须为大写格式。'''
    pattern = re.compile(r'^[A-Z]+$')

    def __new__(metacls, cls, bases, values):
        attr2value = dict()
        for k, v in values.iteritems():
            if k.startswith('_'):
                continue
            attr2value[k] = v
            if not metacls.pattern.match(k):
                raise AttributeError('%s should be written in upper case.' % k)
        attr2value['ALL_AVALIABLE_VALUES'] = attr2value.values()

        return type.__new__(metacls, cls, bases, attr2value)


class Enum(object):

    __metaclass__ = EnumMeta


if __name__ == '__main__':
    o = Enum()
    print o.ALL_AVALIABLE_VALUES
