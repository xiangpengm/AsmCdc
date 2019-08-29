import os
import webview
import json
from utils import *
from multiprocessing import Manager

from check import enter, Global
from pipe import PipeManager, Pipe


class Api:
    # 进程中的共享数据
    m = Manager()
    pipeManager = PipeManager(Pipe.Assembly)

    def __init__(self):
        self.itemList = self.m.list()

    def getCount(self, params):
        """
        webview获取 hash数据计算进度
        :param params:
        :type params:
        :return:
        :rtype:
        """
        if Global.total() == 0:
            return "noTask"
        elif Global.count() == Global.total():
            Global.reset()
            return 1
        else:
            return Global.status()

    def getFilePath(self, params):
        """
        获取目录文件 并使用多进程接口提交后台任务计算文本的hash值
        :param params:
        :type params:
        :return:
        :rtype:
        """
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
            # 扫描目录
            for f in os.listdir(result[0]):
                if f.endswith('fq.gz') or f.endswith('fastq.gz') or f.endswith('fq') or f.endswith('fastq'):
                    filePath = os.path.join(result[0], f)
                    fileList.append((f, filePath))
                    total += 1
            Global.setTotal(total)
            self.fileList = fileList[::]
            # 提交任务
            # fixed 改成进程池
            # 计算md5值
            files = [(filePath, self.itemList) for f, filePath in fileList]
            enter(files)
            # 返回结果
            return {
                "path": result[0], 
                "total": total
            }

    def getOutputPath(self, params):
        """
        获取输出文件目录
        :param params:
        :type params:
        :return:
        :rtype:
        """
        result = window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=True,
        )
        if result is None:
            return "None"
        else:
            self.output = result[0]
            return result[0]

    def getFileData(self, param):
        """
        计算之后的hash值由此api返回
        :param param:
        :type param:
        :return:
        :rtype:
        """
        r = []
        # 这里返回给定的样本表格
        # todo 此处有问题
        itemList = self.getItemList()
        print("return before sort itemList", itemList)
        itemList = self.sortItem(itemList)
        print("return after  sort itemList", itemList)
        for index, cell in enumerate(itemList):
            item = {
                "sample": "sample{}".format(index//2),
                "name": os.path.basename(cell[0]),
                "hash": cell[1],
                "status": "waiting",
            }
            r.append(item)
        
        # 返回当前计算的hash数据
        # 把样本信息传递给PipeManager
        return json.dumps(r, ensure_ascii=False)

    def itemListReset(self):
        """
        重置 itemList, item list是一个Manager().list实例
        :return:
        :rtype:
        """
        self.itemList = self.m.list()

    def getItemList(self):
        itemList = sorted(self.itemList, key=lambda item: item[0])
        return itemList

    def pipeStart(self, params):
        """
        发送启动pipe的命令
        :return:
        :rtype:
        """
        # 异步开启流程任务
        # 返回消息
        args = self.parseArgs([filePath for _, filePath in self.fileList], self.output)
        self.pipeManager.update(args)
        print("main pipeManager start")
        self.pipeManager.start()

    def pipeStatus(self, params):
        """
        使用js定时器发送流程运行信息
        :return:
        :rtype:
        """
        status = self.pipeManager.allState()
        total = len(status)
        done  = status.count('done') 
        r = {
            "total": total,
            "done": done,
            "status": status
        }
        return r

    def parseArgs(self, fastqFileList, *other):
        args = []
        while fastqFileList:
            this = fastqFileList.pop()
            for file in fastqFileList:
                if is_paired(this, file):
                    arg = [this, file]
                    arg.sort()
                    arg.extend(other)
                    args.append(tuple(arg))
        return args

    def sortItem(self, items):
        dt = {}
        r = []
        for item in items:
            dt[os.path.basename(item[0])] = item
        fqList = list(dt.keys())
        args = self.parseArgs(fqList)
        for arg in args:
            r.append(dt.get(arg[0]))
            r.append(dt.get(arg[1]))
        return r



if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'CDC Assembly Client', 
        html=load("templates/index.html"), 
        js_api=api,
        min_size=(800, 600)
    )
    webview.start()
