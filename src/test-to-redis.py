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
import json
import pickle
g1 = os.walk(r"xjcy2")
g2 = os.walk(r'muyu')
file_list1 = []
file_list2 = []
r = redis.Redis(host='localhost', port=6379,
                encoding='utf8', decode_responses=True)


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
    for path, dir_list, file_list in g1:
        for file_name in file_list:
            # print(os.path.join(path, file_name))
            file_list1.append(os.path.join(path, file_name))

    for path, dir_list, file_list in g2:
        for file_name in file_list:
            # print(os.path.join(path, file_name))
            file_list2.append(os.path.join(path, file_name))

    file_list1.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    file_list2.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    file1_len = len(file_list1)
    file2_len = len(file_list2)
    current = -1
    # print(file_list1)
    # print(file_list2)
    dic = {i: -1 for i in range(file2_len)}
    dic[file2_len] = file1_len

    dic1 = calHashDic(file_list1)
    dic2 = calHashDic(file_list2)

    # favorite_color = {"lion": "yellow", "kitty": "red"}  # create a dictionary
    # # save it into a file named save.p
    # pickle.dump(dic2, open("save.p", "wb"))
    # favorite_color = pickle.load(open("save.p", "rb"))
    # print(favorite_color)

    r.set("hash_dict1", pickle.dumps(dic1).decode('latin1'))
    r.set("hash_dict2", pickle.dumps(dic2).decode('latin1'))
    dic11 = pickle.loads(r.get("hash_dict1").encode('latin1'))
    dic22 = pickle.loads(r.get("hash_dict2").encode('latin1'))
    print("dic11:")
    print(dic11)
    print("dic22:")
    print(dic22)
    # print("hash-dic1-redis-value:")
    # print(r.hgetall("hash-dic2"))
    # dic22 = r.hgetall("hash-dic2")
