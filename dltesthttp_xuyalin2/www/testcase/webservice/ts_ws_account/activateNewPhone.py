#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import *

"""
0270.激活新的手机号码
http://127.0.0.1:8280/mallws/mydl/account/activateNewPhone.json
{
	"token":"123",											// 必须
    "valCode": "1234"                                       // 必须 新手机收到的验证码
	"tel":"13800138000"										// 必须 新手机号码
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                     // 0-激活成功 1-激活失败 2-手机号已被占用 3-验证码错误 5-其他错误

    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}
"""

class activateNewPhone(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    #正确激活新的手机号
    def test_activateNewPhone(self):
        ws=webservice()
        loginBody=ws.login(self.UserShop2.username,self.UserShop2.password)
        ws.getValCodeForBindPhone(tel='18798745623')
        # newValCode = ws.__getattribute__('sendSmsContent2')
        # self.assertEqual(newValCode,'1234')

    #输入手机号长度不正确

    #输入手机号号段不存在

    #输入其他用户未激活的手机号

    #输入其他用户已激活的手机号

    #输入待审批的手机号

    #输入已拒绝的手机号

    #输入验证码错误



def suite():
    suite=unittest.TestSuite()
    #suite.addTest(activateNewPhone("test_activateNewPhone"))
    return suite