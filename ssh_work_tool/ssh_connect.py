import asyncio
import socket
import string
import paramiko

class SshActions():

    def __init__(self, ip, login, passwd, port):
        
        self.ip = ip
        self.login = login
        self.passwd = passwd
        self.port = port

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.printable = set(string.printable)

        self.symbol = ">> "

    def run_command(self, command, ip, hide):
        if hide != True:
            print('{} RUN {} >> {}'.format(self.symbol, command, ip))
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            out = stdout.read().decode()
            return ''.join(list(filter(lambda x: x in self.printable, out)))
        except Exception:
            return None
    
    def run_command_as_root(self, command, ip, hide):
        if hide != True:
            print('{} RUN SUDO {} >> {}'.format(self.symbol, command, ip))
        try:
            session = self.ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command("sudo bash -c \"" + command + "\"")
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(self.passwd + '\n')
            stdin.flush()
            out = stdout.read().decode("utf-8").replace(self.passwd, '')
            return ''.join(list(filter(lambda x: x in self.printable, out)))
        except Exception:
            return None
    
    def ssh_authentication(self):
        try:
            self.ssh.connect(hostname=self.ip, username=self.login, password=self.passwd, port=self.port, timeout=10.0, auth_timeout= 10.0)
            return True
        except Exception:
            pass
        return False

    def ssh_check_connect(self):
        if self.ssh_authentication():
            if self.ssh.get_transport().is_active():
                return True
        else:
            return False
    
    def ssh_close(self):
        self.ssh.close()