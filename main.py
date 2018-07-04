#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import sys
import time
import json
import shutil
import argparse
import signal

import util

reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

def load_config(config_file):
    """载入config配置
    """
    params = None
    try:
        if os.path.exists(config_file):
            f = file(config_file)
            params = json.load(f)
    except Exception as e:
        util.Logger.w(e)
        #exit(-1)
    return params


def parse_argv():
    """解析命令行参数
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config',
            help='config file for test',
            metavar='CONFIG_FILE')
    parser.add_argument('-p', '--path', dest='appPath',
            help='input the app path which tested',
            metavar='APP_PATH')
    parser.add_argument('-t', '--run_time', type=int, dest='runTime',
            help='time, default is 180s', default=180)
    params = vars(parser.parse_args())
    if params['config'] is not None:
        extraParams = load_config(params['config'])
        if extraParams is not None:
            for key in extraParams:
                params[key] = extraParams[key]
    if params['appPath'] is None:
        print 'appPath required'
        parser.print_help()
        exit(-1)
    return params

if __name__ == '__main__':
    try:
        params = parse_argv()
        util.Logger.i('app path is : %s' % params['appPath'])
    except Exception as e:
        util.Logger.e(e)
        raise e
    finally:
        util.Logger.close()
        with open('./done', 'w') as f:
            f.write('done')
