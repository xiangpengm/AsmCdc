import os
import sys
import time
import random
import webview
import threading
from hashlib import md5
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import json


def load(file, tp='r'):
    with open(file, tp) as f:
        return f.read()


class Global(object):
    total = 0
    current = 0
    mutex = threading.Lock()

    @classmethod
    def setTotal(cls, value):
        cls.mutex.acquire()
        cls.total = value
        cls.mutex.release()

    @classmethod
    def addCurrent(cls):
        cls.mutex.acquire()
        cls.current += 1
        cls.mutex.release()
    
    @classmethod
    def reset(cls):
        cls.mutex.acquire()
        cls.total = 0
        cls.current = 0
        cls.mutex.release()


class Api:

    def __init__(self):
        self.itemList = []
        self.pool = ThreadPool(2)

    def getCount(self, params):
        if Global.total == 0:
            return "noTask"
        elif Global.current == Global.total:
            Global.reset()
            return 1
        else:
            return Global.current/Global.total

    def getFilePath(self, params):
        result = window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=True,
        )
        if result is None:
            return "None"
        else:
            # 重置
            Global.reset()
            fileList = []
            total = 0
            for f in os.listdir(result[0]):
                if f.endswith('.gz'):
                    filePath = os.path.join(result[0], f)
                    fileList.append((f, filePath))
                    total += 1
            Global.setTotal(total)
            self.resetItemList()
            # todo 改成进程池
            for f, filePath in fileList:
                self.pool.apply_async(self.getFileMD5, (filePath, ))
            return {
                "path": result[0], 
                "total": total
            }

    def getOutputPath(self, params):
        result = window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=True,
        )
        if result is None:
            return "None"
        else:
            return result[0]

    def getFileData(self, param):
        print("itemlist:", self.itemList)
        r = []
        for index, cell in enumerate(self.itemList):
            item = {
                "id": index+1,
                "name": os.path.basename(cell[0]),
                "hash": cell[1],
            }
            r.append(item)
        return json.dumps(r, ensure_ascii=False)

    def getFileMD5(self, file):  # check大文件的MD5值
        print('run check md5 sum', threading.current_thread().name)
        m = md5()
        f = open(file, 'rb')
        buffer = 8192
        while 1:
            chunk = f.read(buffer)
            if not chunk:
                break
            m.update(chunk)
        f.close()
        Global.addCurrent()
        self.itemList.append((file, m.hexdigest()))

    def resetItemList(self):
        self.itemList = []


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'CDC Assembly Client', 
        html=load("templates/index.html"), 
        js_api=api,
        min_size=(720, 540)
    )
    webview.start()
