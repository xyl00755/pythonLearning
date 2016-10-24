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

web_project_map = {"dladmin":"81",
"dlcategroy":"63",
"dlcms":"122",
"dlcompany":"83",
"dlcoupay":"126",
"dlcoupon":"124",
"dldata":"88",
"dlfrontend":"71",
"dlhelp":"68",
"dllycos":"95",
"dlmall":"80",
"dlmerchandise":"65",
"dlnews":"85",
"dloauth2":"109",
"dlopx":"120",
"dlorder":"36",
"dlpay":"27",
"dlpromotion":"67",
"dlpromotionx":"125",
"dlpublic":"73",
"dlsaleright":"64",
"dlscheduler":"52",
"dlsms":"54",
"dluser":"84",
"dlworkflow":"82",
"cas-server3-5-2":"37",
"node-admin-java":"96",
"node-web-admin":"94",
"privilege":"39",
"dlcache":"86",
"dlcodis":"128",
"dlmetaq":"127",
"dlrcmd":"130"}

api_url = "http://idanlu.com:8000/api/v3/projects/"

mail_host='smtp.danlu.com'
mail_user='scm@danlu.com'
mail_pass='A5eeeF341'
sender = 'scm@danlu.com'
#receivers = ['xuyike@danlu.com','liuyisha@danlu.com','chenjiachuan@danlu.com','liyunfei@dhc.com.cn','yaowu.zhang@dhc.com.cn']
receivers = ['xuyalin@danlu.com']  
token = "s6ds3VWzz6PAsBq_t9U4"


def sendMail(mail_content):
	print "start mail send"
	message = MIMEText(mail_content, 'plain', 'UTF-8')
	message['From'] = Header("%s"%sender)
	message['To'] = COMMASPACE.join(receivers)
	message['Date'] = formatdate(localtime=True) 

	subject = '[AutoMergeReport] 持续集成-代码自动合并报告'
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

def loadConfig():
	projectObjList = []
	for cc in web_project_map:
		projectObj = {}
		projectObj["projectName"] = cc
		project_id = web_project_map[cc]
		url = api_url+project_id+"/repository/branches?private_token="+token
		query_req = urllib2.Request(url)
		query_resp = urllib2.urlopen(query_req)
		info = json.loads(query_resp.read())
		
		branchList = []
		for ccc in info:
			br = ccc['name']
			match
			if br=="bug_fix" or br=="develop" or br=="master" or br=="uat_feature" or br=="origin/develop":
				pass
			else:
				branchList.append(br)
		projectObj["branchs"] = branchList
		projectObjList.append(projectObj)
	return projectObjList

def create_MR(api_url,project_id,targetBR):
	url = api_url+project_id+"/merge_requests?private_token="+token
	da="source_branch=develop&target_branch="+targetBR+"&title=\"Auto merge\""

	query_req = urllib2.Request(url,data=da)
	query_resp = urllib2.urlopen(query_req)
	info = query_resp.read()
	print info
	jsonInfo = json.loads(info)
	#mergeId = str(jsonInfo["id"])
	mergeState = jsonInfo["state"]
	return str(jsonInfo["id"])
	
def Accpet_MR(api_url,project_id,mergeId,project,targetBR):
	if mergeId == "":
		return "not need merge"
	
	url = api_url+project_id+"/merge_request/"+mergeId+"/merge?private_token="+token
	da=""
	print "start merge"
	query_req = urllib2.Request(url,data=da)
	query_req.get_method = lambda: 'PUT'
	query_resp = urllib2.urlopen(query_req)
	print query_resp.read()
	return "Auto Merge:[succ] Project["+project+"] Branch["+targetBR+"] merge success.\r\n"
	
#def Close_MR(api_url,project_id,mergeId):
#	if mergeId == "":
#		return "not need merge"
#	
#	url = api_url+project_id+"/merge_request/"+mergeId+"/merge?private_token="+token
#	da=""
#	print "start merge"
#	query_req = urllib2.Request(url,data=da)
#	query_req.get_method = lambda: 'PUT'
#	query_resp = urllib2.urlopen(query_req)
#	print query_resp.read()
#	return "Auto Merge:[succ] Project["+project+"] Branch["+targetBR+"] merge success.\r\n"
	
def mergeBranch(project, branchs):
	#print branchs
	project_id = web_project_map[project]
	return_text = \
	"==================================================================\r\n"+\
	"AutoMerge project [ "+project+" ] id [ " +project_id+ " ].\r\n"+\
	"==================================================================\r\n"
	print return_text
	if len(branchs) == 0:
		print "doesn't have any active branch.\r\n"
		return_text = return_text + "doesn't have any active branch.\r\n"
		return return_text
	
	report_succ_text = ""
	report_fail_text = ""
	
	for br in branchs:
		mergeId = ""
		try:
			mergeId = create_MR( api_url,project_id,br)
		except IOError, e:
			if str(e) == "HTTP Error 409: Conflict":
				print "conflict"
				report_fail_text += "Auto Merge[fail]: Project["+project+"] Branch["+br+"] request conflict.\r\n"
				continue
			else:
				print "error"+str(e)
				continue

		#Accpet MR
		try:
			report_succ_text = report_succ_text + Accpet_MR(api_url,project_id,mergeId,project,br)
		except IOError, e:
			if str(e) == "HTTP Error 405: Method Not Allowed":
				report_fail_text += "Auto Merge[fail]: Project["+project+"] Branch["+br+"] code conflict.\r\n"
				print "conflict"
				continue
			else:
				print "error"+str(e)
				continue
	return_text = return_text + report_fail_text + "\r\n\r\n\r\n"+report_succ_text
	return return_text

	
def scan_project():

	report_text = ""
	for cc in web_project_map:
		#print "project:              "+cc
		projectObj = {}
		project_id = web_project_map[cc]
		url = api_url+project_id+"/repository/branches?private_token="+token
		query_req = urllib2.Request(url)
		query_resp = urllib2.urlopen(query_req)
		info = json.loads(query_resp.read())
		
		branchList = []
		for ccc in info:
			br = ccc['name']
			obj = re.match(r'^feature.*',br)
			if obj:
				branchList.append(obj.group())
		
		#print branchList
		report_text = report_text + mergeBranch(cc,branchList)
		
	return report_text


if __name__== '__main__':
	#load branch config
	#scan_project()

	sendMail(scan_project())