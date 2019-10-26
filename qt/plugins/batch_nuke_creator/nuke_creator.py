#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

if os.path.expandvars("$ALG_PY3_LIBS") not in sys.path:
    sys.path.append(os.path.expandvars("$ALG_PY3_LIBS"))

import time
from functools import partial
from itertools import product

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QTableWidget, QApplication, QTableWidgetItem, \
    QAbstractItemView, QCheckBox, QVBoxLayout, QHBoxLayout

class NukeTemplateCreator(QWidget):

    def __init__(self, kmb_list, proj): 
        super(NukeTemplateCreator, self).__init__()
        self.kmb_list = kmb_list
        self.proj = proj
        self.kmb_list_size = len(self.kmb_list)
        self.select_row = []
        self.initUI()
        self.show()
        self.info = dict()

    def initUI(self):
        
        #Start settings
        self.setWindowTitle('SELECT MORE')
        self.setMinimumHeight(500)
        self.setMinimumWidth(670)
        self.setMaximumWidth(670)
        self.setMaximumHeight(500)
        mainLayout = QVBoxLayout()
        funcLayout_low = QHBoxLayout()
        funcLayout_high = QHBoxLayout()
        infoLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        #For gui
        self.type_do_names = {
            "1" : ['Select Comp', 'unSelect Comp'],
            "2" : ['Select Precomp', 'unSelect Precomp'],
            "3" : ['Select Matte', 'unSelect Matte'],
            "4" : ['Select Cleanup', 'unSelect Cleanup'],
            "5" : ['Select Roto', 'unSelect Roto'],
            "0" : ['Select All', 'unSelect All']
        }

        #Add table
        self.table = QTableWidget(self)

        #Add info label
        self.label_info_proj = QLabel("PROJ: " + self.proj)
        self.label_info_proj.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info_size = QLabel("COUNT KMB: " + str(self.kmb_list_size))
        self.label_info_size.setAlignment(QtCore.Qt.AlignCenter)

        #Add button

        #For no select func
        self.button_start = QPushButton('Start')
        self.button_select_all = QPushButton(self.type_do_names['0'][0])
        self.button_select_comp = QPushButton(self.type_do_names['1'][0])
        self.button_select_precomp = QPushButton(self.type_do_names['2'][0])
        self.button_select_matte = QPushButton(self.type_do_names['3'][0])
        self.button_select_cleanup = QPushButton(self.type_do_names['4'][0])
        self.button_select_roto = QPushButton(self.type_do_names['5'][0])

        #Settings table
        self.table.setColumnCount(6)
        self.table.setRowCount(len(self.kmb_list))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.headers = ["Name", "Comp", "Precomp", "Matte", "Cleanup", "Roto"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 125)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)

        for i in range(len(self.kmb_list)):

            #Add checkbox
            checkbox_comp = QCheckBox()
            checkbox_precomp = QCheckBox()
            checkbox_matte = QCheckBox()
            checkbox_cleanup = QCheckBox()
            checkbox_roto = QCheckBox()

            #Settings checkbox
            checkbox_comp.stateChanged.connect(self.on_changed)
            checkbox_precomp.stateChanged.connect(self.on_changed)
            checkbox_matte.stateChanged.connect(self.on_changed)
            checkbox_cleanup.stateChanged.connect(self.on_changed)
            checkbox_roto.stateChanged.connect(self.on_changed)

            checkbox_comp.setStyleSheet("padding-left: 45%")
            checkbox_precomp.setStyleSheet("padding-left: 45%")
            checkbox_matte.setStyleSheet("padding-left: 45%")
            checkbox_cleanup.setStyleSheet("padding-left: 45%")
            checkbox_roto.setStyleSheet("padding-left: 45%")

            #Add cell name
            cell_kmb = QTableWidgetItem(self.kmb_list[i])
            
            #Add on table checkbox's
            self.table.setCellWidget(i, 1, checkbox_comp)
            self.table.setCellWidget(i, 2, checkbox_precomp)
            self.table.setCellWidget(i, 3, checkbox_matte)
            self.table.setCellWidget(i, 4, checkbox_cleanup)
            self.table.setCellWidget(i, 5, checkbox_roto)

            #Add cell name
            self.table.setItem(i,0, cell_kmb)

        #Add on func layout
        funcLayout_low.addWidget(self.button_select_all)
        funcLayout_low.addWidget(self.button_select_comp)
        funcLayout_low.addWidget(self.button_select_precomp)
        funcLayout_low.addWidget(self.button_select_matte)
        funcLayout_low.addWidget(self.button_select_cleanup)
        funcLayout_low.addWidget(self.button_select_roto)
        infoLayout.addWidget(self.label_info_proj)
        infoLayout.addWidget(self.label_info_size)
        #Add on main layout
        mainLayout.addLayout(infoLayout)
        mainLayout.addWidget(self.table)
        mainLayout.addLayout(funcLayout_high)
        mainLayout.addLayout(funcLayout_low)
        mainLayout.addWidget(self.button_start)

        #Connect
        self.table.itemSelectionChanged.connect(self.on_itemSelectionChanged)
        self.button_start.clicked.connect(self.send_info)
        self.button_select_all.clicked.connect(partial(self.select_action, "0"))
        self.button_select_comp.clicked.connect(partial(self.select_action, "1"))
        self.button_select_precomp.clicked.connect(partial(self.select_action, "2"))
        self.button_select_matte.clicked.connect(partial(self.select_action, "3"))
        self.button_select_cleanup.clicked.connect(partial(self.select_action, "4"))
        self.button_select_roto.clicked.connect(partial(self.select_action, "5"))

    @QtCore.pyqtSlot()
    def on_itemSelectionChanged(self):
        all_sel_items = self.table.selectedItems()
        select_row = []
        items = []
        for x in range(len(self.kmb_list)):
            items.append(self.table.item(x, 0))
        for item in items:
            if item.column() == 0:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsSelectable)

        for i in all_sel_items:
            select_row.append(i.row())

        self.select_row = select_row

    def action_for_select_row_column(self, type_do, row_list, ctrl, name_sender):

        if ctrl is False:
            for i in range(len(self.kmb_list)):
                checkbox = self.table.cellWidget(i, int(type_do))
                if "un" in name_sender:
                    checkbox.setChecked(False)
                else:
                    checkbox.setChecked(True)
                index = self.table.indexAt(checkbox.pos())
                try:
                    self.creating_responce(index.column(), index.row(), checkbox)
                except Exception:
                    pass
        else:
            for i in row_list:
                checkbox = self.table.cellWidget(i, int(type_do))
                if "un" in name_sender:
                    checkbox.setChecked(False)
                else:
                    checkbox.setChecked(True)
                index = self.table.indexAt(checkbox.pos())
                try:
                    self.creating_responce(index.column(), index.row(), checkbox)
                except Exception:
                    pass
    
    def action_for_select(self, row_list, ctrl, name_sender):

        if ctrl is False:
            for i in range(1, len(self.headers)):
                for j in range(len(self.kmb_list)):
                    checkbox = self.table.cellWidget(j, i)
                    if "un" in name_sender:
                        checkbox.setChecked(False)
                    else:
                        checkbox.setChecked(True)
                    index = self.table.indexAt(checkbox.pos())
                    try:
                        self.creating_responce(index.column(), index.row(), checkbox)
                    except Exception:
                        pass
        else:
            for i in range(1, len(self.headers)):
                for j in row_list:
                    checkbox = self.table.cellWidget(j, i)
                    if "un" in name_sender:
                        checkbox.setChecked(False)
                    else:
                        checkbox.setChecked(True)
                    index = self.table.indexAt(checkbox.pos())
                    try:
                        self.creating_responce(index.column(), index.row(), checkbox)
                    except Exception:
                        pass
    
    def check_for_all(self):

        cnt = 0
        for i in range(1, len(self.headers)):
            for j in range(len(self.kmb_list)):
                checkbox = self.table.cellWidget(j, i)
                if checkbox.isChecked():
                    cnt += 1
        if cnt > 0:
            self.set_name_on_buttons('0', False)
        else:
            self.set_name_on_buttons('0', True)

    def check_select_row_column(self, sr):
        counter = 0
        if len(sr) != 0:
            sr = sorted(sr)
            for i in range(len(sr)-1):
                if int(sr[i]) + 1 == int(sr[i+1]):
                    counter +=1
            if counter == len(sr):
                return 1
            else:
                return -1
        else:
            return -2

    def select_action(self, type_do):

        ctrl = False
        name_sender = self.sender().text()

        select_row = list(set(self.select_row))
        if self.check_select_row_column(select_row) == 1:
            select_row = [select_row[0], select_row[len(select_row) - 1]]
        elif self.check_select_row_column(select_row) == -1:
            select_row = select_row
            ctrl = True
        elif self.check_select_row_column(select_row) == -2:
            select_row = self.kmb_list
        
        # print(type_do, select_row, ctrl)

        if type_do != "0":
            self.action_for_select_row_column(type_do, select_row, ctrl, name_sender)
        else:
            self.action_for_select(select_row, ctrl, name_sender)

    def set_name_on_buttons(self, type_do, action = None):

        if type_do == '1':
            if action == True:
                self.button_select_comp.setText(self.type_do_names[type_do][0])
            else:
                self.button_select_comp.setText(self.type_do_names[type_do][1])
        elif type_do == '2':
            if action == True:
                self.button_select_precomp.setText(self.type_do_names[type_do][0])
            else:
                self.button_select_precomp.setText(self.type_do_names[type_do][1])
        elif type_do == '3':
            if action == True:
                self.button_select_matte.setText(self.type_do_names[type_do][0])
            else:
                self.button_select_matte.setText(self.type_do_names[type_do][1])
        elif type_do == '4':
            if action == True:
                self.button_select_cleanup.setText(self.type_do_names[type_do][0])
            else:
                self.button_select_cleanup.setText(self.type_do_names[type_do][1])
        elif type_do == '5':
            if action == True:
                self.button_select_roto.setText(self.type_do_names[type_do][0])
            else:
                self.button_select_roto.setText(self.type_do_names[type_do][1])
        elif type_do == '0':
            if action == True:
                self.button_select_all.setText(self.type_do_names["0"][0])
            else:
                self.button_select_all.setText(self.type_do_names["0"][1])

    def check_checkbox_on_column(self, col):
        cnt = 0
        for i in range(len(self.kmb_list)):
            checkbox = self.table.cellWidget(i, int(col))
            if checkbox.isChecked():
                cnt +=1
        if cnt > 0:
            self.set_name_on_buttons(str(col), action = False)
        else:
            self.set_name_on_buttons(str(col), action = True)

    def on_changed(self):
        checkbox = self.sender()
        index = self.table.indexAt(checkbox.pos())
        self.check_checkbox_on_column(index.column())
        self.check_for_all()
        self.creating_responce(index.column(), index.row(), checkbox)

    def creating_responce(self, index_col, index_row, checkbox):
        
        name = self.table.item(index_row, 0).text()
        if name not in self.info.keys():
            self.info[name] = {}
        if checkbox.isChecked():
            if index_col == 1:
                self.info[name].update({"comp" : True})
            if index_col == 2:
                self.info[name].update({"precomp" : True})
            if index_col == 3:
                self.info[name].update({"matte" : True})
            if index_col == 4:
                self.info[name].update({"cleanup" : True})
            if index_col == 5:
                self.info[name].update({"roto" : True})
        else:

            if index_col == 1:
                self.info[name].pop("comp")
            elif index_col == 2:
                self.info[name].pop("precomp")
            elif index_col == 3:
                self.info[name].pop("matte")
            elif index_col == 4:
                self.info[name].pop("cleanup")
            elif index_col == 5:
                self.info[name].pop("roto")
    
    def correct_info(self):
        corrected = {k: v for k, v in self.info.items() if v}
        if len(corrected) == 0:
            return False
        else:
            return corrected
    
    def print_info(self, a):
        print("\n" + ("-" * 4) + " SELECTED " + ("-" * 4))
        if a is not False:
            for k,v in a.items():
                print(k, v)
            print("Size:", len(a.items()))
        else:
            print(a)
        print("-" * 18)

    def exec_nuke_with_params(self, proj, kmb, activity_type):
        if proj and kmb:
            cmd = " ".join(("$ALG_NUKE_EXEC -i -t",
                "/studio/tools/code/release/project_editor/create_nk_zero_version.py", 
                str(proj), str(kmb), str(activity_type)))
            print('')
            print('\nPROJ:' + str(proj))
            print('\nKMB:' + str(kmb))
            print('\nACTIV:' + str(activity_type))
            print('')
            say(cmd, 5)
            errormsg = ""
            try:
                say(cmd, 5)
                res = os.system(cmd)
                print("RES: %s" % res)
            except Exception as e:
                print("Error: %s" % e)

    def print_hello(self, name:
        print('hello {}'.format(name))

    def exec_task(self):
        cpus = os.cpu_count() - 2 if os.cpu_count() > 4 else 1
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpus) as executor:
            for num, val in enumerate(executor.map(print_hello, "vlad", chunksize=15)):
                print(num, val)
                
    def send_info(self):
        ready_info = self.correct_info()
        self.print_info(ready_info)


if __name__ == '__main__':
    # kmb_list, proj = sys.argv[1].split(":")
    app = QApplication(sys.argv)
    # window = NukeTemplateCreator(kmb_list.split(","), proj)
    window = NukeTemplateCreator(list("privetpoka"), "Kykareky")
    app.exec_()
    sys.exit()