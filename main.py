import os
import webview
import json
from utils import *
from multiprocessing import Manager


from check import enter, Global
from pipe import PipeManager, Pipe


class Api:
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
                if f.endswith('.gz'):
                    filePath = os.path.join(result[0], f)
                    fileList.append((f, filePath))
                    total += 1
            Global.setTotal(total)
            # 提交任务
            # fixed 改成进程池
            files = [(filePath, self.itemList) for f, filePath in fileList]
            enter(files)
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
        statusList = self.pipeStatus("")
        # todo 此处有问题
        for index, cell in enumerate(self.itemList):
            item = {
                "id": index+1,
                "sample": "sample{}".format(index//2),
                "name": os.path.basename(cell[0]),
                "hash": cell[1],
                "status": statusList[index]
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


    def pipeStart(self, params):
        """
        发送启动pipe的命令
        :return:
        :rtype:
        """
        # 异步开启流程任务
        # 返回消息
        fastq_list = [(1, 2), (1, 2), (1, 2), (1, 2)]
        self.pipeManager.update(fastq_list)
        r = self.pipeManager.start()
        return


    def pipeStatus(self, params):
        """
        使用js定时器发送流程运行信息
        :return:
        :rtype:
        """
        print("pipeStatus", self.pipeManager.allState())
        return self.pipeManager.allState()



if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'CDC Assembly Client', 
        html=load("templates/index.html"), 
        js_api=api,
        min_size=(720, 540)
    )
    webview.start()
