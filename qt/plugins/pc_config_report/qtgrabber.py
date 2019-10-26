#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import time

if os.path.expandvars("$ALG_PY3_LIBS") not in sys.path:
    sys.path.append(os.path.expandvars("$ALG_PY3_LIBS"))

from PyQt5 import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import grabber

class MyThread(Qt.QThread):
    def __init__(self, users_list = None, path_to_save = None):
        super(MyThread, self).__init__()
        self.users_list = users_list
        self.path_to_save = path_to_save
    
    change_value = Qt.pyqtSignal(int)
    isFinish = Qt.pyqtSignal(bool)

    def set_params(self, ul, ps):
        self.users_list = ul
        self.path_to_save = ps

    def run(self):
        self.pyGrab = grabber.Grab(progress_signal=self.change_value, users_list=self.users_list, path_to_save_report=self.path_to_save)
        if self.isRender():
            self.pyGrab.start_grabber(get_render=True)
        else:
            self.pyGrab.start_grabber(get_render=False)
        self.isFinish.emit(True)
    
    def stop(self):
        self.terminate()

    def isRender(self):
        for i in self.users_list:
            if 'render' in i:
                return True
        return False

class Grabber(QtWidgets.QWidget):

    def __init__(self): 
        super(Grabber, self).__init__()
        self.path_exist = False
        self.path_to_save = os.path.realpath('report.xlsx')
        self.path_to_users_list = '/home/vlad/vladcode/qt/plugins/grabber/hosts_list_with_renders.txt'
        self.host_list = None
        self.thread = MyThread()
        self.initUI()
        self.show()

    def initUI(self):

        #Start settings
        self.setWindowTitle('Information collection')
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMaximumHeight(300)
        mainLayout = Qt.QGridLayout()
        self.setLayout(mainLayout)

        #Add button
        self.buttonStart = Qt.QPushButton('Start', self)
        self.buttonSelectHostList = Qt.QPushButton('Select', self)
        self.buttonSave = Qt.QPushButton('Save', self)
        self.buttonStop = Qt.QPushButton('Stop', self)
        self.buttonStop.setDisabled(True)
        
        #Add progressbar
        self.progressBar = Qt.QProgressBar()

        #Add label
        self.labelInfo = Qt.QLabel('')
        self.check_path_to_user_list(self.path_to_users_list)
        self.labelSave = Qt.QLabel('File to save :')

        #Add lineEdit
        self.lineFx = Qt.QLineEdit(self)
        self.lineRender = Qt.QLineEdit(self)
        self.linePathToPc = Qt.QLineEdit(self)
        self.linePathToSave = Qt.QLineEdit(self)

        #Add checkbox
        self.checkAll = Qt.QCheckBox('All')
        self.checkFx = Qt.QCheckBox('FX')
        self.checkRender = Qt.QCheckBox('Render')
        
        #Settings for lineedit
        self.lineFx.setText('')
        self.lineFx.setFixedWidth(175)
        self.lineFx.setDisabled(True)
        self.lineRender.setText('')
        self.lineRender.setFixedWidth(175)
        self.lineRender.setDisabled(True)
        self.linePathToPc.setFixedWidth(175)
        self.linePathToPc.setText(self.path_to_users_list)
        self.linePathToSave.setFixedWidth(175)
        self.linePathToSave.setText(self.path_to_save)
        self.linePathToSave.setReadOnly(True)
        self.linePathToPc.setReadOnly(True)

        #Settings for checkbox 
        self.checkAll.setChecked(True)

        #Settings for progressbar
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        #Add on layout
        mainLayout.addWidget(self.checkAll, 1,0)
        mainLayout.addWidget(self.buttonSelectHostList, 1, 2)
        mainLayout.addWidget(self.linePathToPc, 1,1)
        mainLayout.addWidget(self.checkFx, 2,0)
        mainLayout.addWidget(self.checkRender, 3,0)
        mainLayout.addWidget(self.lineFx, 2,1)
        mainLayout.addWidget(self.lineRender, 3,1)
        mainLayout.addWidget(self.labelSave, 4, 0)
        mainLayout.addWidget(self.buttonSave, 4, 2)
        mainLayout.addWidget(self.linePathToSave, 4,1)
        mainLayout.addWidget(self.labelInfo, 5, 0)
        mainLayout.addWidget(self.buttonStart, 5, 1)
        mainLayout.addWidget(self.buttonStop, 5, 2)
        mainLayout.addWidget(self.progressBar, 6, 0, 1, 0)
        
        #Connect
        self.checkAll.stateChanged.connect(self.checkBoxAll)
        self.checkFx.stateChanged.connect(self.checkBoxFxRender)
        self.checkRender.stateChanged.connect(self.checkBoxFxRender)
        self.buttonStart.clicked.connect(self.start_grab)
        self.buttonSave.clicked.connect(self.get_path_to_save)
        self.buttonStop.clicked.connect(self.stopThread)
        self.buttonSelectHostList.clicked.connect(self.get_path_to_host_list)
        self.linePathToPc.textChanged.connect(self.check_path_to_user_list)
        self.lineFx.textChanged.connect(self.infoAboutFxRender)
        self.lineRender.textChanged.connect(self.infoAboutFxRender)
    
    def startProgressBar(self, users_list = None, path_to_save = None):
        self.thread.set_params(users_list,path_to_save)
        self.progressBar.setMaximum(len(users_list))
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.isFinish.connect(self.resetState)
        self.thread.start()

    def stopThread(self):
        self.thread.stop()
        print('Work end..')
        self.progressBar.setValue(0)
        self.buttonStop.setDisabled(True)
        self.buttonStart.setDisabled(False)
        self.progressBar.setVisible(False)

    def resetState(self, boolean):
        if boolean:
            self.progressBar.setValue(0)
            self.buttonStop.setDisabled(True)
            self.buttonStart.setDisabled(False)
            self.progressBar.setVisible(False)

    def setProgressVal(self, val):
        self.progressBar.setValue(val)

    def infoAboutFxRender(self):
        self.labelInfo.setText('ex: 1,2,3,4 | 1-4')

    def checkBoxAll(self):
        if self.checkAll.isChecked():
            self.lineRender.setDisabled(True)
            self.checkFx.setChecked(False)
            self.checkRender.setChecked(False)
            self.checkAll.setChecked(True)
            self.lineFx.setDisabled(True)
            self.linePathToPc.setDisabled(False)
            self.check_path_to_user_list(self.linePathToPc.text())
            self.buttonSelectHostList.setDisabled(False)
        else:
            self.linePathToPc.setDisabled(True)
            self.buttonSelectHostList.setDisabled(True)

    def checkBoxFxRender(self):

        if self.checkFx.isChecked():
            self.checkAll.setChecked(False)
            self.linePathToPc.setDisabled(True)
            self.lineFx.setDisabled(False)
            self.infoAboutFxRender()
        else:
            self.lineFx.setDisabled(True)
        
        if self.checkRender.isChecked():
            self.checkAll.setChecked(False)
            self.linePathToPc.setDisabled(True)
            self.lineRender.setDisabled(False)
            self.infoAboutFxRender()
        else:
            self.lineRender.setDisabled(True)

    def get_path_to_host_list(self):
        options = Qt.QFileDialog.Options()
        options |= Qt.QFileDialog.DontUseNativeDialog
        fileName, _ = Qt.QFileDialog.getOpenFileName(self,"Select host list..", "","Text files (*.txt)", options=options)
        if fileName:
            self.path_to_users_list = fileName
            self.linePathToPc.setText(self.path_to_users_list)

    def get_path_to_save(self):
        options = Qt.QFileDialog.Options()
        options |= Qt.QFileDialog.DontUseNativeDialog
        fileName, ex = Qt.QFileDialog.getSaveFileName(self,"Where save report file?","","Excel file (*.xlsx)", options=options)
        if fileName:
            self.path_to_save = fileName + '.xlsx'
            self.linePathToSave.setText(self.path_to_save)
    
    def check_path_to_user_list(self, path):

        if os.path.isfile(path):
            self.labelInfo.setText('Host list found!')
            self.path_exist = True
        else:
            self.labelInfo.setText('Specify the correct path to the host list..')
            self.path_exist = False

    def check_modify_name_pc(self, string, lineName):
        if len(string) > 0 and string[0] != '-':
            if ((',' in string) or ('-' in string)) and (str(string.replace(',', '').strip()).isdigit() or str(string.replace("-", '').strip()).isdigit()):
                string = string.strip()
                if ',' in string:
                    string = list(set(string.split(',')))
                    if string[0] == '':
                        string.pop(0)
                    return string
                if '-' in string:
                    string = string.split('-')
                    string = list(range(int(string[0]), int(string[1]) + 1))
                    string = list(set(string))
                    if string[0] == '':
                        string.pop(0)
                    return string
            elif string.strip().isdigit():
                a = list()
                a.append(string.strip())
                return a
            else:
                if lineName == 1:
                    self.lineFx.setText('')
                elif lineName == 0:
                    self.lineRender.setText('')
        else:
            return -1
    
    def add_prefix(self, array, prefix):
        for i in range(len(array)):
            if len(str(array[i])) == 1:
                array[i] = '0' + str(array[i])
            array[i] = prefix + str(array[i])
        return array

    def start_grab(self):

        self.buttonStop.setDisabled(False)
        self.buttonStart.setDisabled(True)
        self.progressBar.setVisible(True)

        if self.checkAll.isChecked() and self.path_exist:
            self.path_to_users_list = self.linePathToPc.text()
            # print('path: ', self.path_to_users_list)
            with open(self.path_to_users_list, 'r') as f:
                self.host_list = f.read().split('\n')
            
        if self.checkFx.isChecked() and not self.checkRender.isChecked():
            fx = self.check_modify_name_pc(self.lineFx.text(), 1)
            if fx is not None and fx != -1:
                fx = self.add_prefix(fx, "fx")
                # print('fx: ', fx)
                self.host_list = fx
            else:
                print('Check the supplied value in fx!')

        if self.checkRender.isChecked() and not self.checkFx.isChecked():
            render = self.check_modify_name_pc(self.lineRender.text(), 0)
            if render is not None and render != -1:
                render = self.add_prefix(render, "render")
                # print('render: ', render)
                self.host_list = render
            else:
                print('Check the supplied value in render!')
        
        if self.checkRender.isChecked() and self.checkFx.isChecked():
            render = self.check_modify_name_pc(self.lineRender.text(), 0)
            fx = self.check_modify_name_pc(self.lineFx.text(), 1)
            if render is not None and fx is not None and render != -1 and fx != -1:
                render = self.add_prefix(render, "render")
                fx = self.add_prefix(fx, "fx")
                self.host_list = fx + render
                # print(self.host_list)
            else:
                if fx == -1:
                    self.checkFx.setChecked(False)
                if render == -1:
                    self.checkRender.setChecked(False)
                print('Check the supplied values!')
        
        if self.host_list is not None:
            self.startProgressBar(users_list=self.host_list, path_to_save = self.path_to_save)
        else:
            self.infoAboutFxRender()      

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Grabber()
    app.exec_()
    sys.exit()