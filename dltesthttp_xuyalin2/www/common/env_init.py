#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设置环境为自动化测试环境
"""

import time
import os

basedir = os.path.abspath(os.path.dirname(__file__))


import sys
print
sys.path.append(sys.path[0])

def envAutoFlag(serverConfig, serverName):
    import www.common.sshlinux
    # 获取相关服务器信息
    server_ip = serverConfig[serverName+'host']
    server_port = serverConfig['port']
    server_user = serverConfig['user']
    server_passwd = serverConfig[serverName+'pwd']
    remoteFile = serverConfig[serverName+'flagfile']
    flagName = serverConfig[serverName+'testflag']
    restartFlag = serverConfig[serverName+'restart']

    # 切割remoteFile
    tomcat = remoteFile.split('/')[2]
    filename = remoteFile.split('/')[-1].split('.')[0]
    tmpfile = basedir + "/../../tmp/" + filename + ".txt"

    # 1、修改配置文件，设置自动化标志为true
    www.common.sshlinux.linux_to_win(tmpfile, remoteFile, server_ip=server_ip, server_port=server_port, server_user=server_user, server_passwd=server_passwd)
    try:
        lines=open(tmpfile,"r").readlines()
        for i in range(0, len(lines)):
            if flagName in lines[i].decode('utf-8') and 'false' in lines[i].decode('utf-8'):
                lines[i]=lines[i].replace('false','true')
            elif flagName in lines[i].decode('utf-8') and '0' in lines[i].decode('utf-8'):
                lines[i]=lines[i].replace('0','1')
        open(tmpfile,'w').writelines(lines)
    except Exception,e:
        print e
    www.common.sshlinux.win_to_linux(tmpfile, remoteFile, server_ip=server_ip, server_port=server_port, server_user=server_user, server_passwd=server_passwd)

    if restartFlag == 'True':
        # 重启tomcat
        ssh = www.common.sshlinux.ssh_connect(server_ip, server_port, server_user, server_passwd)
        progress = www.common.sshlinux.exec_cmd(ssh, 'ps -ef|grep /data/' + tomcat + '/').split('\n')
        for i in range(0,len(progress)):
            if 'grep' not in progress[i] and progress[i] is not '':
                tomcatID = progress[i].split()[1]
        ssh = www.common.sshlinux.ssh_connect(server_ip, server_port, server_user, server_passwd)
        www.common.sshlinux.exec_cmd(ssh, 'kill -9 ' + tomcatID)
        # ssh = sshlinux.ssh_connect(server_ip, server_port, server_user, server_passwd)
        # print "cd /data/" + tomcat +"/bin/;./startup.sh"
        # sshlinux.exec_cmd(ssh, "source /etc/profile")
        # sshlinux.exec_cmd(ssh, "env")
        # #sshlinux.exec_cmd(ssh, "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/usr/local/jdk1.7.0_79/bin:/usr/local/jdk1.7.0_79/jre/bin:/root/bin:/usr/local/jdk1.7.0_79/bin:/usr/local/jdk1.7.0_79/jre/bin")
        # sshlinux.exec_cmd(ssh, "env")
        www.common.sshlinux.exec_cmd(ssh, "source /etc/profile;cd /data/" + tomcat + "/bin/;sh startup.sh")

        # 等待120s
        # time.sleep(100)
        print "restart is OK"



if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/../..')
    print basedir
    from www.common.config import config
    httpConfig = config().configServer
    envAutoFlag(httpConfig, 'sso')
    envAutoFlag(httpConfig, 'dlmall')
    envAutoFlag(httpConfig, 'dladmin')
    envAutoFlag(httpConfig, 'ws')
