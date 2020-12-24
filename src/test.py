from cv2 import cv2
import numpy as np
import os
from PIL import Image
import math
import operator
from functools import reduce
import time
from aphash import PHash
from comAlth.ImageHash import compareIH
from comAlth import aHash
from comAlth.aHash import classfiy_aHash
from comAlth.histogram2 import *

g1 = os.walk(r"xjcy2")
g2 = os.walk(r'muyu')
file_list1 = []
file_list2 = []

if __name__ == '__main__':
    # time_start = time.time()
    # for i in range(100):
    #     compare(r'.\\muyu\\27.jpg',r'.\\top\\23.jpg')
    # time_end = time.time()
    # print('time cost', time_end - time_start, 's')
    #
    # time_start1 = time.time()
    # for i in range(100):
    #     compareIH(r'.\\muyu\\27.jpg', r'.\\top\\23.jpg',4)
    # time_end1= time.time()
    # print('time cost', time_end1 - time_start1, 's')
    #
    # print('done')
    for path, dir_list, file_list in g1:
        for file_name in file_list:
            #print(os.path.join(path, file_name))
            file_list1.append(os.path.join(path, file_name))

    for path, dir_list, file_list in g2:
        for file_name in file_list:
            #print(os.path.join(path, file_name))
            file_list2.append(os.path.join(path, file_name))

    file_list1.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    file_list2.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    file1_len = len(file_list1)
    file2_len = len(file_list2)
    current = 0
    print(file_list1)
    print(file_list2)
    dic = {i: -1 for i in range(file2_len)}
    dic[file2_len] = file1_len

    for idx, file2 in enumerate(file_list2):
        index = current+1
        while index < file1_len:
            file1 = file_list1[index-1]
            # 二分法
            if index > 600 and idx/file2_len*2 < index/file1_len:
                # print("idx/file2_len*4:", "index/file1_len:")
                # print(idx, file2_len, idx/file2_len*4, "file1:",
                #       index, file1_len, index/file1_len)
                #print(idx, index)
                break
            if(compareIH(file1, file2, 4)):
                print("找到相近的图片：", idx, file2, file1, index, current)
                dic[idx] = index
                current = index
                break
            index += 1
    print("结果如下", "dic")
    print(dic)


def findSimiPic(file_list1, file_list2, dict, index, low, high):
    file1_len = len(file_list1)
    file2_len = len(file_list2)
    file1_low = dict[low]
    file1_high = dict[high]

    file1_index = file1_low
    while file1_index < file1_high:
        file1 = file_list1[index-1]

        if idx/file2_len*2 < index/file1_len:
            break
        if(compareIH(file1, file2, 4)):
            print("找到相近的图片：", file2, file1, file1_index)
            dict[index] = file1_index
            return dict
        file1_index += 1
    dict[index] = -2
    return dict


def findSimilarPic(file_list1, file_list2, dict, index, low, high):
    file1_len = len(file_list1)
    file2_len = len(file_list2)
    file1_low = dict[low]
    file1_high = dict[high]
    mid = int(low + (high - low)/2)
    dict = findSimiPic(file_list1, file_list2, dict, index, low, high)
    plus = True
    count = 1
    if(dict[index] == -2):
        count += count
        if(plus):
            findSimiPic(file_list1, file_list2, dict, index+count, low, high)
        else:
            findSimiPic(file_list1, file_list2, dict, index - count, low, high)
        plus = not plus
