import enum
import time
from datetime import datetime
from multiprocessing.pool import ThreadPool
from utils import log
import os
import tempfile
import subprocess
import shutil
from multiprocessing import cpu_count
import psutil


class Pipe(enum.Enum):
    Assembly = 0


class Assembly(object):

    def __init__(self, taskid, args):
        print("instanse ", taskid, args)
        self.args = args
        self.id = taskid
        self.workDir = self.tempDir()
        self.threads = cpu_count() // 2

    def run(self, status):
        # 每个任务都需要自行设置运行的状态
        log("aseembly", self.id, "start running")
        startTime = datetime.now()
        outputDir = self.args[2]
        # 初始化工作路径
        # 初始化参数
        #  clean参数
        logFile = self.workDir + "/{}_{}.log".format(self.__class__.__name__, self.id)
        fastq1 = os.path.join(self.workDir, os.path.basename(self.args[0]))
        fastq2 = os.path.join(self.workDir, os.path.basename(self.args[1]))
        fastq1unpaired = fastq1 + ".unpaired.fq.gz"
        fastq2unpaired = fastq2 + ".unpaired.fq.gz"
        # clean的输出asm的输入
        fastq1Clean = fastq1 + ".clean.fq.gz"
        fastq2Clean = fastq2 + ".clean.fq.gz"
        #  asm参数
        asmDir = os.path.join(self.workDir, 'asm')

        # 复制文件
        status.setState("copy file to work dir")
        shutil.copyfile(self.args[0], fastq1)
        shutil.copyfile(self.args[1], fastq2)

        # 过滤数据
        status.setState("clean fastq file")
        cleanCmd = f"""trimmomatic PE -threads {self.threads} \
            -trimlog {logFile} \
            {fastq1} {fastq2}\
            {fastq1Clean} \
            {fastq1unpaired} \
            {fastq2Clean} \
            {fastq2unpaired} \
            LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"""
        print("cleanCmd", cleanCmd)
        os.system(cleanCmd)

        # 组装
        status.setState("assembly file")
        asmCmd = f"""spades.py -o {asmDir} \
            --pe1-1 {fastq1Clean} \
            --pe1-2 {fastq2Clean} \
            --only-assembler --careful --cov-cutoff auto"""
        print("asmCmd", asmCmd)
        os.system(asmCmd)

        # todo 先压缩在copy, 之后在清除
        # 移动组装数据到输出目录
        status.setState("move fasta file to output dir")
        outputBasename = "assemble_{}.fa".format(self.id)
        spadesOutput = os.path.join(asmDir, "scaffolds.fasta")
        outputFasta = os.path.join(outputDir, outputBasename)
        shutil.copyfile(spadesOutput, outputFasta)

        # 压缩输出文件
        status.setState("gzip fasta file")
        os.system("cd \"{}\" && gzip {}".format(outputDir, outputBasename))

        # 清理工作目录 clean
        status.setState("clean temp file")
        shutil.rmtree(self.workDir)

        # 结束
        endTime = datetime.now()
        useTime = endTime - startTime
        useTimeStr = time.strftime("%H:%M:%S", time.gmtime(int(useTime.total_seconds())))
        status.setState("done<br>" + useTimeStr)
        log("assembly", self.id, "end")

    def tempDir(self):
        template = "/tmp/{}_{}".format(self.__class__.__name__, self.id)
        if not os.path.exists(template):
            print("create temp dir")
            os.makedirs(template)
        return template
    

class Status(object):

    def __init__(self, taskId):
        self.id = taskId
        self.currentState = "waiting"
        self.isDone = False
        self.StateList = []

    def setDone(self):
        self.isDone = True
        self.currentState = "done"

    def setState(self, value):
        self.currentState = value
        self.StateList.append(value)


class PipeManager(object):
    """
    需要实现的功能是流程管理
    update, 传递流程信息
    3.
    """
    mapper = {
        # 设置流程枚举映射
        Pipe.Assembly: Assembly
    }
    statusList = {}
    instanceList = []

    def __init__(self, pipe, maxThread=2):
        p = self.mapper.get(pipe)
        if p is None:
            raise ValueError(p)
        # 给予流程创建实例来用
        self.pipe = p
        self.pool = ThreadPool(maxThread)
        self.running = False
        self._ready = False

    def update(self, tasks):
        """
        把参数列表变成流程对象实例
        :param tasks:
        :type tasks:
        :return:
        :rtype:
        """
        self.instanceList = []
        for index, task in enumerate(tasks):
            instance = self.pipe(index, task)
            self.instanceList.append(instance)
            self.statusList[index] = Status(index)

    def start(self):
        if not self._ready and not self.running:
            log("Pipe Manager start running")
            for index in range(len(self.instanceList)):
                pipeInstance = self.instanceList[index]
                pipeStatusInstance = self.statusList[index]
                self.pool.apply_async(
                    pipeInstance.run,
                    (pipeStatusInstance, )
                )
            self.running = True
            log("Pipe Manager end running")
            return "started"
        elif self.running == True:
            log("task have running ")
            return "runnning"
        else:
            log("task have running ")
            return "already"

    def ready(self):
        count = 0
        for status in self.statusList.values():
            if status.isDone == False:
                count += 1
        ready = count == 0
        if ready == True:
            self.running = False
            self._ready = True
            return True
        else:
            return False

    def allState(self):
        r = []
        for status in self.statusList.values():
            r.append(status.currentState)
        return r


def main():
    fastq_list = [(1, 2), (1, 2), (1, 2), (1, 2)]
    pipeManager =  PipeManager(Pipe.Assembly)
    pipeManager.update(fastq_list)
    pipeManager.start()
    while True:
        if pipeManager.ready() == True:
            break
        else:
            time.sleep(0.5)
            log(pipeManager.allState())


if __name__ == "__main__":
    # main()
    a = Assembly(
        12, (
        "/Users/xiangpeng/Desktop/04. 我的仓库/AsmCdc/test/S-4_FDMS190640081-1a/S-4_FDMS190640081-1a_1.clean.fq.gz",
        "/Users/xiangpeng/Desktop/04. 我的仓库/AsmCdc/test/S-4_FDMS190640081-1a/S-4_FDMS190640081-1a_2.clean.fq.gz",
        "/tmp/output"
        )
    )
    print(a.tempDir())
    status =  Status(0)
    a.run(status)
