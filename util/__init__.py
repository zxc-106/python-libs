#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide ....
"""

from util.log import Logger
from util.encrypt import Encrypt
from util.netUtil import NetUtil
from util.cmd import Cmd


def ignore_exception(fn):
    """忽略异常的装饰器
    """
    def _wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            Logger.w('catch exception in ' + fn.__name__)
            Logger.w(e)
            Logger.w('ignore exception')
            return None
    return _wrapped
