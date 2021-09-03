# 窗体相关
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QMainWindow
from PyQt5.QtCore import QTimer,QRegExp
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator
from ble_pygatt_ui import Ui_MainWindow
import pygatt


class ble_Tool(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ble_Tool, self).__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        self.adapter = None
        #绑定按键    
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.disconnect)
        self.pushButton_3.clicked.connect(self.send)
        self.textBrowser.insertPlainText("初始化完成"+"\n\n")
        #限制输入
        reg = QRegExp("[a-zA-Z0-9]+$")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit.setValidator(LE1Validator)
        self.lineEdit_2.setValidator(LE1Validator)
        self.lineEdit_3.setValidator(LE1Validator)
        self.lineEdit_4.setValidator(LE1Validator)
        self.lineEdit_5.setValidator(LE1Validator)

    def connect(self):
        mac = self.lineEdit.text()
        uuid_1 = self.lineEdit_2.text()
        uuid_2 = self.lineEdit_3.text()
        
        self.textBrowser.insertPlainText("点击了连接"+"\n\n")
        self.adapter = pygatt.GATTToolBackend(search_window_size=2048)
        self.adapter.start()
        self.device = self.adapter.connect("54:B7:E5:79:F4:49")
        self.device.subscribe("0000fff1-0000-1000-8000-00805f9b34fb",
                         callback=self.dataCallback,
                         indication=True)

    def send(self):
        self.textBrowser.insertPlainText("点击了发送"+"\n\n")
        if(self.adapter == None):
            self.textBrowser.insertPlainText("未建立连接"+"\n\n")
            return

    def dataCallback(self,handle,value):
        print("Data: {}".format(value.hex()))
        print("Handle: {}".format(handle))

    def disconnect(self):
        self.textBrowser.insertPlainText("点击了断开"+"\n\n")
        if(self.adapter != None):
            self.adapter.stop()
            self.adapter = None
    def closeEvent(self,event):
        sys.exit(app.exec_())        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ble_Tool()
    win.show()
    sys.exit(app.exec_())
