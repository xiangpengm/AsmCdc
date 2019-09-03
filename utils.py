import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    #time_format = '[%Y/%m/%d %H:%M:%S]'
    #localtime = time.localtime(int(time.time()))
    #formatted = time.strftime(time_format, localtime)
    #with open('log.gua.txt', 'a', encoding='utf-8') as f:
    #    print(formatted, *args, **kwargs)
    #    print(formatted, *args, file=f, **kwargs)
    pass

def is_paired(s1, s2, threshold=1):
    ls1 = len(s1)
    ls2 = len(s2)
    diff_count = 0
    diffSet = []
    if ls1 == ls2:
        for i in range(ls1):
            s1item = s1[i]
            s2item = s2[i]
            if s1item != s2item:
                diff_count += 1
                diffSet.append(s1item)
                diffSet.append(s2item)
                if diff_count > threshold:
                    return False
        if diffSet == ['1', '2'] or diffSet == ['2', '1']:
            return True
        else:
            return False
    else:
        return False


def load(file, tp='r'):
    with open(file, tp) as f:
        return f.read()
