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

class mt_tool:
	
    info_text = NULL
    ccb_start = NULL
    ccb_end = NULL
    def start_compare_tags(self):
        token = self.en_token.get()
        tag_name = self.en_tagname.get()
        if token == "" or tag_name == ""  :
            tkMessageBox.showinfo( "Warning", "Please input tag and your token")
        else:
            for br in project_map:
                project_id = project_map[br]
                branch_info_url = "http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/branches/develop?private_token="+token
				#获取commit id
                try:
                    query_req = urllib2.Request(branch_info_url)
                    query_resp = urllib2.urlopen(query_req)
                    branch_info = json.loads(query_resp.read())
                    ref_id = branch_info["commit"]["id"]
                except IOError:
                    tkMessageBox.showinfo( "Error", "Select project or branch fail")
                    return
					
				#打tag
                url = "http://idanlu.com:8000/api/v3/projects/"+project_id+"/repository/tags?private_token="+token
            
                da="tag_name="+tag_name+"&ref="+ref_id+"&message=\"Auto tag\""
                try:
                    query_req = urllib2.Request(url,data=da)
                    query_resp = urllib2.urlopen(query_req)
                    
                    self.info_text.insert(INSERT, query_resp.read()+"\n")
                    time.sleep(0.1)
                    self.info_text.update()
    
                except IOError:
                    tkMessageBox.showinfo( "Error", "Make tag fail, maybe have same tag")
                    return
            pass
    
    def start_compare_tags_test(self):
        token = self.en_token.get()
        tag_name = self.en_tagname.get()
        branch_info_url = "http://idanlu.com:8000/api/v3/projects/119/repository/branches/master?private_token="+token

        try:
            query_req = urllib2.Request(branch_info_url)
            query_resp = urllib2.urlopen(query_req)
            branch_info = json.loads(query_resp.read())
            #print branch_info
            ref_id = branch_info["commit"]["id"]
        except IOError:
            tkMessageBox.showinfo( "Error", "Make tag fail")
            return
    
        url = "http://idanlu.com:8000/api/v3/projects/119/repository/tags?private_token="+token
    
        da="tag_name="+tag_name+"&ref="+ref_id+"&message=\"Auto tag\""
        try:
            query_req = urllib2.Request(url,data=da)
            query_resp = urllib2.urlopen(query_req)
            
            self.info_text.insert(INSERT, query_resp.read()+"\n")
            time.sleep(0.1)
            self.info_text.update()

        except IOError:
            tkMessageBox.showinfo( "Error", "Make tag fail, maybe have same tag")
            return
    
    def __init__(self):

        self.root = Tk()
        self.root.title("MakeTagTool")
        self.root.geometry('600x400')                 
        self.root.resizable(width=False, height=True) 
        
        #self.tags = Get_Tags()
        
        self.lb_tagname = Label(self.root, text="TagName that you want make:")
        self.lb_tagname.grid(row=0,column=0)
        self.en_tagname = Entry(self.root)
        self.en_tagname.grid(row=0,column=1)

        self.lb_token = Label(self.root, text="Input your token:")
        self.lb_token.grid(row=1,column=0)
        self.en_token = Entry(self.root)
        self.en_token.grid(row=1,column=1)        
        
        btn_compare = Button(self.root, text ="Make Tag", command = self.start_compare_tags)
        btn_compare.grid(row=1,column=2)

        self.info_text = Text(self.root)
        self.info_text.grid(row=5,column=0,columnspan=5)



if __name__== "__main__":
	
    d = mt_tool()
    mainloop()
