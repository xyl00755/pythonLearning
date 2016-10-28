#!/usr/bin/env python
# -*- coding: utf-8 -*-


import configparser
import paramiko


#machine details
ini_file='../../config/server_config.ini'
config = configparser.ConfigParser()
config.read(ini_file)

server_ip=config['webservice']['host']
server_user=config['webservice']['user']
server_passwd=config['webservice']['password']
server_port=int(config['webservice']['port'])


def ssh_connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, port=server_port,username=server_user, password=server_passwd)
    return ssh

def ssh_disconnect(client):
    client.close()

def exec_cmd(ssh, command):
    '''
    windows客户端远程执行linux服务器上命令
    '''
    stdin, stdout, stderr = ssh.exec_command(command)
    err = stderr.read()
    out = stdout.read()

    if "" != err:
        print "command: " + command + " exec failed!\nERROR :" + err
        return err
    else:
        print "command: " + command + " exec success."
        print out
        return out

def win_to_linux(localpath, remotepath):
    '''
    windows向linux服务器上传文件.
    localpath  为本地文件的绝对路径。如：D:\test.py
    remotepath 为服务器端存放上传文件的绝对路径,而不是一个目录。如：/tmp/my_file.txt
    '''
    client = paramiko.Transport((server_ip, server_port))
    client.connect(username = server_user, password = server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.put(localpath,remotepath)
    client.close()

def linux_to_win(localpath, remotepath):
    '''
    从linux服务器下载文件到本地
    localpath  为本地文件的绝对路径。如：D:\test.py
    remotepath 为服务器端存放上传文件的绝对路径,而不是一个目录。如：/tmp/my_file.txt
    '''
    client = paramiko.Transport((server_ip, server_port))
    client.connect(username = server_user, password = server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.get(remotepath, localpath)
    client.close()

# def connect(hostname=config['webservice']['host'],username=config['webservice']['user'],password=config['webservice']['password'],port=config['webservice']['port']):
#     import sys
#     if 'linux' in sys.platform:
#         from pexpect import pxssh
#         try:
#             s = pxssh.pxssh()
#             s.login(hostname,username,password,port)
#             s.readline('ls')
#             print s
#             return s
#         except Exception,e:
#             print "[-] Error Connectiong:" + str(e)
#     else:
#         from winpexpect import winspawn
#         ssh = winspawn('telnet',[username + '@' + hostname + ' -p ' + port])
#         ssh.logfile = sys.stdout
#         i = ssh.expect(['Password:'], timeout = 5)
#         print i
#         ssh.readline(password)
#         print ssh.readline('ls')

if __name__ == '__main__':
    ssh = ssh_connect()
    exec_cmd(ssh, 'ls')