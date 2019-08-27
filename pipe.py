import enum
import time
from multiprocessing.pool import ThreadPool
from utils import log


class Pipe(enum.Enum):
    Assembly = 0


class Assembly(object):

    def __init__(self, taskid, args):
        self.args = args
        self.id = taskid

    def run(self, status):
        # 每个任务都需要自行设置运行的状态
        log("aseembly", self.id, "start running")
        status.setState("clean data")
        time.sleep(10)
        status.setState("merge data")
        time.sleep(10)
        status.setState("assembly data")
        time.sleep(10)
        # 运行结束后设置状态为结束
        status.setDone()
        log("aseembly", self.id, "end running")


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
    main()
