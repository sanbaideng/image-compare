from cv2 import cv2
import numpy as np
import os
import PIL
from PIL import Image
import math
import operator
from functools import reduce
import time
from aphash import PHash
from comAlth.ImageHash import *
from comAlth import aHash
from comAlth.aHash import classfiy_aHash
from comAlth.histogram2 import *
from resultHandle import *
import redis
import pickle

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
def findNextPositive(idx,positiveDict):    
    lastindex = int(list(positiveDict)[-1])
    while idx < lastindex:
        idx = idx + 1
        if(idx in positiveDict):
            return positiveDict[idx]
    return positiveDict[lastindex]

def findPrePositive(idx,positiveDict):
    firstindex = int(list(positiveDict)[0])
    while idx >= firstindex:
        idx = idx - 1
        if(idx in positiveDict):
            return positiveDict[idx]
    return positiveDict[firstindex]

def dhashcmp():
    positiveDict = pickle.loads(r.get("positiveDict").encode('latin1'))
    negativeDict = pickle.loads(r.get("negativeDict").encode('latin1'))
    positiveLen = len(positiveDict)
    negativeLen = len(negativeDict)
    totalLen = negativeLen + positiveLen

    lastKeyOfNega = list(negativeDict)[-1]
    lastKeyOfPosi = list(positiveDict)[-1]
    firstKeyOfNega = list(negativeDict)[0]
    firstKeyOfPosi = list(positiveDict)[0]
    maxKeyIndex = 0
    minKeyIndex = -1
    if(lastKeyOfNega > lastKeyOfPosi):
        maxKeyIndex = negativeDict[lastKeyOfNega]
    else:
        maxKeyIndex = positiveDict[lastKeyOfPosi]

    if(firstKeyOfNega < firstKeyOfPosi):
        minKeyIndex = negativeDict[firstKeyOfNega]
    else:
        minKeyIndex = positiveDict[firstKeyOfPosi]
    maxKeyIndex = int(maxKeyIndex)
    minKeyIndex = int(minKeyIndex)
    lastKeyOfNega = int(lastKeyOfNega)
    lastKeyOfPosi = int(lastKeyOfPosi)
    firstKeyOfNega = int(firstKeyOfNega)
    firstKeyOfPosi = int(firstKeyOfPosi)
    minIndex = firstKeyOfNega if firstKeyOfPosi > firstKeyOfNega else firstKeyOfPosi
    maxIndex = lastKeyOfNega if lastKeyOfNega > lastKeyOfPosi else lastKeyOfPosi

    # print(dic1)
    # 循环比对
    # 找到negative的边界,遍历positive的大小
    dicnew = {}
    for idx, val in negativeDict.items():
        idx = int(idx)
        
        imageidx = Image.open("muyu//"+str(idx)+".jpg")
        d0 = imagehash.dhash(imageidx)

        print("查找", idx, "的边界")
        # upperBoundary = maxKeyIndex
        # lowerBoundary = minKeyIndex

        # 找下边界
        lowerBoundary = findPrePositive(idx,positiveDict)
        upperBoundary = findNextPositive(idx,positiveDict)
        if lowerBoundary > upperBoundary:
            temp = upperBoundary
            lowerBoundary = upperBoundary
            upperBoundary = temp
        # 计算
        # x = lowerBoundary
        # 暂存结果
        minRatePic = {'image': '', 'rate': 10000}
        print("lowerBoundary:")
        print(lowerBoundary)
        print("upperBoundary:")
        print(upperBoundary)
        xint = lowerBoundary
          


        while xint <= upperBoundary:

            # 算法,比较,拿出两张图 得到所有值,拿出最小的

            imagex = PIL.Image.open("xjcy2//"+str(xint)+".jpg")
            d1 = imagehash.dhash(imagex)
            result1 = ((d1 - d0) / len(d1.hash) ** 2)
            if result1 < minRatePic["rate"]:
                minRatePic["image"] = xint
                minRatePic["rate"] = result1
                print("result1: ", result1, "index:", minRatePic["image"])
            if(xint == upperBoundary):
                # 循环的结果
                dicnew[idx] = minRatePic["image"]

            xint = xint + 1
            # 找大边界
    r.set("negativeDict_new", pickle.dumps(dicnew).decode('latin1'))

    print("redo完成")
    print("dicnew:")

    print(dicnew)
    comIndex = minIndex
    while comIndex <= maxIndex:
        if(comIndex in dicnew):
            print("+++", comIndex, dicnew[comIndex])
            writeLine("resultnew.csv", str(comIndex) +
                      " " + str(dicnew[comIndex]))
        if(comIndex in positiveDict):
            print("---", comIndex, positiveDict[comIndex])
            writeLine("resultnew.csv", str(comIndex) +
                      " " + str(positiveDict[comIndex]))
        comIndex = comIndex + 1

if __name__ == '__main__':
    dhashcmp()

if __name__ == '__main__1':
    positiveDict = pickle.loads(r.get("positiveDict").encode('latin1'))
    negativeDict = pickle.loads(r.get("negativeDict").encode('latin1'))
    positiveLen = len(positiveDict)
    negativeLen = len(negativeDict)
    totalLen = negativeLen + positiveLen

    lastKeyOfNega = list(negativeDict)[-1]
    lastKeyOfPosi = list(positiveDict)[-1]
    firstKeyOfNega = list(negativeDict)[0]
    firstKeyOfPosi = list(positiveDict)[0]
    maxKeyIndex = 0
    minKeyIndex = -1
    if(lastKeyOfNega > lastKeyOfPosi):
        maxKeyIndex = negativeDict[lastKeyOfNega]
    else:
        maxKeyIndex = positiveDict[lastKeyOfPosi]

    if(firstKeyOfNega < firstKeyOfPosi):
        minKeyIndex = negativeDict[firstKeyOfNega]
    else:
        minKeyIndex = positiveDict[firstKeyOfPosi]
    maxKeyIndex = int(maxKeyIndex)
    minKeyIndex = int(minKeyIndex)
    lastKeyOfNega = int(lastKeyOfNega)
    lastKeyOfPosi = int(lastKeyOfPosi)
    firstKeyOfNega = int(firstKeyOfNega)
    firstKeyOfPosi = int(firstKeyOfPosi)
    minIndex = firstKeyOfNega if firstKeyOfPosi > firstKeyOfNega else firstKeyOfPosi
    maxIndex = lastKeyOfNega if lastKeyOfNega > lastKeyOfPosi else lastKeyOfPosi

    # print(dic1)
    # 循环比对
    # 找到negative的边界,遍历positive的大小
    dicnew = {}
    for idx, val in negativeDict.items():
        idx = int(idx)
        imageidx = Image.open("muyu//"+str(idx)+".jpg")
        d0 = imagehash.dhash(imageidx)

        print("查找", idx, "的边界")
        upperBoundary = maxKeyIndex
        lowerBoundary = minKeyIndex

        # 找下边界
        i = idx - 1
        while i >= 0:
            # 倒着查 如果有key 则是下边界
            if(i == 0):
                print("下边界1:0")
                lowerBoundary = minKeyIndex
                break
            if(i in positiveDict):
                print("下边界2:", i)
                lowerBoundary = positiveDict[i]
                break
            i = i - 1

        # 找上边界
        j = idx + 1
        while j < lastKeyOfPosi:
            if(j == lastKeyOfPosi):
                print("上边界1:", maxKeyIndex)
                upperBoundary = maxKeyIndex
                break
            if(j in positiveDict):
                print("上边界2", j)
                upperBoundary = positiveDict[j]
                break
            j = j + 1

        # 计算
        x = lowerBoundary
        # 暂存结果
        minRatePic = {'image': '', 'rate': 10000}
        print("lowerBoundary:")
        print(lowerBoundary)
        print("upperBoundary:")
        print(upperBoundary)
        while x <= upperBoundary:

            # 算法,比较,拿出两张图 得到所有值,拿出最小的

            imagex = PIL.Image.open("xjcy2//"+str(x)+".jpg")
            d1 = imagehash.dhash(imagex)
            result1 = ((d1 - d0) / len(d1.hash) ** 2)
            if result1 < minRatePic["rate"]:
                minRatePic["image"] = x
                minRatePic["rate"] = result1
                print("result1: ", result1, "index:", minRatePic["image"])
            if(x == upperBoundary):
                # 循环的结果
                dicnew[idx] = minRatePic["image"]

            x = x + 1
            # 找大边界
    r.set("negativeDict_new", pickle.dumps(dicnew).decode('latin1'))

    print("redo完成")
    print("dicnew:")

    print(dicnew)
    comIndex = minIndex
    while comIndex <= maxIndex:
        if(comIndex in dicnew):
            print("+++", comIndex, dicnew[comIndex])
            writeLine("resultnew.csv", str(comIndex) +
                      " " + str(dicnew[comIndex]))
        if(comIndex in positiveDict):
            print("---", comIndex, positiveDict[comIndex])
            writeLine("resultnew.csv", str(comIndex) +
                      " " + str(positiveDict[comIndex]))
        comIndex = comIndex + 1
