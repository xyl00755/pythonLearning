#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
2.发送短信验证码
http://127.0.0.1:8080/mallws/shoppingcart/sendMessage.json
{
    "token":"123",                       // 必须
    "tel":"15281213560"                // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                 //0-成功 1-手机号格式错误   2-发送间隔少于1分钟   3-验证码发送失败
    },
     "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}
"""

import unittest

from www.api.webservice import *
from www.common.excel import *


class sendMessage(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    # S1.成功发送短信验证码
    def test_sendMessage_normal(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber)
        self.assertEqual(sendMessage.model['success'],'0')

    # S2.手机号长度不正确
    def test_sendMessage_telLen(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage(tel='1850000000')
        self.assertEqual(sendMessage.model['success'],'1')
        sendMessage = ws.sendMessage(tel='185000000000')
        self.assertEqual(sendMessage.model['success'],'1')

    # S3.手机号段不正确
    def test_sendMessage_segment(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage(tel='2850000000')
        self.assertEqual(sendMessage.model['success'],'1')

    # S4.手机号未激活——由于终端店需要强制激活，故未激活号码也能收到短信
    def test_sendMessage_noActivate(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        sendMessage = ws.sendMessage(tel=self.UserShop2.mobileNumber)
        self.assertEqual(sendMessage.model['success'],'0')

    # S5.一分钟内重复发送短信验证码
    def test_sendMessage_oneMinute(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber)
        self.assertEqual(sendMessage.model['success'],'0')
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber)
        self.assertEqual(sendMessage.model['success'],'2')

    # S6.一分钟后获取短信验证码
    def test_sendMessage_oneMinuteMore(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber)
        self.assertEqual(sendMessage.model['success'],'0')
        import time
        time.sleep(65)
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber)
        self.assertEqual(sendMessage.model['success'],'0')

    # S7.不带token或token错误
    def test_sendMessage_noToken(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber,token='null')
        self.assertEqual(sendMessage.code,600)
        sendMessage = ws.sendMessage(tel=self.UserShop1.mobileNumber,token='errorToken')
        self.assertEqual(sendMessage.code,100)

    # S8.不带tel——准确来说应该是400，由于没处理该异常导致返回500
    def test_sendMessage_noTel(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        sendMessage = ws.sendMessage()
        self.assertEqual(sendMessage.code,500)

def suite():
    suite=unittest.TestSuite()
    # 屏蔽需要发送短信的用例
    #suite.addTest(sendMessage("test_sendMessage_normal"))
    suite.addTest(sendMessage("test_sendMessage_telLen"))
    suite.addTest(sendMessage("test_sendMessage_segment"))
    #suite.addTest(sendMessage("test_sendMessage_noActivate"))
    #suite.addTest(sendMessage("test_sendMessage_oneMinute"))
    #suite.addTest(sendMessage("test_sendMessage_oneMinuteMore"))
    suite.addTest(sendMessage("test_sendMessage_noToken"))
    suite.addTest(sendMessage("test_sendMessage_noTel"))
    return suite
