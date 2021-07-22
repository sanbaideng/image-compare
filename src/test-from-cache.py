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
import pandas as pd
import heapq
import json

g1 = os.walk(r"xjcy2")
g2 = os.walk(r'muyu')
file_list1 = []
file_list2 = []
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def calHashDic(file_list):
    # dic = {i: -1 for i in range(len(file_list))}
    # dic = {"a":"b"}
    dic={}
    print('calHashDic 计算中... 长度为：',len(file_list))
    for idx, file in enumerate(file_list):
        hash = getAverageHashOfImage(file)
        
        basename = os.path.basename(file)
        basenamenum = basename.split('.')[0]
        # print(basenamenum)
        if(idx % 1000 == 0):
            print(idx)
        dic[int(basenamenum)] = hash
    print(len(dic))
    return dic

def calDhashDic(file_list):
    dic={}
    print('calHashDic 计算中... 长度为：',len(file_list))
    for idx, file in enumerate(file_list):
        hash = getDhashOfImage(file)
        
        basename = os.path.basename(file)
        basenamenum = basename.split('.')[0]
        # print(basenamenum)
        if(idx % 1000 == 0):
            print(idx)
        dic[int(basenamenum)] = hash
    print(len(dic))
    return dic


def dirToRedis(dirSmall,dirBig,redis_hash_name_small,redis_hash_name_big,method="avg"):
    g1 = os.walk(dirBig)
    g2 = os.walk(dirSmall)
    file_list_big = []
    file_list_small = []
    for path, dir_list, file_list in g1:
        for file_name in file_list:
            #print(os.path.join(path, file_name))
            file_list_big.append(os.path.join(path, file_name))

    for path, dir_list, file_list in g2:
        for file_name in file_list:
            #print(os.path.join(path, file_name))
            file_list_small.append(os.path.join(path, file_name))

    file_list_big.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    file_list_small.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    file_big_len = len(file_list_big)
    file_small_len = len(file_list_small)
    # current = -1
    # print(file_list1)
    # print(file_list2)
    dic = {i: -1 for i in range(file_small_len)}
    # dic[file2_len] = file1_len

    # dic_small = calHashDic(file_list_small)
    # dic_big = calHashDic(file_list_big)
    if method == 'avg':
        dic_small = calHashDic(file_list_small)
        dic_big = calHashDic(file_list_big)
    else:
        dic_small = calDhashDic(file_list_small)
        dic_big = calDhashDic(file_list_big)
    p_dict_small = pickle.dumps(dic_small).decode('latin1')
    p_dict_big = pickle.dumps(dic_big).decode('latin1')

    r.set(redis_hash_name_big, p_dict_big)
    r.set(redis_hash_name_small, p_dict_small)

    print("hash-dic1-redis-value:")
    read_big_dict = r.get(redis_hash_name_big)
    bigdict = pickle.loads(read_big_dict.encode('latin1'))
    print(1)
    # dic22 = r.hgetall("hash-dic2")

def loadRedisAndCompare(redis_hash_name_big,redis_hash_name_small):
    current = -1
    positiveDict = {}
    negativeDict = {}
    dic_big = pickle.loads(r.get(redis_hash_name_big).encode('latin1'))
    dic_small = pickle.loads(r.get(redis_hash_name_small).encode('latin1'))
    # file1_len = len(dic_big)
    # file2_len = len(dic_small)
    file1_len = list(dic_big)[-1]
    file2_len = list(dic_small)[-1]

    # print(dic1)

    minRatePic = {'image': '', 'rate': 10000}
    # 循环比对
    for idx, hash2 in dic_small.items():
        # index = current+1\
        # print('muyu:',idx)
        for index ,hash1 in dic_big.items():
            # print('xjcy',index)
            # if int(index) < current:
            #     continue
            if(index == file1_len):
                
                # 比较 取值
                compareNew2(hash2, hash1, idx, index, minRatePic)
                print("-找到相近的图片-：", idx,
                      int(minRatePic["image"]))
                writeLine('result.csv', "-找到相近的图片-："+str(idx) + "  " +
                          str(int(minRatePic["image"])))
                negativeDict[idx] = int(minRatePic["image"])
                # 复位
                minRatePic = {'image': '', 'rate': 10000}
            if(compareNew2(hash2, hash1, idx, index, minRatePic)):
                if(idx > 50 and idx/file2_len*2 < index/file1_len):
                    print("=找到相近的图片-：", idx, index)
                    writeLine('result.csv', "=找到相近的图片=：" +
                              str(idx) + "  " + str(index))
                    negativeDict[idx] = index
                else:
                    print("+找到相近的图片+：", idx, index)
                    writeLine('result.csv', "+找到相近的图片+：" +
                              str(idx) + "  " + str(index))
                    positiveDict[idx] = index
                    # current = int(index)
                break        
    r.set("positiveDict", pickle.dumps(positiveDict).decode('latin1'))
    r.set("negativeDict", pickle.dumps(negativeDict).decode('latin1'))
    print("完成")
def loadRedisAndCompare_dhash(redis_hash_name_big,redis_hash_name_small):
    positiveDict = {}
    negativeDict = {}
    dic_big = pickle.loads(r.get(redis_hash_name_big).encode('latin1'))
    dic_small = pickle.loads(r.get(redis_hash_name_small).encode('latin1'))
    
    dic_big_avg = pickle.loads(r.get('xjcy2_hash').encode('latin1'))
    dic_small_avg = pickle.loads(r.get('muyu_hash').encode('latin1'))

    file1_len = list(dic_big)[-1]
    file2_len = list(dic_small)[-1]
    # minRatePic = {'image': '', 'rate': 10000}

    for idx, hash2 in dic_small.items():
        # index = current+1\
        # print('muyu:',idx)
        minRatePic = {'image': '', 'rate': 10000}
        top10MinRatePic = {}
        top10MinRatePic_avg = {}
        for index ,hash1 in dic_big.items():
            
            result1 = ((hash1 - hash2) / len(hash1.hash) ** 2)
            if result1<0.3:
                top10MinRatePic[index] = result1
            if  index < (idx/file2_len)*file1_len - 1000:
                continue
            # if result1 <0.2:
            if result1 < minRatePic['rate']:
                minRatePic['rate'] = result1
                minRatePic['image'] = index
            if index >(idx/file2_len)*file1_len+1000:                
                break
                    # print(index,result1)
        # print(idx,minRatePic['image'],minRatePic['rate'])
        top10Pic =  heapq.nsmallest(10, top10MinRatePic.items())
        r.hset(redis_hash_name_small+"_top10", idx, json.dumps(top10Pic))
        # 打算在0.2以上的，再用avg算法算一次，发现没用
        # if minRatePic['rate'] >0.2:
        #     avg_small_hash = dic_small_avg[idx]
        #     for index_avg ,hash_big_avg in dic_big_avg.items():
        #         compareNew3(avg_small_hash, hash_big_avg, idx, index_avg, top10MinRatePic_avg)

        #     top10Pic_avg =  heapq.nsmallest(10, top10MinRatePic_avg.items())
        #     r.hset(redis_hash_name_small+"_top10_avg", idx, json.dumps(top10Pic_avg))


        # d = r.hget('wait_task', idx)
        # djson = json.loads(d)
        # print(djson)
        # for ds in djson:
        #     print(ds[0],ds[1])
        # writeLine("resultnew.csv", str(idx) + " " + str(minRatePic['image'])+" " + str(minRatePic['rate']))
        writeLine("resultnew.csv", str(idx) + " " + str(minRatePic['image']))
            # print('xjcy',index)
            # if int(index) < current:
            #     continue
            
    # r.set("positiveDict", pickle.dumps(positiveDict).decode('latin1'))
    # r.set("negativeDict", pickle.dumps(negativeDict).decode('latin1'))
    print("完成")

def comparetwoimage4Test(img1,img2):
    hash1 = getAverageHashOfImage(img1)
    hash2 = getAverageHashOfImage(img2)
    minRatePic = {'image': '', 'rate': 10000}
    a = compareNew2(hash2, hash1, 1, 2, minRatePic)
    print(a,minRatePic)

def compareTowImage4TestBydhash(img1,img2):
    image1 = PIL.Image.open(img1)
    image2 = PIL.Image.open(img2)

    d1 = imagehash.dhash(image1)
    d2 = imagehash.dhash(image2)
    result1 = ((d1 - d2) / len(d1.hash) ** 2)
    print(result1)
    return result1
'''
dhash得到的结果处理，把低于2以上的和2以下的分开 速度很
'''


'''
找到附近的几个，用来表明界限
'''
def findSurroungdings(key,num,dsure):
    firstkey =list(dsure)[0]
    lastkey = list(dsure)[-1]
    resdict = {}
    indx  = 1
    cnt = 0
    findkey = key
    direction = -1 # -1 左，1右
    while cnt<num:
        #前面两个特殊情况，到边界了
        if findkey <= firstkey:
            findkey = findkey + indx
        elif findkey >= lastkey:
            findkey = findkey - indx
        #这里是左右摇摆
        else:
            direction = -(direction)
            findkey = findkey + indx*direction
        
        if findkey in dsure:
            resdict[findkey] = dsure[findkey]
            cnt = cnt + 1#
            
        indx = indx + 1
    return resdict
            


if __name__ == '__main__':
    # dirToRedis('muyu','xjcy2','muyu_hash','xjcy2_hash','avg')
    # dirToRedis('muyu','xjcy2','muyu_hash_dhash','xjcy2_hash_dhash','dhash')
    # loadRedisAndCompare('xjcy2_hash','muyu_hash')
    loadRedisAndCompare_dhash('xjcy2_hash_dhash','muyu_hash_dhash')
    # # 单个图片比较测试
    # comparetwoimage4Test('muyu/43.jpg','xjcy2/316.jpg')
    # compareTowImage4TestBydhash('muyu/43.jpg','xjcy2/316.jpg') # muyu/17.jpg xjcy2/155.jpg 0.25125

    
if __name__ == '__main__1':
    # for path, dir_list, file_list in g1:
    #     for file_name in file_list:
    #         #print(os.path.join(path, file_name))
    #         file_list1.append(os.path.join(path, file_name))

    # for path, dir_list, file_list in g2:
    #     for file_name in file_list:
    #         #print(os.path.join(path, file_name))
    #         file_list2.append(os.path.join(path, file_name))

    # file_list1.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    # file_list2.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    # file1_len = len(file_list1)
    # file2_len = len(file_list2)
    current = -1
    # # print(file_list1)
    # # print(file_list2)
    # dic = {i: -1 for i in range(file2_len)}
    # dic[file2_len] = file1_len

    # dic2 = calHashDic(file_list2)
    # dic1 = calHashDic(file_list1)

    # r.hmset("hash-dic1", dic1)
    # r.hmset("hash-dic2", dic2)
    # print("hash-dic1-redis-value:")
    # print(r.hgetall("hash-dic2"))
    # dic22 = r.hgetall("hash-dic2")
    positiveDict = {}
    negativeDict = {}
    dic1 = pickle.loads(r.get("hash_dict1").encode('latin1'))
    dic2 = pickle.loads(r.get("hash_dict2").encode('latin1'))
    file1_len = len(dic1)
    file2_len = len(dic2)
    # print(dic1)

    minRatePic = {'image': '', 'rate': 10000}
    # 循环比对
    for idx, hash2 in dic2.items():
        index = current+1
        while index < file1_len:
            #print("index:", index)
            if(index == file1_len-1):
                # 比较 取值
                compareNew2(hash2, dic1[index], idx, index, minRatePic)
                print("-找到相近的图片-：", idx+7,
                      int(minRatePic["image"])+78)
                writeLine('result.csv', "-找到相近的图片-："+str(idx+7) + "  " +
                          str(int(minRatePic["image"])+78))
                negativeDict[idx+7] = int(minRatePic["image"])+78
                # 复位
                minRatePic = {'image': '', 'rate': 10000}
            if(compareNew2(hash2, dic1[index], idx, index, minRatePic)):
                if(idx > 50 and idx/file2_len*2 < index/file1_len):
                    print("=找到相近的图片-：", idx+7, index+78)
                    writeLine('result.csv', "=找到相近的图片-：" +
                              str(idx+7) + "  " + str(index+78))
                    negativeDict[idx+7] = index+78
                else:
                    print("+找到相近的图片+：", idx+7, index+78)
                    writeLine('result.csv', "+找到相近的图片+：" +
                              str(idx+7) + "  " + str(index+78))
                    positiveDict[idx+7] = index+78
                    current = index
                break

            index += 1
    r.set("positiveDict", pickle.dumps(positiveDict).decode('latin1'))
    r.set("negativeDict", pickle.dumps(negativeDict).decode('latin1'))
    print("完成")

