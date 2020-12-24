import time
import cv2
import os


def capFrame(videoPath, savePath, frameNum):
    cap = cv2.VideoCapture(videoPath)
    frame_counter = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(frame_counter)
    print("总张数：", frame_counter/frameNum)
    numFrame = 0
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    while True:
        numFrame += 1
        if numFrame >= frame_counter:
            break
        if numFrame % frameNum != 1:
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, numFrame)

        if cap.grab():
            # 每N桢截取一个图片
            if numFrame % frameNum == 1:
                # retrieve 解码并返回一个桢
                flag, frame = cap.retrieve()
                if not flag:
                    continue
                else:
                    #cv2.imshow('video', frame)
                    newPath = savePath + "\\" + \
                        str(int(numFrame / frameNum)) + ".jpg"
                    cv2.imencode('.jpg', frame)[1].tofile(newPath)
                if ((numFrame / frameNum) % 1000 == 0):
                    print("第", numFrame / frameNum, "张")
        # 检测到按下Esc时，break（和imshow配合使用）
        if cv2.waitKey(10) == 27:
            break


def capFrameNew(savePath, cap, frame_counter, frameNum):
    #cap = cv2.VideoCapture(videoPath)
    #frame_counter = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(frame_counter)
    print("总张数：", frame_counter/frameNum)
    numFrame = 0
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    while True:
        numFrame += 1
        if numFrame >= frame_counter:
            break
        if numFrame % frameNum != 1:
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, numFrame)

        if cap.grab():
            # 每N桢截取一个图片
            if numFrame % frameNum == 1:
                # retrieve 解码并返回一个桢
                flag, frame = cap.retrieve()
                if not flag:
                    continue
                else:
                    #cv2.imshow('video', frame)
                    newPath = savePath + "\\" + \
                        str(int(numFrame / frameNum)) + ".jpg"
                    cv2.imencode('.jpg', frame)[1].tofile(newPath)
                if (int((numFrame / frameNum)) % 1000 == 0):
                    print("第", numFrame / frameNum, "张")
        # 检测到按下Esc时，break（和imshow配合使用）
        if cv2.waitKey(10) == 27:
            break


def calTimeLine(videoPath,   cutWindow):
    cap = cv2.VideoCapture(videoPath)
    # get方法参数按顺序对应下表（从0开始编号)
    rate = cap.get(cv2.CAP_PROP_FPS)   # 帧速率
    print("rate", rate)
    FrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频文件的帧数
    print("FrameNumber", FrameNumber)
    duration = FrameNumber/rate  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
    return duration*picNo*24/FrameNumber


if __name__ == '__main__':
    print(time.localtime(time.time()))  # 获得时间元组
    #print(calTimeLine('xjcy2.mp4', 24, 24))
    #capFrame('xjcy2.mp4', 'xjcy3', 24)

    videoPath = 'xjcy2.mp4'
    savePath = 'xjcy3'
    cap = cv2.VideoCapture(videoPath)
    frame_counter = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    frameNum = 12

    capFrameNew(savePath, cap, frame_counter, frameNum)

    print(time.localtime(time.time()))  # 获得时间元组
