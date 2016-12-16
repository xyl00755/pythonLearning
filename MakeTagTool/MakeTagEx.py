#!/usr/bin/python  
# -*- coding:utf-8 -*- 


import urllib2
import json
import os


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

'''
project_check = {"dladmin":os.getenv(key='dladmin'),
"dlcategroy":os.getenv(key='dlcategroy'),
"dlcms":os.getenv(key='dlcms'),
"dlcompany":os.getenv(key='dlcompany'),
"dlcoupay":os.getenv(key='dlcoupay'),
"dlcoupon":os.getenv(key='dlcoupon'),
"dldata":os.getenv(key='dldata'),
"dlfrontend":os.getenv(key='dlfrontend'),
"dlhelp":os.getenv(key='dlhelp'),
"dllycos":os.getenv(key='dllycos'),
"dlmall":os.getenv(key='dlmall'),
"dlmerchandise":os.getenv(key='dlmerchandise'),
"dlnews":os.getenv(key='dlnews'),
"dloauth2":os.getenv(key='dloauth2'),
"dlopx":os.getenv(key='dlopx'),
"dlorder":os.getenv(key='dlorder'),
"dlpay":os.getenv(key='dlpay'),
"dlpromotion":os.getenv(key='dlpromotion'),
"dlpromotionx":os.getenv(key='dlpromotionx'),
"dlpublic":os.getenv(key='dlpublic'),
"dlsaleright":os.getenv(key=':True'),
"dlscheduler":os.getenv(key='dlscheduler'),
"dlsms":os.getenv(key='dlsms'),
"dluser":os.getenv(key='dluser'),
"dlworkflow":os.getenv(key='dlworkflow'),
"cas-server3-5-2":os.getenv(key='cas-server3-5-2'),
"node-admin-java":os.getenv(key='node-admin-java'),
"node-web-admin":os.getenv(key='node-web-admin'),
"privilege":os.getenv(key='privilege'),
"dlcache":os.getenv(key='dlcache'),
"dlcodis":os.getenv(key='dlcodis'),
"dlmetaq":os.getenv(key='dlmetaq'),
"dlrcmd":os.getenv(key='dlrcmd')
}
'''

latest_tag_name = os.getenv(key='latest_tag_name').replace(".","%2E")
new_tag_name = os.getenv(key='new_tag_name')
token = "oGmBRCQXj9tXzLCQiVCu"
strli = os.getenv(key='dlActiveList')
li = strli.split(",")
print li




class mt_tool:
	tag_name_lists = []
	latest_commit_id = ""
	commit_id_byTag = ""

	
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
		for ck in project_map:
			project_id = project_map[ck]
			make_tag_url = "http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/tags?private_token="+token
			if ck in li:
				ref_id = self.get_commit_latest(project_id)
				#print "self.get_commit_latest"+ref_id
				da="tag_name="+new_tag_name+"&ref="+ref_id+"&message=\"Auto tag\""
				#print da
			else:
				ref_id = self.get_commit_byTag(project_id)
				#print "self.get_commit_byTag="+ref_id
				da="tag_name="+new_tag_name+"&ref="+ref_id+"&message=\"Auto tag\""
				#print da
				
			if self.get_commit_byTag(project_id) != "" :
				try:
					print "Make tag:project_id="+project_id+",commit_id="+ref_id+",new_tag_name="+new_tag_name
					#query_req = urllib2.Request(url,data=da)
					#query_resp = urllib2.urlopen(query_req)
					
					#self.info_text.insert(INSERT, query_resp.read()+"\n")
					#time.sleep(0.1)
					#self.info_text.update()
					
				except IOError:
					print "Make tag fail, maybe have same tag"
					return
			else:
				pass
d = mt_tool()
d.make_tag()