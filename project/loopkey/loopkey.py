import pyautogui
import time
import threading


# 使用方式
# t1 = LoopKey() t1.start()将开启一些无线循环线程
# set_str()修改按压字符串
# set_time_s()修改循环时间
# push_start()启动重复输入
# push_stop()关闭重复输入


class LoopKey(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.flag= False
        self.meg = "test"
        self.interval = 1 
        self.key_interval = 0.1
        self.closeFlag = True

    def run(self):
        print('start')
        while 1:
            time.sleep(self.interval)
            if(self.flag):
                # print(self.loopkey_str)
                pyautogui.typewrite(self.meg, interval=self.key_interval) 
            else:
                print('0000')
                pass
            if(self.closeFlag == False):
                break
        print('end')

    def set_str(self,str):
        self.meg = str
        print(self.meg)

    #设置输入每条按键的间隔
    def set_interval_s(self,t):
        if(t<0.1):
            print("输入值不可小于100毫秒")
            return
        print("每次输入间隔"+str(t))
        self.interval = t
    #设置输入按键指令中每个字符的间隔
    def set_key_interval_s(self,t):
        print("字符输入间隔"+str(t))
        self.key_interval = t


    def push_start(self):
        self.flag = True
    def push_stop(self):
        self.flag = False
    def close(self):
        self.closeFlag = False

# t1 = LoopKey()
# t1.start()
# t1.push_start()


