#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

if os.path.expandvars("$ALG_PY3_LIBS") not in sys.path:
    sys.path.append(os.path.expandvars("$ALG_PY3_LIBS"))

from PyQt5 import Qt


class TemplateEditor(Qt.QWidget):
    def __init__(self, init_line):
        super(TemplateEditor, self).__init__()
        self.init_line = init_line
        self.initUI()
        self.show()

    def initUI(self):

        #Start settings
        self.setMinimumHeight(150)
        self.setMinimumWidth(500)
        mainLayout = Qt.QVBoxLayout()
        forButtonLayout = Qt.QGridLayout()
        self.setLayout(mainLayout)

        #Add button
        self.buttonAddKMB = Qt.QPushButton('$KMB', self)
        self.buttonAddkmb = Qt.QPushButton('$kmb', self)
        self.buttonAddVersion = Qt.QPushButton('$VERSION', self)
        self.buttonAddProj = Qt.QPushButton('$PROJ', self)
        self.buttonAddproj = Qt.QPushButton('$proj', self)
        self.buttonAddColorspace = Qt.QPushButton('$COLORSPACE', self)

        forButtonLayout.addWidget(self.buttonAddKMB, 0, 0)
        forButtonLayout.addWidget(self.buttonAddVersion, 0, 1)
        forButtonLayout.addWidget(self.buttonAddProj, 0, 2)
        forButtonLayout.addWidget(self.buttonAddColorspace, 0, 3)
        forButtonLayout.addWidget(self.buttonAddkmb, 1, 0)
        forButtonLayout.addWidget(self.buttonAddproj, 1, 2)


        #Set obj name
        self.buttonAddKMB.setObjectName('$KMB')
        self.buttonAddkmb.setObjectName('$kmb')
        self.buttonAddVersion.setObjectName('$VERSION')
        self.buttonAddProj.setObjectName('$PROJ')
        self.buttonAddproj.setObjectName('$proj')
        self.buttonAddColorspace.setObjectName('$COLORSPACE')

        #Add lineEdit
        self.lineEdit = Qt.QLineEdit(self)
        self.lineEdit.setText(self.init_line)
        self.lineEdit.setFixedWidth(475)
        mainLayout.addWidget(self.lineEdit)

        #Connect
        self.buttonAddKMB.clicked.connect(self.insert)
        self.buttonAddkmb.clicked.connect(self.insert)
        self.buttonAddVersion.clicked.connect(self.insert)
        self.buttonAddProj.clicked.connect(self.insert)
        self.buttonAddproj.clicked.connect(self.insert)
        self.buttonAddColorspace.clicked.connect(self.insert)

        #Merge layout
        mainLayout.addLayout(forButtonLayout)


    #Function for insert text on pos cursor
    def insert(self):
        
        sender = self.sender()
        posCursor = self.lineEdit.cursorPosition()
        ins = self.insertOnPost(self.lineEdit.text(), str(sender.objectName()), posCursor)
        self.lineEdit.setText(ins)


    def insertOnPost(self, string, add ,pos):
        return string[:pos] + add + string[pos:]


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = TemplateEditor()
    app.exec_()
    sys.exit()


    # $kmb_comp_v$VERSION_aces/$kmb_comp_v$VERSION_aces.%04d.exr
    # 1. kmb \ KMB - name of the shot ex: 04_CLN-0040 (str)
    # 2. VERSION - version number (int)
    # 3. proj / PROJ - name of the project (str)
    # 4. COLORSPACE - name of the color space (str) ex: acescg
