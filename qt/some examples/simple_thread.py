#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import time

if os.path.expandvars("$ALG_PY3_LIBS") not in sys.path:
    sys.path.append(os.path.expandvars("$ALG_PY3_LIBS"))

from PyQt5 import Qt


class MyThread(Qt.QThread):

    change_value = Qt.pyqtSignal(int)

    def run(self):
        print("Start")
        count = 0
        while count < 100:
            count +=1
            time.sleep(0.1)
            print(count)
            self.change_value.emit(count)

class SimpleThread(Qt.QDialog):
    def __init__(self):
        super(SimpleThread, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):

        self.setMinimumHeight(150)
        self.setMinimumWidth(300)
        
        vbox = Qt.QVBoxLayout()

        self.setLayout(vbox)

        self.progressBar = Qt.QProgressBar()
        self.button = Qt.QPushButton("Start")
        self.button.clicked.connect(self.startProgressBar)

        vbox.addWidget(self.progressBar)
        vbox.addWidget(self.button)

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.progressBar.setValue(val)


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = SimpleThread()
    app.exec_()
    sys.exit()
