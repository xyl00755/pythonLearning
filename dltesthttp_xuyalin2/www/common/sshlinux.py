#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko

def ssh_connect(server_ip, server_port='14588', server_user='tomcat', server_passwd=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, port=int(server_port),username=server_user, password=server_passwd)
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

def win_to_linux(localpath, remotepath, server_ip, server_port='14588', server_user='tomcat', server_passwd=None):
    '''
    windows向linux服务器上传文件.
    localpath  为本地文件的绝对路径。如：D:\test.py
    remotepath 为服务器端存放上传文件的绝对路径,而不是一个目录。如：/tmp/my_file.txt
    '''
    client = paramiko.Transport((server_ip, int(server_port)))
    client.connect(username = server_user, password = server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.put(localpath,remotepath)
    client.close()

def linux_to_win(localpath, remotepath, server_ip, server_port='14588', server_user='tomcat', server_passwd=None):
    '''
    从linux服务器下载文件到本地
    localpath  为本地文件的绝对路径。如：D:\test.py
    remotepath 为服务器端存放上传文件的绝对路径,而不是一个目录。如：/tmp/my_file.txt
    '''
    client = paramiko.Transport((server_ip, int(server_port)))
    client.connect(username = server_user, password = server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.get(remotepath, localpath)
    client.close()



if __name__ == '__main__':
    ssh = ssh_connect()
    exec_cmd(ssh, 'ls')