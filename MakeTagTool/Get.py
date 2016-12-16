#!/usr/bin/python  
# -*- coding:utf-8 -*- 


from Tkinter import *
from ttk import *
import tkMessageBox
import time
from wxPython._wx import NULL
import urllib2
import json


project_map = {"dladmin":"81",
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

project_check = {"dladmin":False,
"dlcategroy":True,
"dlcms":True,
"dlcompany":True,
"dlcoupay":True,
"dlcoupon":True,
"dldata":True,
"dlfrontend":True,
"dlhelp":True,
"dllycos":True,
"dlmall":True,
"dlmerchandise":True,
"dlnews":True,
"dloauth2":True,
"dlopx":True,
"dlorder":True,
"dlpay":True,
"dlpromotion":True,
"dlpromotionx":True,
"dlpublic":True,
"dlsaleright":True,
"dlscheduler":True,
"dlsms":True,
"dluser":True,
"dlworkflow":True,
"cas-server3-5-2":True,
"node-admin-java":True,
"node-web-admin":True,
"privilege":True,
"dlcache":True,
"dlcodis":True,
"dlmetaq":True,
"dlrcmd":True
}

latest_tag_name = "Web_V2.1.5".replace(".","%2E")
new_tag_name = "new_tag_name"
token = "oGmBRCQXj9tXzLCQiVCu"

class mt_tool:
	tag_name_lists = []
	latest_commit_id = ""
	commit_id_byTag = ""
	
	'''def get_history_commit(self,project_id):
		project_tags_url="http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/tags?private_token="+self.token
		try:
			query_req = urllib2.Request(project_tags_url)
			query_resp = urllib2.urlopen(query_req)
			tag_lists = json.loads(query_resp.read())
			self.latest_commit_id = tag_lists[0]["commit"]["id"]
			#print self.latest_commit_id
			self.latest_tag_name = tag_lists[0]["name"]
			#print self.latest_tag_name
			for cc in tag_lists:
				#print cc["name"]
				self.tag_name_lists.append(str(cc["name"]))
			
		except IOError:
			tkMessageBox.showinfo( "Error", "Select project or branch fail")
			return self.latest_tag_name
			
		return self.latest_commit_id
	'''
	
	def get_commit_byTag(self,project_id):
		commitByTag_url="http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/commits/"+latest_tag_name+"?private_token="+token
		#print "commitByTag_url"+commitByTag_url
		try:
			query_req = urllib2.Request(commitByTag_url)
			query_resp = urllib2.urlopen(query_req)
			commit_info = json.loads(query_resp.read())
			self.commit_id_byTag = commit_info["id"]
			#print self.commit_id_byTag
		except IOError:
			print "get_commit_byTag fail,commitByTag_url=" + commitByTag_url
			return ""
			
		return self.commit_id_byTag
	
	
	def get_commit_latest(self,project_id):
		branch_info_url = "http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/branches/develop?private_token="+token
		#获取commit id
		try:
			query_req = urllib2.Request(branch_info_url)
			query_resp = urllib2.urlopen(query_req)
			branch_info = json.loads(query_resp.read())
			self.latest_commit_id = branch_info["commit"]["id"]
			#print self.latest_commit_id
		except IOError:
			print "get_commit_latest fail,branch_info_url=" + branch_info_url
			return ""
			
		return self.latest_commit_id

	def make_tag(self):
		for ck in project_check:
			isChecked = project_check[ck]
			project_id = project_map[ck]
			make_tag_url = "http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/tags?private_token="+token
			if isChecked == True:
				ref_id = self.get_commit_latest(project_id)
				#print "self.get_commit_latest"+ref_id
				da="tag_name="+new_tag_name+"&ref="+ref_id+"&message=\"Auto tag\""
				
			else:
				ref_id = self.get_commit_byTag(project_id)
				#print "self.get_commit_byTag="+ref_id
				da="tag_name="+new_tag_name+"&ref="+ref_id+"&message=\"Auto tag\""
				
			try:
				print "Make tag:project_id="+project_id+",commit_id="+ref_id
				#query_req = urllib2.Request(url,data=da)
				#query_resp = urllib2.urlopen(query_req)
				
				#self.info_text.insert(INSERT, query_resp.read()+"\n")
				#time.sleep(0.1)
				#self.info_text.update()
				
			except IOError:
				print "Make tag fail, maybe have same tag"
				return
	
d = mt_tool()
d.make_tag()