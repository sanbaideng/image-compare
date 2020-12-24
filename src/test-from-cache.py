from cv2 import cv2
import numpy as np
import os
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

g1 = os.walk(r"xjcy2")
g2 = os.walk(r'muyu')
file_list1 = []
file_list2 = []
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def calHashDic(file_list):
    dic = {i: -1 for i in range(len(file_list))}
    print('calHashDic 计算中...')
    for idx, file in enumerate(file_list):
        hash = getAverageHashOfImage(file)
        if(idx % 1000 == 0):
            print(idx)
        dic[idx] = hash
    print(len(dic))
    return dic


if __name__ == '__main__':
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
