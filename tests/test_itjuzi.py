#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""自动化测试脚本。"""

import nose

from export.itjuzi_copy import get_last_id
from export.itjuzi_copy import set_last_id


def setup():
    pass


def teardown():
    pass


@nose.with_setup(setup, teardown)
def test_set_last_id():
    last_id = 1000
    set_last_id(last_id)


@nose.with_setup(setup, teardown)
def test_get_last_id():
    ret = get_last_id()
    nose.tools.assert_equals(ret, 1000)


if __name__ == '__main__':
    nose.run()
