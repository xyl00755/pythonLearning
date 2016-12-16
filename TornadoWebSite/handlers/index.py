#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import methods.db as mrd

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # greeting =self.get_argument('greeting','hellox')
        # self.write(greeting+',welcome you to read:www.baidu.com')
        self.render("index1.html")

    def post(self, *args, **kwargs):
        username=self.get_argument("username")
        password=self.get_argument("password")
        # self.write(username+'xyl')
        user_infos=mrd.select_table("Userinfo",'*','username',username)
        if user_infos:
            db_pwd=user_infos[0][1]
            if db_pwd ==password:
                self.write("welcome you:"+username)
            else:self.write("your password was not right.")
        else:
            self.write("there is no thi user.")
