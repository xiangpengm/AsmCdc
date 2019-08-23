from hashlib import md5
from multiprocessing import current_process
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
from multiprocessing import Value
import time


# 全局变量
class Global(object):
    lock = Lock()
    _count = Value('i', 0)
    _total = Value('i', 0)

    @classmethod
    def acquire(cls):
        cls.lock.acquire()

    @classmethod
    def release(cls):
        cls.lock.release()

    @classmethod
    def countAdd(cls, value=1):
        cls.acquire()
        cls._count.value += value
        cls.release()
    
    @classmethod
    def reset(cls):
        cls.acquire()
        cls._count.value = 0
        cls._total.value = 0
        cls.release()

    @classmethod
    def count(cls):
        return cls._count.value

    @classmethod
    def setTotal(cls, value):
        cls._total.value = value
    
    @classmethod
    def total(cls):
        return cls._total.value

    @classmethod
    def status(cls):
        if cls.total != 0:
            r = cls.count() / cls.total()
            return r
        else:
            return None


def getFileMD5(file, itemList):
    m = md5()
    f = open(file, 'rb')
    buffer = 8192
    while 1:
        chunk = f.read(buffer)
        if not chunk:
            break
        m.update(chunk)
    f.close()
    Global.countAdd()
    itemList.append((file, m.hexdigest()))


p = Pool((cpu_count()-1)*2)


def enter(files):
    for file in files:
        p.apply_async(getFileMD5, file)