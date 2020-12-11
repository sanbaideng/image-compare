class FourPoint(object):
    def __init__(self, flag, dic, slow, shigh, blow, bhigh, index, count,current):
        self.flag = flag
        self.dic = dic
        self.slow = slow
        self.shigh = shigh
        self.blow = blow
        self.bhigh = bhigh
        self.count  = count
        self.index = index
        self.current = current

    def setCurrentFalse(self):
        self.flag = False
        self.dic[self.index] = -2
        return self
    def setCurrentTrue(self):
        self.flag = True
        #self.dic[self.index] = -2
        return self
    def getCurrentStatus(self):
        return self.flag
    def getCurrentValue(self):
        return self.dic[self.index]
    def setCountAndOne(self):
        self.count=self.count+1
        return self
    def movewindow(self):
        print("movewindow")
        if(self.flag):
            self.current = self.index + self.count
        else:
            self.current = self.index - self.count
        self.count = self.count + 1
    def isOnWindow(self):
        if(self.index - self.count >= self.slow
                or self.index + self.count <= self.shigh):
            return True
        else:
            return False
    def nextIndex(self):
        if(self.flag):
            self.current = self.index + self.count
            return self
        else:
            self.current = self.index - self.count
            return self
        self.count = self.count + 1
    def isOutRight(self):
        print("右边到顶了")
        if(self.index + self.count > self.shigh):
            return True
        else:
            return False
    def isOutLeft(self):
        print("左边到顶了")
        if(self.index - self.count < self.slow):
            return True
        else:
            return False
    def getSmid(self):
        return int((self.slow+self.shigh)/2)
    def getBmid(self):
        return int((self.blow+self.bhigh)/2)

    def __str__(self):
        return 'flag：%s , slow：%s , shigh：%s, blow：%s , bhigh：%s , index：%s , count：%s , current：%s  ' % (self.flag, self.slow, self.shigh, self.blow, self.bhigh, self.index, self.count,self.current)