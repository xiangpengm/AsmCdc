import os
import sys
import time
import webview
from hashlib import md5
import json

from check import enter, Global
from multiprocessing import Manager


def load(file, tp='r'):
    with open(file, tp) as f:
        return f.read()


class Api:
    m = Manager()

    def __init__(self):
        self.itemList = self.m.list()

    def getCount(self, params):
        if Global.total() == 0:
            return "noTask"
        elif Global.count() == Global.total():
            Global.reset()
            return 1
        else:
            return Global.status()

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
            self.itemListReset()
            fileList = []
            total = 0
            for f in os.listdir(result[0]):
                if f.endswith('.gz'):
                    filePath = os.path.join(result[0], f)
                    fileList.append((f, filePath))
                    total += 1
            Global.setTotal(total)
            # todo 改成进程池
            files = [(filePath, self.itemList) for f, filePath in fileList]
            enter(files)
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
        r = []
        for index, cell in enumerate(self.itemList):
            item = {
                "id": index+1,
                "name": os.path.basename(cell[0]),
                "hash": cell[1],
            }
            r.append(item)
        return json.dumps(r, ensure_ascii=False)

    def itemListReset(self):
        self.itemList = self.m.list()

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'CDC Assembly Client', 
        html=load("templates/index.html"), 
        js_api=api,
        min_size=(720, 540)
    )
    webview.start()
