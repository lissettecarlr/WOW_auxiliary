# 窗体相关
from logging import log
import sys
import uuid
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QMainWindow
from PyQt5.QtCore import QTimer,QRegExp,QThread, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator
from ble_pygatt_ui import Ui_MainWindow
import pygatt

import threading

import queue
from loguru import logger
import time

class ble_Tool(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ble_Tool, self).__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        global q
        global show
        # show = self.textBrowser
        q = queue.Queue()
        # self.loop = ble_show_loop()
        #定义
        self.loop = showLoop()
        # 线程自定义信号连接的槽函数
        self.loop.trigger.connect(self.display)

        self.adapter = None
        self.defaultMac = "54:B7:E5:79:F4:49"
        self.defaultUUID = "0000fff1-0000-1000-8000-00805f9b34fb"
        self.defaultUUID_2 = "0000f101-0000-1000-8000-00805f9b34fb"
        #绑定按键    
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.disconnect)
        self.pushButton_3.clicked.connect(self.send)

        #限制输入
        reg = QRegExp("([a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2})")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit_3.setValidator(LE1Validator)

        reg2 = QRegExp("[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}")
        LE1Validator2 = QRegExpValidator(self)
        LE1Validator2.setRegExp(reg2)        
        self.lineEdit_2.setValidator(LE1Validator2)
        self.lineEdit.setValidator(LE1Validator2)
        self.lineEdit_4.setValidator(LE1Validator2)
        self.lineEdit_5.setValidator(LE1Validator2)

        self.lineEdit_3.setText(self.defaultMac)
        self.lineEdit_2.setText(self.defaultUUID)
        self.lineEdit.setText(self.defaultUUID_2)

        self.loop.start()
        logger.info("init ok")

    def connect(self):
        self.mac = self.lineEdit_3.text()
        self.uuid_1 = self.lineEdit_2.text()
        self.uuid_2 = self.lineEdit.text()
        #清除显示
        self.textBrowser.clear()
        self.adapter = pygatt.GATTToolBackend(search_window_size=2048)
        try:
            self.adapter.start()
            self.device = self.adapter.connect(self.mac)
            self.device.subscribe(self.uuid_1,
                         callback=self.dataCallback,
                         indication=True)
            self.device.subscribe(self.uuid_2,
                         callback=self.dataCallback2,
                         indication=True)        
        except:
            self.textBrowser.insertPlainText("连接失败"+"\n\n")
            self.disconnect()
        self.textBrowser.insertPlainText("连接成功"+"\n\n")
        #清空接收队列
        logger.info("clear queue")
        while(q.empty() == False):
            temp = q.get()
        logger.info("clear queue over")
        

        #打开更新循环
        self.loop.rcvStart()


    def display(self,str):
        self.textBrowser.insertPlainText(str + "\n")
        self.textBrowser.moveCursor(win.textBrowser.textCursor().End) 

    def send(self):
        self.textBrowser.insertPlainText("点击了发送"+"\n\n")
        if(self.adapter == None):
            self.textBrowser.insertPlainText("未建立连接"+"\n\n")
            return
    # 将数据存入缓冲区
    def setTextBrowser(self,str):
        q.put(str)
        logger.info(f"queue input：{str}")
        logger.info(f"queue size{q.qsize()}")
        #self.textBrowser.insertPlainText(str + "\n")
        #self.textBrowser.moveCursor(win.textBrowser.textCursor().End)

    def dataCallback(self,handle,value): 
        str = "U1:" + format(value.hex())
        self.setTextBrowser(str)
        # _thread.start_new_thread(self.setTextBrowser,("U1：",format(value.hex()),) )
        #print("Data: {}".format(value.hex()))
        #print("Handle: {}".format(handle))

    def dataCallback2(self,handle,value):
        str = "U2:" + format(value.hex())
        self.setTextBrowser(str)
        # _thread.start_new_thread(self.setTextBrowser,(str,) )
        # self.textBrowser.insertPlainText("U2："+format(value.hex())+"\n")
        # self.textBrowser.moveCursor(win.textBrowser.textCursor().End)

    def disconnect(self):
        self.textBrowser.insertPlainText("点击了断开"+"\n\n")
        if(self.adapter != None):
            self.adapter.stop()
            self.adapter = None
        self.loop.rcvStop()

    def closeEvent(self,event):
        self.loop.closeLoop()
        sys.exit(app.exec_())        


# 用于从缓冲区取出接受到的蓝牙数据，发送给UI进行显示
# class ble_show_loop(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.closeFlag = False
#         self.alive =True
#     def run(self):
#         logger.info("loop start")
#         while self.alive:
#             #如果队列中有数据，则取出输出到显示区域
#             if(self.closeFlag==True and q.qsize()>0):
#                 str = q.get()#取出
#                 logger.info("queue output")
#                 show.insertPlainText(str + "\n")
#                 show.moveCursor(win.textBrowser.textCursor().End)
#             else:
#                 time.sleep(0.1)
#         logger.info("loop end")

#     def closeLoop(self):
#         self.alive = False

#     def rcvStart(self):
#         #清空队列
#         logger.info("clear queue")
#         while(q.empty() == False):
#             temp = q.get()
#         logger.info("clear queue over")
#         self.closeFlag = True

#     def rcvStop(self):
#         self.closeFlag = False

class showLoop(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)
    closeFlag = False
    alive =True

    def run(self):
        logger.info("loop start")
        while self.alive:
             #如果队列中有数据，则取出输出到显示区域
            if(self.closeFlag==True and q.qsize()>0):
                str = q.get()#取出
                logger.info("queue output")
                self.trigger.emit(str)
            else:
                 time.sleep(0.1)
        logger.info("loop end")

    def rcvStart(self):
        self.closeFlag = True

    def rcvStop(self):
        self.closeFlag = False
        
    def closeLoop(self):
        self.alive = False        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ble_Tool()
    win.show()
    sys.exit(app.exec_())
