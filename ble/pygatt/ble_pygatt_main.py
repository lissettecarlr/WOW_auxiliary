# 窗体相关
import sys
from typing import Type
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QRegExp,QThread, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator
from ble_pygatt_ui import Ui_MainWindow
import pygatt
import queue
from loguru import logger
import time
import binascii
# 以下是TCP连接需要的包
from simpletcp.clientsocket import ClientSocket
from queue import Queue

class ble_Tool(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ble_Tool, self).__init__()
        self.setupUi(self)
        self.init()
        
    def init(self):
        global q
        q = queue.Queue()
        #定义
        self.loop = showLoop()
        self.tcpLoop = tcpConnect()
        # 线程自定义信号连接的槽函数
        self.loop.trigger.connect(self.display)
        self.tcpLoop.trigger.connect(self.display)
        # UI变更
        self.statusBar =  QStatusBar()
        self.setStatusBar(self.statusBar)

        self.setWindowTitle('自用的蓝牙工具')
        self.setFixedSize(self.width(), self.height())
        self.lineEdit_5.setPlaceholderText("发送通道UUID") 
        self.lineEdit_2.setPlaceholderText("需要监听的UUID-1")
        self.lineEdit.setPlaceholderText("需要监听的UUID-2")
        self.lineEdit_3.setPlaceholderText("需要连接的蓝牙MAC地址")
        self.lineEdit_4.setPlaceholderText("发送的内容，输入HEX") 
        

        # 一些默认值
        self.adapter = None
        self.defaultMac = "54:B7:E5:79:F4:49"
        self.defaultUUID = "0000fff1-0000-1000-8000-00805f9b34fb"
        self.defaultUUID_2 = "0000f101-0000-1000-8000-00805f9b34fb"
        self.defaultSendUUID = '0000f102-0000-1000-8000-00805f9b34fb'
        self.defaultSendCmd = 'A401FF'
        self.serverIp = '47.108.178.9'
        self.serverPort='3001'

        #绑定按键    
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.disconnect)
        self.pushButton_3.clicked.connect(self.send)
        self.action111.triggered.connect(self.scan)
        self.action222.triggered.connect(self.findServer)
        self.pushButton_4.clicked.connect(self.connectServer)
        self.actionTCP.triggered.connect(self.testTcpSend)

        # 绑定复选框状态改变回调
        self.checkBox.stateChanged.connect(self.choose1)
        self.checkBox_2.stateChanged.connect(self.choose2)
        self.checkBox_3.stateChanged.connect(self.choose3)
        #限制输入 MAC
        reg = QRegExp("([a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2}:[a-f0-9A-F]{2})")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit_3.setValidator(LE1Validator)

        # UUID
        reg2 = QRegExp("[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}")
        LE1Validator2 = QRegExpValidator(self)
        LE1Validator2.setRegExp(reg2)        
        self.lineEdit_2.setValidator(LE1Validator2)
        self.lineEdit.setValidator(LE1Validator2)
        self.lineEdit_5.setValidator(LE1Validator2)

        # IP  port
        reg3 = QRegExp("((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)")
        LE1Validator3 = QRegExpValidator(self)
        LE1Validator3.setRegExp(reg3)        
        self.lineEdit_6.setValidator(LE1Validator3)

        reg4 = QRegExp("^([0-9]|[1-9]\\d|[1-9]\\d{2}|[1-9]\\d{3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5])$")
        LE1Validator4 = QRegExpValidator(self)
        LE1Validator4.setRegExp(reg4)        
        self.lineEdit_7.setValidator(LE1Validator4)


        # 设置默认值
        self.lineEdit_3.setText(self.defaultMac)
        self.lineEdit_2.setText(self.defaultUUID)
        self.lineEdit.setText(self.defaultUUID_2)
        self.lineEdit_5.setText(self.defaultSendUUID)
        self.lineEdit_4.setText(self.defaultSendCmd) 
        self.lineEdit_6.setText(self.serverIp)
        self.lineEdit_7.setText(self.serverPort)

        # HEX
        reg3 = QRegExp("^[0-9A-Fa-f]+$")
        LE1Validator3 = QRegExpValidator(self)
        LE1Validator3.setRegExp(reg3) 
        self.lineEdit_4.setValidator(LE1Validator3)

        self.loop.start()
        logger.info("init ok")

    def connect(self):
        self.mac = self.lineEdit_3.text()
        self.uuid_1 = self.lineEdit_2.text()
        self.uuid_2 = self.lineEdit.text()
        self.macHex = bytes.fromhex(self.mac.replace(':',''))

        self.statusBar.showMessage('点击了连接',5000)
        #清除显示
        self.textBrowser.clear()
        if sys.platform.startswith('win'):
            logger.info("win")
            self.textBrowser.insertPlainText("该软件被运行在Windows上，如果点击连接没有反应，则大概率是适配器不支持，请切换到linux平台"+"\n\n")
            self.adapter = pygatt.BGAPIBackend()
        else:
            self.adapter = pygatt.GATTToolBackend()
        try: 
            self.adapter.start()
            self.device = self.adapter.connect(self.mac)
            self.device.subscribe(self.uuid_1,
                         callback=self.dataCallback)
            self.device.subscribe(self.uuid_2,
                         callback=self.dataCallback2,
                         indication=True)        
        except:
            self.textBrowser.insertPlainText("连接失败"+"\n\n")
            self.disconnect()
            return
        self.textBrowser.insertPlainText("连接成功"+"\n\n")
        #清空接收队列
        logger.info("clear queue")
        while(q.empty() == False):
            temp = q.get()
        logger.info("clear queue over")
        
        #打开更新循环
        self.loop.rcvStart()

    # 用于在UI中显示字符串，作为信号接收后的处理函数
    def display(self,str):
        self.textBrowser.insertPlainText(str + "\n")
        self.textBrowser.moveCursor(win.textBrowser.textCursor().End) 

    def send(self):
        sendUUID = self.lineEdit_5.text()
        sendStr = self.lineEdit_4.text()
        # 字符串转hex
        # data = sendStr.encode("utf-8")
        # logger.info(f"send:{type(sendUUID)},{sendUUID}-{type(data)}{sendStr}")
        # self.device.char_write(sendUUID,)
        # test = bytearray(sendStr,'utf-8')

        # sendbin = sendStr.encode("utf-8")
        # test = binascii.unhexlify(sendbin)
        # test2 = bytearray([0XA4,0X01,0XFF])
        # test3 = bytearray(test)
        # logger.info(f"{test}")
        # logger.info(f"{test2}")
        # logger.info(f"{test3}")
        # logger.info(f"bytearray1:{bytearray(sendStr,'utf-8')}")
        # logger.info(f"bytearray2:{bytearray([0XA4,0X01,0XFF])}")
  
        #self.textBrowser.insertPlainText("点击了发送"+"\n\n")
        self.statusBar.showMessage('点击了发送',5000)
        if(self.adapter == None):
            self.textBrowser.insertPlainText("未建立连接"+"\n\n")
            return
        else:
            self.device.char_write(sendUUID,bytearray(binascii.unhexlify(sendStr.encode("utf-8"))))
    # 将数据存入缓冲区
    def setTextBrowser(self,str):
        q.put(str)
        logger.info(f"queue input：{str}")
        logger.info(f"queue size{q.qsize()}")

    def dataCallback(self,handle,value):
        # logger.info(f"d:{format(value.hex())}")
    
        # TCP上行
        if(self.checkBox.isChecked() and self.tcpLoop.getStatus()):
            if(self.checkBox_3.isChecked()):
                data = self.encode(value,self.macHex)
                self.tcpLoop.send(data)
                logger.info("encode TCP upload")
            else:#原样上行
                data = value
                self.tcpLoop.send(data)
                logger.info("TCP upload")
        # UI显示
        str = "U1:" + format(value.hex())
        self.setTextBrowser(str)


    def dataCallback2(self,handle,value):
        if(self.checkBox_2.isChecked()):
            self.tcpLoop.send(value)
        str = "U2:" + format(value.hex())
        self.setTextBrowser(str)

    def disconnect(self):
        self.textBrowser.insertPlainText("\n"+"断开连接"+"\n\n")
        self.statusBar.showMessage('点击了断开',5000)
        if(self.adapter != None):
            self.adapter.stop()
            self.adapter = None
        self.loop.rcvStop()

    def closeEvent(self,event):
        self.loop.closeLoop()
        self.tcpLoop.close()
        sys.exit(app.exec_())     

    def scan(self):
        self.statusBar.showMessage('点击了扫描',5000)
        #如果已有连接则需要断开
        self.textBrowser.insertPlainText("\n"+"该功能有BUG，未开放"+"\n\n")
        return # 这个库的扫描有BUG，暂时不用
        if(self.adapter!=None):
            self.disconnect()
        try:    
            if sys.platform.startswith('win'):
                self.adapter = pygatt.BGAPIBackend()
            else:
                self.adapter = pygatt.GATTToolBackend(search_window_size=2048)        
            self.adapter.start()
            devices = self.adapter.scan()
            for dev in devices:
                self.textBrowser.insertPlainText("address:"+dev['address']+", name:"+dev['name']+"\n")
            self.adapter.stop()
        except:
            self.textBrowser.insertPlainText("\n"+"扫描失败"+"\n\n")
    

    def findServer(self):
        self.statusBar.showMessage('点击了发现服务',5000)
        # self.mac = self.lineEdit_3.text()
        try:
            # if(self.adapter==None):
            #     self.adapter = pygatt.GATTToolBackend(search_window_size=2048)
            #     self.adapter.start()
            #     self.device = self.adapter.connect(self.mac)

            for uuid in self.device.discover_characteristics().keys():
                try:
                    #print("Read UUID %s (handle %d)" %(uuid, self.device.get_handle(uuid) ))
                    logger.info(f"UUID:{uuid},(handle {self.device.get_handle(uuid)})")
                    self.setTextBrowser(f"UUID:{uuid},(handle {self.device.get_handle(uuid)})")
                except:
                    #print("Read UUID %s (handle %d): %s" %(uuid, self.device.get_handle(uuid), "!deny!"))    
                    logger.info(f"UUID:{uuid},(handle {self.device.get_handle(uuid)}) deny")   
                    self.setTextBrowser(f"UUID:{uuid},(handle {self.device.get_handle(uuid)}) deny")
        except:
            self.textBrowser.insertPlainText("发现服务失败,请先连接设备"+"\n\n")
    # 复选框状态改变回调    
    def choose1(self):
        if(self.checkBox.isChecked()):
            self.statusBar.showMessage('将会向服务器发送UUID_1数据',3000)
        else:
            self.statusBar.showMessage('取消向服务器发送UUID_1数据',3000)

    def choose2(self):
        if(self.checkBox_2.isChecked()):
            self.statusBar.showMessage('将会向服务器发送UUID_2数据',3000)
        else:
            self.statusBar.showMessage('取消向服务器发送UUID_2数据',3000)
    
    def choose3(self):
        if(self.checkBox_3.isChecked()):
            self.statusBar.showMessage('将会启用数据封包',3000)
        else:
            self.statusBar.showMessage('取消数据封包，源数据直接上传',3000)

    def connectServer(self):
        self.serverIp = self.lineEdit_6.text()
        self.serverPort = self.lineEdit_7.text()
        self.textBrowser.insertPlainText(f"尝试连接服务器({self.serverIp},{self.serverPort})"+'\n')
        self.tcpLoop.init(self.serverIp,int(self.serverPort))
        try:
            self.tcpLoop.start()
        except:
            self.textBrowser.insertPlainText(f"TCP连接建立失败")


    # 自定义封包 示例：包头+地址+长度+原始数据
    def encode(self,data,addr):
        head=b'\xf0\xaa\x01\x01\x02'
        newPck = head + addr
        dataLen = (len(data)).to_bytes(2,byteorder='big')
        newPck = newPck + dataLen + data
        return newPck    

    # 按键回调，和上函数均属于自定义函数，实现数据封包上传 
    def testTcpSend(self):
        if(self.tcpLoop.getStatus()):
            self.mac = self.lineEdit_3.text()
            mac = self.mac.replace(':','')
            logger.info(f"input : {mac}")
            macHex =  bytes.fromhex(mac)
            # 假数据 FC 09 A4 0A 20 11 EB C4 24 A9
            d =b'\xfc\x09\xa4\x0a\x20\x11\xeb\xc4\x24\xa9'
            data = self.encode(d,macHex)
            logger.info(f"test data:{binascii.hexlify(data)}")
            self.tcpLoop.send(data)
            self.textBrowser.insertPlainText("发送TCP测试数据"+"\n\n")
        else:
            self.textBrowser.insertPlainText("请先建立TCP连接"+"\n\n")



        

# 用于UI显示的线程
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

# 用于TCP连接的线程
class tcpConnect(QThread):
    trigger = pyqtSignal(str)

    def init(self,ip,port):
        self.ip = ip
        self.port = port
        self.buffer = Queue(maxsize=0)
        self.socketStatus = False
        self.exitLoop = False

    def run(self):
        while(1):
            self.connectSocket()
            if(self.buffer.qsize() > 0):
                try:
                    self.client.send(self.buffer.get())
                except Exception:
                    logger.error("tcp send fail")
                    self.trigger.emit("TCP发送失败，重新连接")
                    self.socketStatus = False
            else:
                time.sleep(0.1)
            if(self.exitLoop == True):
                break

    def connectSocket(self):
        if(self.socketStatus == True):
            return
        while(1):
            try:
                self.client =  ClientSocket(self.ip, self.port, recv_bytes=0, single_use=False)
                break
            except Exception:
                logger.error("TCP connect fail")
                self.trigger.emit("TCP连接失败")
                time.sleep(10)
        logger.info("TCP connect ok")
        self.trigger.emit("TCP连接成功")
        self.socketStatus = True

    def send(self,data):
        if(self.socketStatus == True):
            self.buffer.put(data)
            return True
        else:
            return False
    def getStatus(self):
        return self.socketStatus
    def close(self):
        self.exitLoop = True



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ble_Tool()
    win.show()
    sys.exit(app.exec_())
