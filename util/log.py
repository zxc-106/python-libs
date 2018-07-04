#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Logger
Created by zxc
"""

import os
import sys
import logging
import traceback

class Logger(object):
    logger = {}
    formatter = logging.Formatter('[%(asctime)s](%(levelname)s)%(name)s:%(message)s')

    @staticmethod
    def createLogger(name='default', file_path='default_'):
        if not Logger.logger.has_key(name):
            if name == 'default':
                _logger = logging.getLogger()
                fileHandler = logging.FileHandler(file_path + name + ".log")
                fileHandler.setFormatter(Logger.formatter)
            else:
                _logger = logging.getLogger(name)
                fileHandler = logging.FileHandler(file_path + name + ".log")
                # fileHandler.setFormatter(Logger.formatter)
            _logger.addHandler(fileHandler)
            _logger.setLevel(logging.DEBUG)
            Logger.logger[name] = _logger
        return Logger.logger[name]

    @staticmethod
    def getLogger(name='default'):
        if not Logger.logger.has_key(name):
            Logger.createLogger(name)
        return Logger.logger[name]

    @staticmethod
    def close():
        for name, log in Logger.logger.items():
            for hd in log.handlers:
                if hd is not None:
                    log.removeHandler(hd)
                    hd.flush()
                    hd.close()

    @staticmethod
    def d(msg, name='default'):
        Logger.getLogger(name).debug(msg)

    @staticmethod
    def i(msg, name='default'):
        Logger.getLogger(name).info(msg)

    @staticmethod
    def w(msg, name='default'):
        Logger.getLogger(name).warn(msg)
        Logger.getLogger(name).warn(traceback.format_exc())

    @staticmethod
    def e(msg, name='default'):
        Logger.getLogger(name).error(msg)
        Logger.getLogger(name).error(traceback.format_exc())
