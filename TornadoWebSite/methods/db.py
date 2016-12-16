#!/usr/bin/env python
# -*- coding:utf-8 -*-

import mysql.connector

# conn=mysql.connector.connect(user="root", password="123456", database="testxx", host="180.76.174.29", port=3307,charset="utf8")
conn=mysql.connector.connect(user="root", database="testxx", host="180.76.174.29", port=3307,charset="utf8") #由于此数据库不需要密码，所以无需密码参数
cur=conn.cursor()

def select_table(table,column,condition,value):
    sql="select"+column+" from "+table+" where "+condition+"='"+value+"'"
    cur.execute(sql)
    lines=cur.fetchall()
    return lines

if __name__ == '__main__':
    # print cur.execute("SELECT * FROM Userinfo")
    print select_table("Userinfo",'*','username','xyl')
