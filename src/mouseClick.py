from resultHandle import writeLine
import cv2
from matplotlib import artist
import numpy as np
import matplotlib.pyplot as plt
import redis
import itertools
from collections import OrderedDict
import pickle
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 全局变量
flagnow = OrderedDict()
flagresult = OrderedDict()


def onclick(event):
    global flagresult
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    rown, columnn = getPicByPosition(event.x, event.y, 10, 20)
    indexofdic = 10 * (rown-1) + int(columnn/2)
    #print("移除", indexofdic)

    els = list(flagnow.items())
    key = els[indexofdic]
    print("key:")
    print(key)
    # print(els[indexofdic])
    # print(flagnow.pop(11))
    # print(flagnow[els[indexofdic][0]])
    # print("移除lagnow.pop(els[indexofdic]):")
    # print(flagnow.pop(indexofdic))
    print("移除lagnow.pop(els[indexofdic]):")
    print(flagnow.pop(str(key[0])))
    flagresult = {**flagresult, **flagnow}


def matplotlib_multi_pic2(dis):
    lensofdis = len(dis)
    row = int(lensofdis / 10)
    column = int(lensofdis / 10) * 2
    if lensofdis % 10 != 0:
        row = int(lensofdis / 10) + 1
        column = int(lensofdis / 10) * 2

    idx = 0

    fig, ax = plt.subplots(figsize=(40, 80))
    fig.canvas.mpl_connect('button_press_event', onclick)

    #fig.canvas.mpl_connect('figure_enter_event', figure_enter_event)

    for key, val in dis.items():
        path1 = "muyu//" + key + ".jpg"
        path2 = "xjcy2//" + val + ".jpg"
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
        idx = idx + 1
        #print("idx1", idx)
        plt.subplot(row, column, idx)
        plt.imshow(img1)
        plt.title(key, fontsize=8)
        plt.xticks([])
        plt.yticks([])

        idx = idx + 1
        #print("idx2", idx)
        plt.subplot(row, column, idx)
        plt.imshow(img2)
        plt.title(val, fontsize=8)
        plt.xticks([])
        plt.yticks([])

    plt.grid(True)
    plt.show()


def getPicByPosition(x, y, rowcnt, columncnt, xdistance=130, ydistance=110):
    xbase = 450
    ybase = 150
    xd = x - xbase
    yd = y - ybase
    columnc = int(xd / xdistance)+1
    rowc = int(yd / ydistance)+1
    print("rowc:", 11-rowc, "columnc:", columnc)
    return 11-rowc, columnc


def getLineFormCsvToDict(filepath):
    f = open(filepath)
    f_read = f.read()
    no = 0
    dicpare = OrderedDict()
    for line in f_read.split('\n'):
        key = line.split(" ")[0]
        val = line.split(" ")[1]
        dicpare[key] = val
    return dicpare


def pickFakeResult():
    dic = getLineFormCsvToDict("resultnew.csv")

    lenofDic = len(dic)
    times = int(lenofDic / 100)+1

    t = 1
    while t <= times:
        begin = (t-1)*100
        end = begin + 100
        global flagnow
        flagnow = dict(itertools.islice(dic.items(), begin, end))
        lenofflagnow = len(flagnow)
        if(lenofflagnow < 100):
            ltemp = dict(itertools.islice(dic.items(), 0, 100-lenofflagnow))
            flagnow = {**flagnow, **ltemp}

        print("flagnow init:")
        print(flagnow)
        matplotlib_multi_pic2(flagnow)
        t = t+1


# readAndCompare("resultnew.csv")
def getCsVFromResultDic(dic):

    r.set("rescsv.csv", pickle.dumps(dic).decode('latin1'))
    for key, val in dic.items():
        writeLine("rescsv.csv", str(key) + " " + str(val))


pickFakeResult()
print(flagresult)
getCsVFromResultDic(flagresult)
