from threading import Thread
from time import sleep

try:
    from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt ,QThread
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QApplication
except ImportError:
    from PySide2.QtCore import QObject, Signal as pyqtSignal, QTimer, Qt,QThread
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QApplication



class UpdateThread(QThread):
    #定义个信号
    trigger = pyqtSignal(int)
    def run(self):
        self.i = 0
        for i in range(101):
            self.i += 1
            self.trigger.emit(i)
            sleep(1)
        self.i = 0
        self.trigger.emit(i)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)
        QTimer.singleShot(2000, self.doStart)

        # 什么线程的类
        self.loop = UpdateThread()

    def display(self,v):
        self.progressBar.setValue(v)

    def doStart(self):
        #类中传递的信号将被抛向display函数
        self.loop.trigger.connect(self.display)
        #启动线程
        self.loop.start()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
