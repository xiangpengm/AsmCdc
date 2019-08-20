# 
import os
import sys
import time
import random
import webview
import threading
from hashlib import md5
import asyncio

# 
from page import html


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
            return {"message": "error"}
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
            for f, filePath in fileList:
                t = threading.Thread(target=self.getFileMD5, args=(filePath, ))
                t.start()
            return [result[0], total]

    def getOutputPath(self, params):
        result = window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=True,
        )
        if result is None:
            return {"message": "error"}
        else:
            return result[0]

    def getFileData(self, param):
        return self.itemList

    def getFileMD5(self, file):  # check大文件的MD5值
        print('start thread', file)
        m = md5()
        f = open(file, 'rb')
        buffer = 8192    # why is 8192 | 8192 is fast than 2048
        while 1:
            chunk = f.read(buffer)
            if not chunk:
                break
            m.update(chunk)
        f.close()
        Global.addCurrent()
        print(file, m.hexdigest(), 'done')
        self.itemList.append((file, m.hexdigest()))


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'CDC Assembly Client', 
        html=html, 
        js_api=api,
        min_size=(720, 480)
    )
    webview.start()
