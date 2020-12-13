from cv2 import cv2
import numpy as np
import os
from PIL import Image
import math
import operator
from functools import reduce
import time
from src.comAlth.ImageHash import compareIH
from src.comAlth.FourPoint import FourPoint


g1 = os.walk(r"xjcy")
g2 = os.walk(r'muyu')
file_list1 = []
file_list2 = []


def findSimilarPic(file_list1,file_list2,fpoint):
    print(fpoint)
    if(fpoint.dic[fpoint.index]>0):
        fpoint.setCurrentFalse();
        return fpoint
    file1_len = len(file_list1)
    file2_len = len(file_list2)

    smid = int((fpoint.shigh + fpoint.slow)/2)
    bmid = int((fpoint.bhigh + fpoint.blow)/2)

    r = findSimiPic(file_list1, file_list2, fpoint)
    #plus = True
    r.count = 0
    current = fpoint.index
    if(r.getCurrentValue()>0):
        r.setCurrentTrue()
        return r
    else:            
        while(r.isOnWindow()):
            if(r.isOutLeft()):
                r.flag = True
                r.movewindow()
                print(r)
                r = findSimiPic(file_list1, file_list2, r)
                if(r.dic[r.current]>0):
                    r.setCurrentTrue()
                    return r
            elif(r.isOutRight()):
                r.flag = False
                r.movewindow()
                print(r)
                r = findSimiPic(file_list1, file_list2, r)
                if(r.dic[r.current]>0):
                    r.setCurrentTrue()
                    return r
            elif(r.flag):
                print(r)
                r.movewindow()
                r = findSimiPic(file_list1, file_list2,  r)
                if(r.dic[r.current]>0):
                    r.setCurrentTrue()
                    return r
                else:
                    r.flag = not r.flag
            else:
                r.movewindow()
                r = findSimiPic(file_list1, file_list2,  r)
                if(r.dic[r.current]>0):
                    r.setCurrentTrue()
                    return r
                else:
                    r.flag = not r.flag


    r.setCurrentFalse()
    return r

def midFindAll(file_list1,file_list2,fourPoint):
    smid = fourPoint.getSmid()
    bmid = fourPoint.getBmid()
    #找中间
    rm = findSimilarPic(file_list1,file_list2,fourPoint)
    if(smid == slow or smid == shigh):
        return rm
    #找下面
    mid = rm.current
    fl = rm
    
    #dic不同步得问题 TODO
    fl.shigh = mid
    fl.blow = fl.dic[slow]
    fl.bhigh = fl.dic[shigh]
    rl = findSimilarPic(file_list1,file_list2,fourPoint)
    #找上面
    fh = rm
    fh.slow = mid+1
    fh.blow = fh.dic[slow]
    fh.bhigh = fh.dic[shigh]
    rh = findSimilarPic(file_list1,file_list2,fourPoint)

    #返回条件
    rm.shigh = smid

def findSimiPic(file_list1,file_list2,fourPoint):
    file1_len = len(file_list1)
    file2_len = len(file_list2)
    file1_low = fourPoint.blow#dict[low]
    file1_high = fourPoint.bhigh#dict[high]

    file1_index = file1_low
    file2 = file_list2[fourPoint.current]
    while file1_index < file1_high:
        #print(file1_index)
        file1 = file_list1[file1_index-1]
        if(fourPoint.index == 0 and file1_index/file1_len >0.33):
            return fourPoint
        
        # if(index!=0 and index/file2_len*2 <file1_index/file1_len):
        #     return dict

        if(compareIH(file1,file2,4)):
            print("找到相近的图片：", file2, file1, file1_index)
            #dict[index]=file1_index
            fourPoint.dic[fourPoint.current] = file1_index
            return fourPoint
        file1_index+=1
    fourPoint.setCurrentFalse()
    print(fourPoint.current,"没找到")
    return fourPoint


if __name__ == '__main__':
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

    dic = {i: -1 for i in range(file2_len)}
    #dic[file2_len] = file1_len
    mid = int(file2_len/2)
    #flaga,dic,currenta,counta,lowa,higha=findSimilarPic(file_list1,file_list2,dic,0,0,file1_len)
    f1 = FourPoint(False,dic,int(file2_len/2)-1,file2_len-1,int(file1_len/2),file1_len-1,file2_len-1,0,file2_len-1)
    f2 = FourPoint(False, dic, 0,int(file2_len / 2) - 1, 0,  int(file1_len / 2), 0,
                  0, 0)

    rhigh=findSimilarPic(file_list1,file_list2,f1)
    rlow=findSimilarPic(file_list1,file_list2,f2)
    #print(rhigh)

    #print(rlow)
    print(rlow.dic)
    print(rhigh.dic)



