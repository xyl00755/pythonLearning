#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设置环境为自动化测试环境
"""
import sshlinux
import time

def run():
    # 1、修改配置文件，设置自动化标志为true
    sshlinux.linux_to_win("d:\\vars.text","/data/tomcat/webapps/ROOT/WEB-INF/classes/vars.properties")
    try:
        lines=open("d:\\vars.text","r").readlines()
        flen=len(lines)
        for i in range(flen):
            if 'isTestInterfaceModel' in lines[i]:
                lines[i]=lines[i].replace('false','true')
        open("d:\\vars.text",'w').writelines(lines)
    except Exception,e:
        print e
    sshlinux.win_to_linux("d:\\vars.text","/data/tomcat/webapps/ROOT/WEB-INF/classes/vars.properties")

    # 重启tomcat
    ssh = sshlinux.ssh_connect()
    progress = sshlinux.exec_cmd(ssh, 'ps -ef|grep /data/tomcat/').split('\n')
    for i in range(0,len(progress)):
        if 'grep' not in progress[i] and progress[i] is not '':
            tomcatID = progress[i].split()[1]
    ssh = sshlinux.ssh_connect()
    sshlinux.exec_cmd(ssh, 'kill -9 ' + tomcatID)
    ssh = sshlinux.ssh_connect()
    sshlinux.exec_cmd(ssh, "cd /data/tomcat/bin/;./startup.sh")
    # 等待120s
    time.sleep(100)
    print "restart is OK"


if __name__ == '__main__':
    run()