import loopkey
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QMainWindow
from PyQt5.QtCore import QRegExp,QVersionNumber,QT_VERSION_STR
from PyQt5.QtGui import QIcon,QRegExpValidator, QIntValidator, QDoubleValidator
from loopkey_ui import Ui_MainWindow

class loop_main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        self.lk = loopkey.LoopKey()
        super(loop_main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("重复输入工具")
        self.init()

    def init(self):
        # 开始按键
        self.pushButton.clicked.connect(self.pushButton_event)
        # 结束按键
        self.pushButton_2.clicked.connect(self.pushButton_event2)

        # 限制为数字和字符
        self.lineEdit.setPlaceholderText("只能键入数字和字符") 
        reg = QRegExp("[a-zA-Z0-9]+$")
        LE1Validator = QRegExpValidator(self)
        LE1Validator.setRegExp(reg)
        self.lineEdit.setValidator(LE1Validator)
        #设置浮点数限制 范围0~86400，小数点1位
        LE2Validator = QDoubleValidator(self)
        LE2Validator.setRange(0, 86400)
        LE2Validator.setNotation(QDoubleValidator.StandardNotation)
        LE2Validator.setDecimals(1)
        self.lineEdit_2.setValidator(LE2Validator)
        self.lineEdit_2.setPlaceholderText("最小为0.1s")

        self.lineEdit_3.setValidator(LE2Validator)
        self.lineEdit_3.setPlaceholderText("最小为0.1s")


        # 启动后台
        self.lk.start()

    # 重构窗体退出函数，在退出的时候同时也结束建立的线程
    def closeEvent(self,event):
        print("123")
        self.lk.close()



    # 开始按键事件
    def pushButton_event(self):
        self.pushButton.setEnabled(False)
        inputMsg = self.lineEdit.text()
        if(inputMsg == ''):
            print("输入为空")
        else:
            # print(inputMsg)
            self.lk.set_str(inputMsg)
            pass
        try:
            inputKeyInterval = float(self.lineEdit_2.text())
            inputInterval = float(self.lineEdit_3.text())

            self.lk.set_interval_s(inputInterval)
            self.lk.set_key_interval_s(inputKeyInterval)

        except ValueError:
            print("传入参数错误")
        self.lk.push_start()

    # 结束事件按键
    def pushButton_event2(self):
        self.pushButton.setEnabled(True)
        self.lk.push_stop()
        print("222")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = loop_main()
    win.show()
    sys.exit(app.exec_())


