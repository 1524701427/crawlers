# -*- coding: utf-8 -*-

"""随机返回一个User-Agent。"""

from __future__ import print_function


class DeviceType:
    """设备类型。"""
    PC = 0
    MOBILE = 1


class UAPool(object):

    default_ua_list_file = {
        DeviceType.PC: './data/pc.txt',
        DeviceType.MOBILE: './data/mobile.txt'
    }

    def __init__(self, device_type, ua_list_file=None):
        assert device_type in (0, 1)
        self.device_type = device_type
        self.ua_list_file = ua_list_file or self.default_ua_list_file[device_type]  # noqa: E501
        self.pool = []
        self.pos = 0
        self.load()

    def load(self):
        try:
            with open(self.ua_list_file, 'rt') as f:
                for line in f:
                    line = line.strip()
                    self.pool.append(line)
        except IOError:
            print('====OPEN FILE FAILED.')

    def pick(self):
        if not self.pool:
            raise StandardError(u'Empty UA list.')
        ua = self.pool[self.pos % len(self.pool)]
        self.pos += 1
        return ua


if __name__ == '__main__':
    pool = UAPool(DeviceType.PC)
    for i in range(5):
        print('>>>', pool.pick())
