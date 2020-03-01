import os
import sys

from PyQt5 import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPlainTextEdit, QPushButton, QVBoxLayout, QWidget)

from ssh_connect import SshActions as ssh


class Helper(QWidget):

    def __init__(self):
        super(Helper, self).__init__()
        self.ssh = None
        self.current_directory = ''
        self.initUI()
        self.show()

    def initUI(self):

        # Start settings
        self.setWindowTitle('Koban helper | ssh & nc & misc')
        self.setFixedHeight(600)
        self.setMinimumWidth(800)
        self.setMaximumWidth(1200)

        # Layout
        mainLayout = QHBoxLayout()
        connectLayout = QVBoxLayout()

        # Add widget's on layouts
        connectLayout.addWidget(self.connect_widgets_ui())
        connectLayout.addWidget(self.settings_run_widgets_ui())
        mainLayout.addLayout(connectLayout)
        mainLayout.addWidget(self.output_widgets_ui())
        self.setLayout(mainLayout)

        # Init connect widgets with func
        self.connect_actions()

    # SSH "Connect" widget's
    def connect_widgets_ui(self):

        group_box = Qt.QGroupBox("")

        layout = QGridLayout()
        layout.setAlignment(Qt.Qt.AlignTop)

        self.lbl_user = QLabel('Change user (in progress..)')
        self.cmb_user = QComboBox()

        self.ln_ip = QLineEdit('')
        self.ln_login = QLineEdit('')
        self.ln_pass = QLineEdit('')
        self.ln_pass.setEchoMode(QLineEdit.Password)

        self.ln_ip.setFixedWidth(220)
        self.ln_login.setFixedWidth(220)
        self.ln_pass.setFixedWidth(220)
        self.ln_ip.setFixedHeight(20)
        self.ln_login.setFixedHeight(20)
        self.ln_pass.setFixedHeight(20)

        self.lbl_ip = QLabel('IP:')
        self.lbl_login = QLabel('LOGIN:')
        self.lbl_pass = QLabel('PASSWORD:')
        self.chx_port = QCheckBox('PORT DEFAULT')
        self.ln_port = QLineEdit('22')
        self.ln_port.setFixedWidth(220)
        self.ln_port.setFixedHeight(20)

        self.lbl_ip.setFixedWidth(150)
        self.lbl_login.setFixedWidth(150)
        self.lbl_pass.setFixedWidth(150)
        self.chx_port.setChecked(True)
        self.ln_port.setDisabled(True)

        self.txt_command = QPlainTextEdit('')
        self.txt_command.setPlaceholderText('Input your command here..')
        self.txt_command.setFixedHeight(60)

        self.btn_connect = QPushButton('Connect')
        self.btn_run = QPushButton('Run command')

        self.btn_run.setDisabled(True)
        self.txt_command.setDisabled(True)

        # ВРЕМЕННО
        self.set_dafault_value()

        self.fill_kmb_users()

        layout.addWidget(self.lbl_user, 0, 0)
        layout.addWidget(self.cmb_user, 0, 1)
        layout.addWidget(self.lbl_ip, 1, 0)
        layout.addWidget(self.ln_ip, 1, 1)
        layout.addWidget(self.lbl_login, 2, 0)
        layout.addWidget(self.ln_login, 2, 1)
        layout.addWidget(self.lbl_pass, 3, 0)
        layout.addWidget(self.ln_pass, 3, 1)
        layout.addWidget(self.chx_port, 4, 0)
        layout.addWidget(self.ln_port, 4, 1)
        layout.addWidget(self.btn_connect, 5, 0, 1, 2)
        layout.addWidget(self.txt_command, 6, 0, 1, 2)
        layout.addWidget(self.btn_run, 7, 0, 1, 2)

        group_box.setLayout(layout)

        return group_box

    # SSH "Setting for run command" widget's
    def settings_run_widgets_ui(self):

        group_box = Qt.QGroupBox("")

        layout = QHBoxLayout()
        layout.setAlignment(Qt.Qt.AlignTop)

        self.chx_asroot = QCheckBox('AS ROOT(x)')
        self.chx_reset_always_command = QCheckBox('CLEAR COMMAND')
        self.chx_reset_always_out = QCheckBox('CLEAR OUT')

        self.chx_reset_always_out.setChecked(True)
        self.chx_reset_always_command.setChecked(False)

        self.chx_reset_always_out.setDisabled(True)
        self.chx_reset_always_command.setDisabled(True)
        self.chx_asroot.setDisabled(True)

        layout.addWidget(self.chx_asroot)
        layout.addWidget(self.chx_reset_always_command)
        layout.addWidget(self.chx_reset_always_out)

        group_box.setLayout(layout)

        return group_box

    # SSH "Output" widget's
    def output_widgets_ui(self):

        group_box = Qt.QGroupBox("")
        layout = QVBoxLayout()

        start_text_status = "<b>Status: <font color = 'red'>OFF</font><b>"
        self.lbl_out_status = QLabel(start_text_status)
        self.edit_out = QPlainTextEdit('Need connect!')

        layout.addWidget(self.lbl_out_status)
        layout.addWidget(self.edit_out)

        group_box.setLayout(layout)

        return group_box

    # SSH Connect's
    def connect_actions(self):
        self.btn_connect.clicked.connect(self.connect_ssh)
        self.btn_run.clicked.connect(self.send_command)
        self.chx_port.stateChanged.connect(self.change_ln_port_disabled)

    # From this place only functional!

    # ВРЕМЕННО
    def set_dafault_value(self):
        self.ln_ip.setText("a.b.c.ad.d")
        self.ln_login.setText('ad.d.ada')
        self.ln_pass.setText('a.d.a.da')
        self.ln_port.setText('22')

    def fill_kmb_users(self):
        self.cmb_user.addItems(['Jayse'])

    def get_connect_data_from_lns(self):
        data = {
            'ip': self.ln_ip.text(),
            'login': self.ln_login.text(),
            'pass': self.ln_pass.text(),
            'port': self.ln_port.text()
        }
        return data

    def change_ln_port_disabled(self):
        if self.chx_port.isChecked():
            self.ln_port.setDisabled(True)
        else:
            self.ln_port.setDisabled(False)
    
    def color_html_text(self, text, color):
        return "<b><font color = '{}'>{}</font><b>".format(color, text)

    def change_info_gui_connect(self):
        if "OFF" in self.lbl_out_status.text():
            info = self.get_connect_data_from_lns()
            self.lbl_out_status.setText(
                "<b>{}: <font color = 'green'>{}</font> ~ <font color = 'green'>{}@{}</font><b>".format('Status', "ON", info['login'], info['ip']))
            self.btn_connect.setText('Disconnect')
            self.btn_run.setDisabled(False)
            self.txt_command.setDisabled(False)
            self.chx_reset_always_out.setDisabled(False)
            self.chx_reset_always_command.setDisabled(False)
            self.chx_asroot.setDisabled(False)

            self.ln_ip.setDisabled(True)
            self.ln_login.setDisabled(True)
            self.ln_port.setDisabled(True)
            self.ln_pass.setDisabled(True)
            self.chx_port.setDisabled(True)

            self.edit_out.setPlainText('')
        else:
            self.lbl_out_status.setText(
                "<b>{}: <font color = 'red'>{}</font><b>".format('Status', "OFF"))
            self.btn_connect.setText('Connect')
            self.btn_run.setDisabled(True)
            self.txt_command.setDisabled(True)
            self.chx_reset_always_out.setDisabled(True)
            self.chx_reset_always_command.setDisabled(True)
            self.chx_asroot.setDisabled(True)

            self.ln_ip.setDisabled(False)
            self.ln_login.setDisabled(False)
            self.ln_port.setDisabled(False)
            self.ln_pass.setDisabled(False)
            self.chx_port.setDisabled(False)
            self.edit_out.clear()

            self.edit_out.setPlainText('Need connect!')

    def connect_ssh(self):
        if self.btn_connect.text() == 'Connect':
            data = self.get_connect_data_from_lns()
            self.ssh = ssh(data['ip'], data['login'],
                           data['pass'], data['port'])
            if self.ssh.ssh_authentication():
                self.change_info_gui_connect()
        elif self.btn_connect.text() == 'Disconnect':
            self.ssh = None
            self.change_info_gui_connect()

    def change_info_gui_run(self, out, pwd):

        if self.chx_reset_always_out.isChecked():
                self.edit_out.clear()
        if self.chx_reset_always_command.isChecked():
            self.txt_command.setPlainText('')
        if out is not "":
            self.edit_out.appendHtml(self.color_html_text(pwd, 'black'))
            self.edit_out.appendPlainText(out)
        else:
            self.edit_out.appendHtml(self.color_html_text('Some problem with command..', 'red'))

    def send_command(self):
        command = self.txt_command.toPlainText()
        pwd = self.ssh.run_command('pwd', self.get_connect_data_from_lns()['ip'], True)
        if command is not "":
            out = self.ssh.run_command(command, self.get_connect_data_from_lns()['ip'], False)
            self.change_info_gui_run(out, pwd)
        else:
            self.edit_out.appendHtml(self.color_html_text('Input command!', 'blue'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Helper()
    app.exec_()
    sys.exit()