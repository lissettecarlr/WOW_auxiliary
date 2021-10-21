# 窗体相关
from logging import log
import sys
from typing import Type
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QRegExp,QThread, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator
from mqtt_client import Ui_MainWindow
import pygatt
import queue
from loguru import logger
import time
import binascii
import paho.mqtt.client as mqtt
from loguru import logger
from datetime import datetime

class mqtt_Tool(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mqtt_Tool, self).__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        self.statusBar =  QStatusBar()
        self.setStatusBar(self.statusBar)
        self.setFixedSize(self.width(), self.height())
        

        #绑定按键
        self.pushButton_send.clicked.connect(self.btSend)
        self.pushButton_connect.clicked.connect(self.btConnect)
        self.pushButton_sub.clicked.connect(self.btSub)
        self.actionrobot.triggered.connect(self.AtRobot)
        self.actionclear.triggered.connect(self.clearText)
        #禁用按键
        self.pushButton_sub.setEnabled(False)
        self.pushButton_send.setEnabled(False)
        
        #初始状态
        self.label_status.setText("未连接")
        self.mqttStatus = False
        self.client = mqtt.Client()
        self.lineEdit_qos1.setText("0")
        self.lineEdit_qos2.setText("0")
        self.lineEdit_port.setText("1883")
        self.topics =[]
        self.lineEdit_ip.setText("broker.emqx.io")

        #mqtt 回调
        self.client.on_connect = self.mqttCallbackConnected
        self.client.on_message = self.mqttCallbackMessage

        #限制输入 MAC
        reg = QRegExp("[0-3]{0,1}")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit_qos1.setValidator(LE1Validator)
        self.lineEdit_qos2.setValidator(LE1Validator)

        reg2 = QRegExp("((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)")
        LE1Validator2 = QRegExpValidator(self)
        LE1Validator2.setRegExp(reg2)        
        self.lineEdit_port.setValidator(LE1Validator2)
        self.statusBar.showMessage('初始化完成',3000)

    def btConnect(self):
        logger.debug("点击了连接")
        if(self.mqttStatus == True):
            return
        #获取地址和IP
        if(self.lineEdit_ip.text()):
            self.mqttIp = self.lineEdit_ip.text()
        else:
            self.mqttIp = "broker.emqx.io"
        
        if(self.lineEdit_port.text()):
            self.mqttPort = int(self.lineEdit_port.text())
        else:
            self.mqttPort = 1883

        logger.info(f"ip:{self.mqttIp},port:{self.mqttPort}")
        
        if(self.lineEdit_name.text() and self.lineEdit_pwd.text()):
            self.client.username_pw_set(self.lineEdit_name.text(),self.lineEdit_pwd.text())
        self.statusBar.showMessage('开始尝试连接服务器',3000)
        #建立连接
        self.client.connect(self.mqttIp,self.mqttPort, 60)
        self.client.loop_start()

    def btSend(self):
        topic = self.lineEdit_topic1.text()
        qos = self.lineEdit_qos1.text()
        msg = self.textEdit.toPlainText()
        logger.info(f"topic:{topic},qos:{qos},msg:{msg}")
        if topic and msg and qos:
            qos = int(qos)
            self.client.publish(topic, msg, qos)
            self.statusBar.showMessage('已发送',3000)
            logger.info(f"send:{topic},{qos},{msg}")
        else:
             self.statusBar.showMessage('发送失败：缺少参数',5000)

    def btSub(self):
        if self.lineEdit_topic2.text() and self.lineEdit_qos2.text():
            subTopic = self.lineEdit_topic2.text()
            subQos = int(self.lineEdit_qos2.text())
            self.topics.append((subTopic, subQos))

            self.client.subscribe(self.topics)
            logger.info(f"增加订阅:{subTopic}")
            self.label_5.setText(str(self.topics))
        else:
            logger.warning("topic or qos is null")
        

    def AtRobot(self):
        pass

    def mqttCallbackConnected(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Server Connected!")
            self.is_connected = True
            self.pushButton_sub.setEnabled(True)
            self.pushButton_send.setEnabled(True)
            self.label_status.setText("已连接")
            logger.info("已连接")
        else:
            self.label_status.setText("连接失败")
            logger.warning("Server Connect Failed, with result code " + str(rc))


    def mqttCallbackMessage(self, client, userdata, msg):
        text = '[%s] %r:%s ' % (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'), msg.topic,
            bytes.decode(msg.payload))
        logger.info(text)
        self.textBrowser_sub.append(text)
        self.textBrowser_sub.moveCursor(win.textBrowser_sub.textCursor().End) 

    def clearText(self):
        self.textBrowser_sub.clear()
        self.statusBar.showMessage('清空显示',3000)

    def closeEvent(self,event):   
        self.client.loop_stop() 
        sys.exit(app.exec_())  

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = mqtt_Tool()
    win.show()
    sys.exit(app.exec_())