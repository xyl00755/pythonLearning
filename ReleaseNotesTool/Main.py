#!/usr/bin/python  
# -*- coding:utf-8 -*- 


from Tkinter import *
from ttk import *
from gitlab import *
import tkMessageBox
import time
from wxPython._wx import NULL

class rn_tool:
    info_text = NULL
    ccb_start = NULL
    ccb_end = NULL
    def start_compare_tags(self):
        start_tag = self.ccb_start.get()
        end_tag = self.ccb_end.get()
        
        if start_tag == "" or end_tag == ""  :
            tkMessageBox.showinfo( "Warning", "Please select the tag")
        else:
        #tkMessageBox.showinfo( "Hello Python", "Hello World")
            output_info = []
            for br in project_map:
                self.info_text.insert(INSERT, br+"\n")
                project_id = project_map[br]

                time.sleep(0.1)
                self.info_text.update()
                output_info+=find_releasenotes ( project_id, start_tag, end_tag )

    
            new_index = []
            for idd in output_info:
                if idd not in new_index:
                    new_index.append(idd)
                    list.sort(new_index)
    
            fscr = open("./releasenotes/index.json", "w")
            fscr.write(json.dumps(new_index,sort_keys=True))
            fscr.close()

        lb = Label(self.root, text="Compare Tag is finished!")
        lb.grid(row=2,column=0,columnspan=5)    
    
    def __init__(self):

        self.root = Tk()
        self.root.title("ReleaseNotes  Tool")
        self.root.geometry('600x400')                 
        self.root.resizable(width=False, height=True) 
        
        self.tags = Get_Tags()
        
        self.lb_start = Label(self.root, text="The Start Tag:")
        self.lb_start.grid(row=0,column=0)
        
        ccb_start_str = StringVar()

        self.ccb_start = Combobox(self.root, textvariable=ccb_start_str)
        self.ccb_start["values"] = self.tags
        self.ccb_start["state"] = "readonly"
        #self.ccb_start.current(1)
        self.ccb_start.grid(row=0,column=1)
        
        lb_end = Label(self.root, text="The End Tag:")
        lb_end.grid(row=0,column=2)

        ccb_end_str = StringVar()
        self.ccb_end = Combobox(self.root, textvariable=ccb_end_str)
        self.ccb_end["values"] = self.tags
        self.ccb_end["state"] = "readonly"
        self.ccb_end.current(1)
        self.ccb_end.grid(row=0,column=3)
        
        btn_compare = Button(self.root, text ="Compare Tags", command = self.start_compare_tags)
        btn_compare.grid(row=0,column=4)


        self.info_text = Text(self.root)
        #self.info_text.pack(side=LEFT,fill=BOTH)
        self.info_text.grid(row=1,column=0,columnspan=5)



if __name__== "__main__":
    d = rn_tool()
    mainloop()
    #print Get_Tags()