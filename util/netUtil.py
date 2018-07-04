#!/usr/bin/python
#coding=utf-8

import os
import sys
import time
import json
import requests
import urllib2
import util
from requests import exceptions

class NetUtil(object):

    @staticmethod
    def get_post_common_params():
        ts = int(time.time())
        ts = str(ts)
        token = util.Encrypt.get_post_token(ts)
        params = {'token': token, 'ts': ts}
        return params

    @staticmethod
    def request_get(url, file_path=None):
        """
        download
        :param url:
        :param file_path:
        :return:
        """
        content = None
        retry_times = 5
        while retry_times > 0:
            try:
                res = requests.get(url, timeout=(10, 60))
                content = res.content
                if file_path is not None:
                    with open(file_path, 'wb') as f:
                        f.write(res.content)
                break
            except exceptions.ConnectionError:
                print "%s download connectionError." % url
                retry_times = retry_times - 1
                time.sleep(10)
            except exceptions.Timeout:
                print "%s download timeout 60s." % url
                retry_times = retry_times - 1
                time.sleep(10)
            except Exception:
                print "%s download exception." % url
                retry_times = retry_times - 1
                time.sleep(10)
        return content

    @staticmethod
    def urllib_post_json(url, data):
        """
        post json
        :param url:
        :param data:
        :return:
        """
        retry_times = 5
        content = {'net_error': 1, 'log': ''}
        while retry_times > 0:
            try:
                headers = {'Content-Type': 'application/json'}
                request = urllib2.Request(url, headers=headers, data=json.dumps(data))
                response = urllib2.urlopen(request, timeout=60)
                if response.getcode() == 200:
                    content = json.loads(response.read())
                    break
            except Exception as inst:
                print "%s post json failed." % url
                retry_times = retry_times - 1
                content['log'] = inst.message
                time.sleep(10)
        return content
