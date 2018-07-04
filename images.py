#!/usr/bin/python
#coding=utf-8

import os
import re
import sys
import threading
import Queue
import uuid
from PIL import Image
from StringIO import StringIO
import util

reload(sys)
sys.setdefaultencoding('utf-8')

def read_file(file_path):
    units = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                unit = line.split()
                unit = re.split(r'\t+', line)
                units.append(unit)
    return units

class imageProcess(threading.Thread):
    """
    image 处理线程
    """
    def __init__(self, ratio, unit_queue, threading_lock, result_file_path, failed_file_path):
        super(self.__class__, self).__init__()
        self.url_list = []
        self.ratio = ratio
        self.unit_queue = unit_queue
        self.threading_lock = threading_lock
        self.result_file_path = result_file_path
        self.failed_file_path = failed_file_path

    def run(self):
        while True:
            try:
                self.url_list = self.unit_queue.get(block = True, timeout = 1)
            except Queue.Empty:
                break
            good_unit = True
            index = 0
            for url in self.url_list:
                if url.startswith('http'):
                    index = index + 1
                    #file_path = "/tmp/" + str(uuid.uuid1())
                    #self_lib.NetUtil.request_get(url, file_path)
                    content = util.NetUtil.request_get(url)
                    if content is not None:
                        if not self._cmp_ratio(content, url):
                            content = None  #释放引用，避免内存泄漏.
                            good_unit = False
                            self.url_list.append("第" + str(index) + "张图片不符合")
                            break
                    else:
                        good_unit = False
                        self.url_list.append("第" + str(index) + "张图片下载失败")
                        print "%s download failed, file_path is not exists." % url
                        break
            if good_unit:
                self._write_success()
            else:
                self._write_failed()
            self.unit_queue.task_done()
        print self.getName() + " have finished."

    def _cmp_ratio(self, content, url):
        img = Image.open(StringIO(content))
        print url + ": "
        print img.size
        return max(img.size) >= max(self.ratio) and min(img.size) >= min(self.ratio)

    def _write_success(self):
        """
        写文件
        """
        line = '\t'.join(self.url_list)
        while self.threading_lock.locked():
            continue
        self.threading_lock.acquire()
        with open(self.result_file_path, 'a') as fr:
            fr.write("%s\n" % line)
        self.threading_lock.release()

    def _write_failed(self):
        """
        写文件
        """
        line = '\t'.join(self.url_list)
        while self.threading_lock.locked():
            continue
        self.threading_lock.acquire()
        with open(self.failed_file_path, 'a') as fr:
            fr.write("%s\n" % line)
        self.threading_lock.release()



if __name__ == "__main__":
    source_file = ""
    target_file = ""
    failed_target_file = ""
    threading_num = 10
    ratio = (2270, 3500)
    try:
        units = read_file(source_file)
        unit_queue = Queue.Queue(len(units))
        for unit in units:
            unit_queue.put(unit)
        threading_lock = threading.Lock()
        for i in range(0, threading_num):
            image_thread = imageProcess(ratio, unit_queue, threading_lock, target_file, failed_target_file)
            image_thread.start()
        unit_queue.join()
    except Exception as e:
        print e.message
    finally:
        print "done"

