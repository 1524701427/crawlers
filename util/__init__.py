# -*- coding: utf-8 -*-

import sys


def error(msg, *args):
    sys.stderr.write('%s\n' % (msg % args))
