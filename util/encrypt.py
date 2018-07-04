#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
加密
"""
import os
import hashlib
import base64
import uuid

class Encrypt(object):
    """
    静态加密类
    """

    TOKEN_SALT = 'zxc'

    @staticmethod
    def get_post_token(ts):
        return Encrypt.get_str_md5(Encrypt.TOKEN_SALT + ts)

    @staticmethod
    def get_file_md5(filename):
        """
        文件路径，获取前8096个字节用于加密获得md5
        :return:
        """
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = file(filename,'rb')
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    @staticmethod
    def get_str_md5(str):
        """
        获取字符串md5
        """
        m2 = hashlib.md5()
        m2.update(str)
        return m2.hexdigest()

    @staticmethod
    def base64_url_decode(inp):
        """
        base64 解码
        """
        import base64
        return base64.urlsafe_b64decode(str(inp + '=' * (4 - len(inp) % 4)))

    @staticmethod
    def base64_url_encode(inp):
        """
        base64 编码
        """
        import base64
        return base64.urlsafe_b64encode(str(inp)).rstrip('=')

    @staticmethod
    def get_uuid1():
        """
        获取uuid
        """
        return str(uuid.uuid1())
