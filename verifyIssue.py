#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import urllib2
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import COMMASPACE,formatdate
import json
import re

mail_host='smtp.danlu.com'
mail_user='scm@danlu.com'
mail_pass='A5eeeF341'
sender = 'scm@danlu.com'
receivers = ['ceshi@danlu.com','jiadalu@dhc.com.cn']
#receivers = ['xuyalin@danlu.com']  
token = "s6ds3VWzz6PAsBq_t9U4"


def sendMail(mail_content):
	print "start mail send"
	message = MIMEText(mail_content, 'plain', 'UTF-8')
	message['From'] = Header("%s"%sender)
	message['To'] = COMMASPACE.join(receivers)
	message['Date'] = formatdate(localtime=True) 

	subject = u'[BugRelationsCheck] 未关联的打开状态功能bug'
	#subject = '[AutoMergeReport]bug'
	message['Subject'] = Header(subject, 'UTF-8')

	try:
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)
		smtpObj.login(mail_user, mail_pass)  
		smtpObj.sendmail(sender, receivers, message.as_string())
		smtpObj.close()
		print "mail sent"
	except smtplib.SMTPException, e:
		print e

key='8ca58cf0beb6ff2847f77b15f1d27f6a678f4212'
url_web = "http://182.92.230.201:3000/projects/bug2/issues.json?utf8=%E2%9C%93&set_filter=1&f%5B%5D=status_id&op%5Bstatus_id%5D=o&f%5B%5D=tracker_id&op%5Btracker_id%5D=%3D&v%5Btracker_id%5D%5B%5D=2&f%5B%5D=relates&op%5Brelates%5D=%21*&limit=100&key="+key
url_iOS ="http://182.92.230.201:3000/projects/41/issues.json?utf8=%E2%9C%93&set_filter=1&f%5B%5D=status_id&op%5Bstatus_id%5D=o&f%5B%5D=tracker_id&op%5Btracker_id%5D=%3D&v%5Btracker_id%5D%5B%5D=2&f%5B%5D=relates&op%5Brelates%5D=%21*&limit=100&key="+key
url_Android = "http://182.92.230.201:3000/projects/42/issues.json?utf8=%E2%9C%93&set_filter=1&f%5B%5D=status_id&op%5Bstatus_id%5D=o&f%5B%5D=tracker_id&op%5Btracker_id%5D=%3D&v%5Btracker_id%5D%5B%5D=2&f%5B%5D=relates&op%5Brelates%5D=%21*&limit=100&key="+key
ignoreIssuesList=(4095,4096,3624,2914,2024,2223)
#获取issues id 并打印		
def getIssues(url):
	#发请求
	query_req = urllib2.Request(url)
	query_resp = urllib2.urlopen(query_req)
	info = query_resp.read()
	#print info

	#将获取到的JSON载入字符串，以便后续处理
	info_json = json.loads(info)
	issuesList = info_json["issues"]
	#print issuesList

	#将id+subject取出来放到数组中
	#outputList=[]
	outputList=""
	for cc in issuesList:
		#outputList.append(str(cc["id"])+"  "+cc["subject"])
		if cc["id"] not in ignoreIssuesList:
			outputList+=str(cc["id"])+"  "+cc["subject"]+"\r\n"
		
	#outputList.decode('UTF-8')
	return 	outputList
		
def setReport():
	report_text = u'Hi All,\r\n当前未关联的打开状态功能性bug如下：\r\n====项目：丹露web项目问题管理====\r\n'
	project_name2 = u'\r\n====项目：丹露Android项目问题管理====\r\n'
	project_name3 = u'\r\n====项目：丹露iOS项目问题管理====\r\n'
	#report_text =report_text+getIssues(url_web).encode('gbk')+project_name2+getIssues(url_Android).encode('gbk')+project_name2+getIssues(url_iOS).encode('gbk')
	#report_text =report_text+getIssues(url_web).encode('utf-8')+project_name2+getIssues(url_Android).encode('utf-8')+project_name2+getIssues(url_iOS).encode('utf-8')
	
	totalIssues = getIssues(url_web)+getIssues(url_Android)+getIssues(url_iOS)
	if totalIssues.strip() != '':
		report_text = report_text+getIssues(url_web)+project_name2+getIssues(url_Android)+project_name2+getIssues(url_iOS)
	else:
		report_text = ''
	return report_text

#print getIssues(url_web)
#print setReport()

if setReport().strip() != '':
	sendMail(setReport())
else:
	print "今日没有未关联的打开状态功能性bug，不发送邮件。"