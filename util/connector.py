import os
import sys
import paramiko

SSH_KEY = '~/.ssh/id_rsa.pub'

nodes = {'vmware': ['hopper2', 'hopper4', 'hopper5'],
         'qemu': ['hopper6', 'hopper7'],
         'qemu_patched': ['hopper1'],
         'virtualbox': ['hopper3', 'hopper8']}


class SSH(object):
    def __init__(self, host, user=None, port=22, passwd=None):
        self.host = host
        if not user:
            self.user = os.getenv("USER")
        self.passwd = passwd

    def ssh_connect(self, key=False):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key:
            self.key_path = os.path.expanduser(SSH_KEY)
            self.ssh.connect(self.host, username=self.user, password=self.passwd,
                        key_filename=self.key_path)
        else:
            self.ssh.connect(self.host, username=self.user, password=self.passwd)
            print("connected to %s"%self.host)

    def ssh_command(self, cmd):
        (_, stdout, stderr) = self.ssh.exec_command(cmd)
	status = stdout.channel.recv_exit_status()
        lines = stdout.readlines()
	import ipdb; ipdb.set_trace()
        if lines:
            print(lines)

    def ssh_close(self):
        self.ssh.close()


if __name__ == '__main__':
    for i in range(1, 9):
        hostname = 'hopper' + str(i)
        ssh = SSH(hostname)
        ssh.ssh_connect()
        ssh.ssh_command('export HOME=/localhome/$USER')
        ssh.ssh_command('source ~/.virtualenvs/cuckoo-venv/bin/activate')
        ssh.ssh_command('python /opt/share/archive/test_pafish.py')
        ssh.ssh_close()
    #if len(sys.argv) > 1:
    #    backend = sys.argv[1]
    #for node in nodes[backend]:
    #    ssh = SSH(node)
    #    ssh.ssh_connect()
    #    ssh.ssh_command('export HOME=/localhome/$USER')
    #    ssh.ssh_command('source ~/.virtualenvs/cuckoo-venv/bin/activate')
    #    ssh.ssh_command('python /opt/share/archive/archive.py %s'%backend)
    #    ssh.ssh_close()
