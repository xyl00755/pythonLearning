#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0268.获取原手机号解绑短信验证码(4位验证码)
http://127.0.0.1:8280/mallws/mydl/account/getValCodeForUnbindPhone.json
{
    "token":"123",					    //必须
    "tel": "13800138000"               //必须 原手机号码
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                //0-成功 1-手机号格式错误 2-发送间隔少于1分钟 3-发送失败
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}
"""

class getValCodeForUnbindPhone(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    #正确获取原手机号解绑短信验证码
    def test_getValCodeForUnbindPhone(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCodeForUnbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCodeForUnbindPhone.model['success'],'0')

    #手机号长度不正确
    def test_getValCodeForUnbindPhone_long(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCodeForUnbindPhone=ws.getValCodeForUnbindPhone(tel='185498565897485')
        self.assertEqual(getValCodeForUnbindPhone.model['success'],'1')

    #手机号号段不正确
    def test_getValCodeForUnbindPhone_style(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCodeForUnbindPhone=ws.getValCodeForUnbindPhone(tel='12345678945')
        self.assertEqual(getValCodeForUnbindPhone.model['success'],'1')

    #一分钟内重复发送短信
    def test_getValCodeForUnbindPhone_oneMinute(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCodeForUnbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCodeForUnbindPhone.model['success'],'0')
        getValCodeForUnbindPhone2=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCodeForUnbindPhone2.model['success'],'2')

    #非一分钟内重读发送短信
    def test_getValCodeForUnbindPhone_notOneMinute(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getValCodeForUnbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCodeForUnbindPhone.model['success'],'0')
        time.sleep(65)
        getValCodeForUnbindPhone2=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCodeForUnbindPhone2.model['success'],'0')


def suite():
    suite=unittest.TestSuite()
    #suite.addTest(getValCodeForUnbindPhone("test_getValCodeForUnbindPhone"))
    suite.addTest(getValCodeForUnbindPhone("test_getValCodeForUnbindPhone_long"))
    suite.addTest(getValCodeForUnbindPhone("test_getValCodeForUnbindPhone_style"))
    #suite.addTest(getValCodeForUnbindPhone("test_getValCodeForUnbindPhone_oneMinute"))
    #suite.addTest(getValCodeForUnbindPhone("test_getValCodeForUnbindPhone_notOneMinute"))
    return suite