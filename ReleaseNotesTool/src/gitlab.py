#!/usr/bin/python  
# -*- coding:utf-8 -*- 
import urllib2
import json
import re
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
project_map = {"dliosjxs":"100",
"dlgateway":"123",
"dlandroidjxs":"107",
"dlcoupon":"124",
"dlopx":"120",
"dlcms":"122",
"dlsql":"110",
"dloauth2":"109",
"dlpromotionx":"125",
"dlcoupay":"126",
"dlrcmd":"130",
"dlcodis":"128",
"dlscheduler":"52",
"dlpublic":"73",
"node-admin-java":"96",
"dlios":"99",
"dltool":"79",
"dlcommon-jar":"70",
"dlmall":"80",
"dlsms":"54",
"dlnews":"85",
"dladmin":"81",
"dleye":"19",
"dlhelp":"68",
"dlsaleright":"64",
"dlorder":"36",
"dlfrontend":"71",
"dlpay":"27",
"dlpromotion":"67",
"dlmerchandise":"65",
"dlcategroy":"63",
"dlcache":"86",
"dlworkflow":"82",
"dlwebservice":"76",
"dlcompany":"83",
"dluser":"84",
"dllycos":"95",
"dlstaff":"115",
"dlmetaq":"127",
"dldata":"88",
"privilege":"39",
"cas-server3-5-2":"37",
"ios":"74",
"andriod":"75",
"dlfirst":"41",
"cacheservice":"18",
"thousandssunny-manager":"14",
"node-web-admin":"94"}
'''

#token = "x51LvNyUoE8jwkxxc44q"
api_url = "http://idanlu.com:8000/api/v3/"
#project_id = project_map[sys.argv[2]]
#tag_from_str = sys.argv[3]
#tag_to_str = sys.argv[4]

#print project_id
#print tag_from_str
#print tag_to_str

key = "b2b0ee62b00d6ff60ae4342ae81fcd55890165b6"
redmine_url = "http://182.92.230.201:3000/"


token = "s6ds3VWzz6PAsBq_t9U4"


def Get_Tags():
    project_id = "80"

    branch_info_url = "http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/tags?private_token="+token

    try:
        query_req = urllib2.Request(branch_info_url)
        query_resp = urllib2.urlopen(query_req)
        branch_info = json.loads(query_resp.read())
        
        tag_list = []
        
        for tag in branch_info:
            tag_list.append(tag["name"])
        
        return tag_list
    except IOError:
        print "get tags fail"
        pass


def getIssueJson( issue_id ):
    query_url = redmine_url+'issues/'+issue_id+'.json?key='+key+'&include=journals'
    #query_url = redmine_url+'issues/'+issue_id+'.json?key='+key
    query_req = urllib2.Request(query_url)
    query_resp = urllib2.urlopen(query_req)
    return query_resp.read()

def check_folder():
    if not os.path.exists('./releasenotes'):
        os.makedirs('./releasenotes')

def find_releasenotes ( project, tag_from, tag_to ):

    check_folder()
    url = api_url+"projects/"+project+"/repository/compare?private_token="+token+"&from="+tag_from+"&to="+tag_to
    query_url = url
    query_req = urllib2.Request(query_url)
    query_resp = urllib2.urlopen(query_req)
    tags = json.loads(query_resp.read())
    #print tags

    commits = tags["commits"]
    index = []
    #print commits
    for cc in commits:
        #str = cc["id"]
        #print str.encode("UTF-8")
        str2 = cc["title"]
        #print str2.encode("UTF-8")
        obj = re.match( r'(.*)(["bug""requirement""错误""需求"]#)(\d+)(.*)', str2)
        if obj:
            bug_id = obj.group(3)
            index.append(bug_id)
            #print bug_id.encode("UTF-8")
            #print getIssueJson(bug_id)
    
    
    new_index = []
    for id in index:
        if id not in new_index and id != "2024":
            new_index.append(id)
    list.sort(new_index)
    #print new_index
    
    

#write issue json file
    for id in new_index:
        fscr = open("./releasenotes/"+id+".json", "w")
        fscr.write(getIssueJson(id))
        fscr.close()
    
    return new_index



def get_all_diff(tag_from, tag_to):
    output_info = []
    for br in project_map:
        print br
        project_id = project_map[br]
        
        output_info+=find_releasenotes ( project_id, tag_from, tag_to )
    
    
    fscr = open("./releasenotes/index.json", "w")
    fscr.write(json.dumps(output_info,sort_keys=True))
    fscr.close()
    
    return output_info
    
    
    