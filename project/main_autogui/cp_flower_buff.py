# 任务 保持在线，当检测到哈拉BUF后下线且发送通知

import pyautogui
import time
import threading
import cp_config
import cp_image_processing
import cp_communication
import cp_control
from datetime import datetime

class FlowerBuff(threading.Thread):
    sendMsg = "save upload message"
    ex_time=0
    status = "standy"
    #循环2s执行一次 
    times = 120
    sw = False
    def __init__(self):
        threading.Thread.__init__(self)
        self.sw = True

    def run(self):
        self.sw = True
        print("task flower buff start")
        self.status = "start"

        #如果未能成功进入游戏
        if(cp_control.enter_login() == False):
            self.status = "error"
            self.sendMsg = "未能进入游戏" 
            print("任务出错",self.sendMsg)
            vxkey = cp_config.read_VX_KEY_parser()
            if(vxkey != "NULL"):
                cp_communication.vx_post(vxkey,"WOW消息",self.sendMsg)
            return

        else:
            #等待读蓝条
            time.sleep(5)
            #识别图像中花的位置
            flower = cp_image_processing.haveflower()
            if(flower == None):
                vxkey = cp_config.read_VX_KEY_parser()
                if(vxkey != "NULL"):
                    cp_communication.vx_post(vxkey,"WOW消息",self.sendMsg)                
        #尝试次数，每次2s 4分钟    
        times = 120
        # 每次循环有2秒
        while (self.sw):
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))      
            time.sleep(1)
            #如果未找到则将当前鼠标位置作为花的位置
            if(flower == None):
                mouseflower = pyautogui.position()
                deviation = (mouseflower.x,mouseflower.y-100)
                pyautogui.moveTo(mouseflower,duration=0.1)
            else:
                deviation = (flower.x,flower.y-100)
                pyautogui.moveTo(flower,duration=0.1)

            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(deviation,duration=0.1)

            # 判断是否有风格化BUF
            if(cp_image_processing.haveBuffFlower()):
                cp_control.return_login_screen()
                self.sendMsg="风歌花获取成功"
                break
            else:
                if(self.times<=0):
                    self.sendMsg="尝试超时"
                    cp_control.return_login_screen()
                    break    
            self.times = self.times-1

        #只有当通过循环内部退出才发生消息
        if(self.sw == True):
            vxkey = cp_config.read_VX_KEY_parser()
            if(vxkey != "NULL"):
                cp_communication.vx_post(vxkey,"WOW消息",self.sendMsg)
            else:
                pass
        else:
            self.sendMsg = "手动退出了任务"

        self.status = "end"        
        print("退出了循环",self.sendMsg)



    def getStatus(self):
        return self.status
    def getMsg(self):
        return self.sendMsg

    def closeTask(self):
        self.sw=False



