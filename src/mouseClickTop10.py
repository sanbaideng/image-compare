from resultHandle import writeLine
import cv2
from matplotlib import artist
import numpy as np
import matplotlib.pyplot as plt
import redis
import itertools
from collections import OrderedDict
import pickle
import csv,json
from test_redo_intwolist import findNextPositive,findPrePositive

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

'''
从top10中选择最匹配的一张图
'''
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

    # plt.figure(figsize=(1920,1080)) 
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
        #plt.subplots_adjust(0.1,0.1,0.2,0.2,10,10)
        plt.subplots_adjust(wspace =0, hspace =0)#调整子图间距
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
    plt.tight_layout()#调整整体空白
    
    size = fig.get_size_inches()*fig.dpi # size in pixels
    width = round(size[0])
    heigh = round(size[1])
    print(width,heigh)

    plt.show()


def getPicByPosition(x, y, rowcnt, columncnt, xdistance=95, ydistance=95):
    xbase = 450
    ybase = 150
    xbase = 55
    ybase = 80
    xd = x - xbase
    yd = y - ybase
    columnc = int(xd / xdistance)+1
    rowc = int(yd / ydistance)+1
    print("rowc:", 11-rowc, "columnc:", columnc)
    return 11-rowc, columnc

 

def dhashResultHandle():
    dic_big = pickle.loads(r.get('xjcy2_hash_dhash').encode('latin1'))
    dic_small = pickle.loads(r.get('muyu_hash_dhash').encode('latin1'))

    csv_reader = csv.reader(open("resultnew.csv"))

    dsure= {}
    dnotsure = {}

    for line in csv_reader:
        # print(line[0].split(' ')[0],line[0].split(' ')[1],line[0].split(' ')[2])
        if float(line[0].split(' ')[2]) > 0.2:
            dnotsure[int(line[0].split(' ')[0])] = int(line[0].split(' ')[1])
        else:
            dsure[int(line[0].split(' ')[0])]= int(line[0].split(' ')[1])
    for notsure in dnotsure:
        pre = findPrePositive(notsure,dsure)
        last = findNextPositive(notsure,dsure)
        if pre > last :
            tmp = last
            last = pre
            pre = tmp
             
        # print(notsure,dnotsure[notsure])
        # r.hset(redis_hash_name_small+"_top10", idx, json.dumps(top10Pic))
        d = r.hget('muyu_hash_top10',notsure)
        djson = json.loads(d)
        # print(djson)
        
        fig, ax = plt.subplots(figsize=(40, 80))
        path1 = "muyu//" + str(notsure) + ".jpg"
        
        img1 = cv2.imread(path1)
        plt.subplots_adjust(wspace =0, hspace =0)#调整子图间距
        plt.subplot(1, 21, 1)
        plt.imshow(img1)
        plt.title(str(notsure), fontsize=8)
        plt.xticks([])
        plt.yticks([])
        idx = 2
        for index in range(pre,last):
            if idx > 21:
                break
            path1 = "xjcy2//" + str(index) + ".jpg"
            
            img1 = cv2.imread(path1)
            #print("idx1", idx)
            #plt.subplots_adjust(0.1,0.1,0.2,0.2,10,10)
            plt.subplots_adjust(wspace =0, hspace =0)#调整子图间距
            plt.subplot(1, 21, idx)
            plt.imshow(img1)
            plt.title(str(index), fontsize=8)
            plt.xticks([])
            plt.yticks([])
            idx = idx + 1
        plt.tight_layout()#调整整体空白
        
        plt.show()

            
        

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


if __name__ == '__main__':
    # pickFakeResult()
    dhashResultHandle()
    # print(flagresult)
    # getCsVFromResultDic(flagresult)
