# 任务 保持在线，当检测到哈拉BUF后下线且发送通知

import pyautogui
import time
import threading
import cp_config
import cp_image_processing
import cp_communication
import cp_control

class HakaBuff(threading.Thread):
    sendMsg = "save upload message"
    ex_time=0
    status = "standy"
    sw = False
    def __init__(self):
        threading.Thread.__init__(self)
        self.sw = True

    def run(self):
        self.sw = True
        print("task dragon buff start")
        while (self.sw):
            self.status = "start"
            time.sleep(1)

            if(cp_image_processing.isLogout()):
                self.sendMsg = "返回到了登录画面，请前往处理"
                break 
            # 比对图片login.PNG,如果找到则点击
            elif(cp_image_processing.isLogin()):
                #自动小退，手动程序进去游戏
                cp_control.enter_login()
                continue
            # 比对图片bag.PNG，确认是否在游戏画面
            elif(cp_image_processing.isGame()):
                # 比对图片head.PNG，确认是否有龙头BUF
                if(cp_image_processing.haveBuffHaka()):
                    cp_control.return_login_screen()
                    self.sendMsg = "BUF获取成功"
                    break
                else:
                    continue   
            # 以上图片皆未找到则可能是游戏已经退出 
            else:          
                # 进行了20次判断 每次循环是3s
                self.ex_time+=1
                if(self.ex_time>=20):
                    self.sendMsg = "游戏异常退出，请前往处理" 
                    self.ex_time=0
                    break
                print("游戏异常退出",self.ex_time)
                continue

        self.status = "end"        
        print("退出了循环",self.sendMsg)
        #只有当通过循环内部退出才发生消息
        if(self.sw == True):
            vxkey = cp_config.read_VX_KEY_parser()
            if(vxkey != "NULL"):
                cp_communication.vx_post(vxkey,"WOW消息",self.sendMsg)

    def getStatus(self):
        return self.status
    def getMsg(self):
        return self.sendMsg

    def closeTask(self):
        self.sw=False



