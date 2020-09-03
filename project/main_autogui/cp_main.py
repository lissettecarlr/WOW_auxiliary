import time
import pyautogui
import threading
import string
import sys
import cp_config
import cp_communication
#定时器
import sched


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QMainWindow
from PyQt5.QtCore import QRegExp,QVersionNumber,QT_VERSION_STR
from PyQt5.QtGui import QIcon,QRegExpValidator, QIntValidator, QDoubleValidator
from cp_main_ui import Ui_MainWindow
from PyQt5.QtCore import QTimer

import cp_dragon_buff
import cp_haka_buff
import cp_flower_buff

class main_ui(QtWidgets.QMainWindow,Ui_MainWindow):
    cpTask="NULL"
    cpVXKey="NULL"
    cpTargetTask = None
    lastTaskStatus = "NULL"

    def __init__(self):
        super(main_ui, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("WOW辅助")
        self.init()
      
        # self.ex = dragonhead()

    def init(self):

        self.pushButton.clicked.connect(self.pushButton_event)
        # 结束按键
        self.pushButton_2.clicked.connect(self.pushButton_event2)
        self.comboBox.currentIndexChanged.connect(self.comboxChange_event)
        self.action_KEY.triggered.connect(self.set_SERVERKEY)
        self.action_3.triggered.connect(self.test_communication)
        self.action_5.triggered.connect(self.init_config)
        self.textBrowser.clear()

        self.cpVXKey = cp_config.read_VX_KEY_parser()

        # 用于刷新显示任务状态
        self.timer = QTimer(self)
        pass


    def flushTaskStatus(self):
        # 判断状态是否切换
        status = self.cpTargetTask.getStatus()
        if(self.lastTaskStatus != status):
            self.lastTaskStatus = status
            if(status == "start"):
                self.textBrowser.append("<font color='green' size=10> 任务开始 <font>")
            if(status == "end"):
                self.textBrowser.append("<font color='green' size=10> 任务结束 <font>")
                msg = self.cpTargetTask.getMsg()
                self.textBrowser.append("<font color='green' size=10>"+msg+"<font>")
                self.timer.stop()
                self.pushButton.setEnabled(True)
            if(status == "error"):
                self.textBrowser.append("<font color='red' size=10> 任务发生错误 <font>")
                msg = self.cpTargetTask.getMsg()
                self.textBrowser.append("<font color='red' size=10>"+msg+"<font>")
                self.timer.stop()
                self.pushButton.setEnabled(True)          
        pass
    
    def task_timeout(self):
        self.textBrowser.append("<font color='green' size=10> 延时结束，启动任务 <font>")
        self.timer.stop()
        self.cpTargetTask = cp_flower_buff.FlowerBuff()
        self.cpTargetTask.start()

        self.timer.timeout.connect(self.flushTaskStatus)
        self.timer.start(100)
        pass

    def pushButton_event(self):

        
        self.textBrowser.append("<font color='black' size=2>  确认点击了启动按钮 <font>")
        # 判断是否选择了任务
        if(self.cpTask == "NULL"):
            self.textBrowser.append("<font color='red' size=10>未选择任务<font>") 
            return  
        # 判断是否设置了VX_KEY
        if(self.cpVXKey == "NULL"):
            self.textBrowser.append("<font color='red' size=10>未设置KEY<font>") 
            # return
        
        if(self.cpTask == "暴风龙头"):
            self.textBrowser.append("<font color='green' size=10>准备启动监控龙头任务<font>") 
            self.timer.timeout.connect(self.flushTaskStatus)
            self.timer.start(100)
            self.cpTargetTask = cp_dragon_buff.DragonBuff()
            self.cpTargetTask.start()
        elif(self.cpTask == "哈卡"):
            self.textBrowser.append("<font color='green' size=10>准备启动监控哈卡任务<font>")
            self.timer.timeout.connect(self.flushTaskStatus)
            self.timer.start(100)
            self.cpTargetTask = cp_haka_buff.HakaBuff()
            self.cpTargetTask.start()

        elif(self.cpTask == "风歌花"):
            self.textBrowser.append("<font color='green' size=10>准备风歌花任务<font>")
            # 由于风歌花获取特性，需要设定启动时间
            taskDelay = pyautogui.prompt(text='就输入多少秒。别输入其他乱七八糟的，我还没做限制处理', title='输入启动风歌花任务的延时时间(秒)' , default='')
            if(taskDelay == None):  
                self.textBrowser.append("<font color='black' size=2> 未输入时间，不执行<font>")   
                return

            self.pushButton.setEnabled(False)
            self.textBrowser.append("<font color='black' size=2> 延时时长:"+ taskDelay +"<font>")
            t = int(taskDelay)
 
            self.timer.singleShot(t*1000, self.task_timeout)
            # self.timer.timeout.connect(self.task_timeout)
            # self.timer.start(t*1000)

            return
        else:
            pass

        self.pushButton.setEnabled(False)

    def pushButton_event2(self):
        self.timer.stop()
        self.pushButton.setEnabled(True)
        if(self.cpTargetTask != None):
            self.cpTargetTask.closeTask()
        self.textBrowser.append("<font color='black' size=2>  确认点击了关闭按钮 <font>")

    def comboxChange_event(self):
        self.cpTask = self.comboBox.currentText()
        self.textBrowser.append("<font color='green' size=10> " +"选择任务:" +self.cpTask + "<font>")
        pass

    def set_SERVERKEY(self):
        self.cpVXKey = pyautogui.prompt(text='', title='输入server酱KEY值' , default='')
        if(self.cpVXKey !=None):
            self.textBrowser.append("<font color='yellow' size=2> " +"server酱KEY:" +self.cpVXKey + "<font>")
            cp_config.write_VX_KEY_parser(self.cpVXKey)


    def test_communication(self):
        self.textBrowser.append("<font color='green' size=10> 通讯测试 <font>") 
        cp_communication.vx_post(self.cpVXKey,"test","123456")

    def init_config(self):
        cp_config.set_default_parser()
        self.textBrowser.clear()
        self.cpVXKey="NULL"
    



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = main_ui()
    win.show()
    sys.exit(app.exec_())