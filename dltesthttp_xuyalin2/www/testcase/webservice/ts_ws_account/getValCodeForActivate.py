#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0290.获取激活验证码(6位验证码)
http://127.0.0.1:8280/mallws/mydl/account/getValCodeForActivate.json
{
	"token":"123",
	"tel": "13800138000"        @NotNull，不为空字符串
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                //0-成功 1-手机号格式错误 4-发送间隔少于1分钟 9-验证码发送失败
		"valCode": "1234"              //验证码
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.account.GetValCodeForActivateResponse"
    }
}
"""

class getValCodeForActivate(unittest.TestCase):
    UserShop2=wsData('TmlShop2')
    UserShop1=wsData('TmlShop')

    #正确获取激活手机验证码
    def test_getValCodeForActivate(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCode.model['success'],'0')
        self.assertNotEqual(getValCode.model['valCode'],None)

    #手机号格式错误(长度超过11位)
    def test_getValCodeForActivate_styleErrorLong(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel='183495265894587')
        self.assertEqual(getValCode.model['success'],'1')
        self.assertEqual(getValCode.model['valCode'],None)

    #手机号格式错误(号段不存在)
    def test_getValCodeForActivate_styleError(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel='12345678912')
        self.assertEqual(getValCode.model['success'],'1')
        self.assertEqual(getValCode.model['valCode'],None)

    #手机号为空'
    def test_getValCodeForActivate_null(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel='null')
        self.assertEqual(getValCode.model['success'],'1')
        self.assertEqual(getValCode.model['valCode'],None)

    #手机号为其他人手机号(接口未验证手机号是否存在数据库)
    def test_getValCodeForActivate_other(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel=self.UserShop1.mobileNumber)
        self.assertEqual(getValCode.model['success'],'0')
        self.assertNotEqual(getValCode.model['valCode'],None)

    #一分钟内重复获取手机号激活验证码
    def test_getValCodeForActivate_repeatOneMinute(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCode.model['success'],'0')
        self.assertNotEqual(getValCode.model['valCode'],None)
        getValCode2=ws.getValCodeForActivate(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCode2.model['success'],'4')
        self.assertEqual(getValCode2.model['valCode'],None)

    #非一分钟内重复获取手机号激活验证码
    def test_getValCodeForActivate_repeatNotOneMinute(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCode=ws.getValCodeForActivate(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCode.model['success'],'0')
        self.assertNotEqual(getValCode.model['valCode'],None)
        time.sleep(65)
        getValCode2=ws.getValCodeForActivate(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCode2.model['success'],'0')
        self.assertNotEqual(getValCode2.model['valCode'],None)

def suite():
    suite=unittest.TestSuite()
    #suite.addTest(getValCodeForActivate("test_getValCodeForActivate"))
    suite.addTest(getValCodeForActivate("test_getValCodeForActivate_styleErrorLong"))
    suite.addTest(getValCodeForActivate("test_getValCodeForActivate_styleError"))
    suite.addTest(getValCodeForActivate("test_getValCodeForActivate_null"))
    #suite.addTest(getValCodeForActivate("test_getValCodeForActivate_other"))
    #suite.addTest(getValCodeForActivate("test_getValCodeForActivate_repeatOneMinute"))
    #suite.addTest(getValCodeForActivate("test_getValCodeForActivate_repeatNotOneMinute"))
    return suite


