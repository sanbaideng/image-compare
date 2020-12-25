import time
import cv2
import os


def calTimeLine(duration, FrameNumber, picNo, cutWindow):
    #cap = cv2.VideoCapture(videoPath)
    # get方法参数按顺序对应下表（从0开始编号)
    # rate = cap.get(cv2.CAP_PROP_FPS)   # 帧速率
    #print("rate", rate)
    # FrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频文件的帧数
    #print("FrameNumber", FrameNumber)
    # duration = FrameNumber/rate  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
    return (duration*picNo*cutWindow)/FrameNumber


dic = []


def readFile():
    cap1 = cv2.VideoCapture('xjcy2.mp4')
    cap2 = cv2.VideoCapture('muyu.flv')
    rate1 = cap1.get(cv2.CAP_PROP_FPS)
    rate2 = cap2.get(cv2.CAP_PROP_FPS)
    FrameNumber1 = cap1.get(cv2.CAP_PROP_FRAME_COUNT)
    FrameNumber2 = cap2.get(cv2.CAP_PROP_FRAME_COUNT)
    duration1 = FrameNumber1/rate1
    duration2 = FrameNumber2/rate2
    curstart1 = 0
    curstart2 = 0
    curend1 = 0
    curend2 = 0

    jumptime = 2
    fp = open("rescsvcopy.csv")
    timecsvfile1 = "time1.csv"
    timecsvfile2 = "time2.csv"
    for index, line in enumerate(fp):
        # print(line)
        #print(line[2], line[3])
        # file2_name = line[2].split('\\')[1]
        # file1_name = line[3].split('\\')[1]
        #print(file2_name[1], file1_name[1])
        frame2 = line.split(' ')[0]
        frame1 = line.split(' ')[1]

        if(index == 0):
            curstart2 = frame2
            curstart1 = frame1
            curend2 = frame2
            curend1 = frame1
            continue

        print("(int(frame2) - int(cur2))/jumptime")
        print((int(frame2) - int(curstart2))/jumptime)
        # 计算前值
        if((int(frame2) - int(curstart2))/jumptime > 10.0):
            # 不是单独的点
            if(curend2 > curstart2):
                # 计算上一个
                muyucut1 = calTimeLine(
                    duration2, FrameNumber2, int(curstart2), 48)
                muyucut2 = calTimeLine(
                    duration2, FrameNumber2, int(curend2), 48)
                sourceCut1 = calTimeLine(
                    duration1, FrameNumber1, int(curstart1), 24)
                sourceCut2 = calTimeLine(
                    duration1, FrameNumber1, int(curend1), 24)
                writecvsLine(timecsvfile1, muyucut1, muyucut2)
                writecvsLine(timecsvfile2, sourceCut1, sourceCut2)

            # 忽略 右移
            curstart2 = frame2
            curend2 = frame2
            curstart1 = frame1
            curend1 = frame1
            continue
        # 计算当前
        else:
            curend1 = frame1
            curend2 = frame2


def writecvsLine(filename, time1, time2):
    fo = open(filename, "a+")
    line = str(time1) + ',' + str(time2) + ',' + '\n'
    fo.write(line)
    fo.close()


def writeLine(filename, line):
    fo = open(filename, "a+")
    fo.writelines(line + '\n')
    fo.close()


if __name__ == '__main__':
    print(time.localtime(time.time()))  # 获得时间元组
    readFile()
    #capFrame('xjcy2.mp4', 'xjcy2', 24)

    print(time.localtime(time.time()))  # 获得时间元组
