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


flagnow = getLineFormCsvToDict("rescsvcopy.csv")
print(flagnow)
for():
