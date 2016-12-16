#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0263.重置密码（前台已校验过验证码）
http://127.0.0.1:8280/mallws/login/resetPsw.json
{
    "tel": "13800138000",           //必填 用户帐号
    "password": "123456"            //必填 密码
	"passwordConfirm": "123456"     //必填 确认密码
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"             //0-成功 1-失败
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.login.ResetPswResponse"
    }
}
"""

class resetPsw(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    #正确重置密码
    def test_resetPsw(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel=self.UserShop2.mobileNumber,password=self.UserShop2.password,passwordConfirm=self.UserShop2.password)
        self.assertEqual(resetPsw.model['success'],'0')

    #设置密码为特殊字符
    def test_resetPsw_special(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel=self.UserShop2.mobileNumber,password='~!@#$%^&*()',passwordConfirm='~!@#$%^&*()')
        self.assertEqual(resetPsw.model['success'],'0')


    #手机号长度不正确
    def test_resetPsw_long(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel='185485978569874',password=self.UserShop2.password,passwordConfirm=self.UserShop2.password)
        self.assertEqual(resetPsw.model['success'],'1')

    #手机号号段不存在
    def test_resetPsw_style(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel='12345678912',password=self.UserShop2.password,passwordConfirm=self.UserShop2.password)
        self.assertEqual(resetPsw.model['success'],'1')

    #密码和确认密码不一致
    def test_resetPsw_inconsistent(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel=self.UserShop2.mobileNumber,password=self.UserShop2.password,passwordConfirm='123456')
        self.assertEqual(resetPsw.model['success'],'1')

    #用户账号为空
    def test_resetPsw_telNull(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel=None,password=self.UserShop2.password,passwordConfirm=self.UserShop2.password)
        self.assertEqual(resetPsw.model['success'],'1')

    #密码为空
    def test_resetPsw_pswNull(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel=self.UserShop2.mobileNumber,password=None,passwordConfirm=self.UserShop2.password)
        self.assertEqual(resetPsw.model['success'],'1')

    #确认密码为空
    def test_resetPsw_confirmPswNull(self):
        ws=webservice()
        resetPsw=ws.resetPsw(tel=self.UserShop2.mobileNumber,password=self.UserShop2.password,passwordConfirm=None)
        self.assertEqual(resetPsw.model['success'],'1')

    def tearDown(self):
         update('update dluser.dl_user set user_passwd= ? where user_id = ?', hashlib.md5(self.UserShop2.password).hexdigest(), self.UserShop2.userId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(resetPsw("test_resetPsw"))
    suite.addTest(resetPsw("test_resetPsw_special"))
    suite.addTest(resetPsw("test_resetPsw_long"))
    suite.addTest(resetPsw("test_resetPsw_style"))
    suite.addTest(resetPsw("test_resetPsw_inconsistent"))
    suite.addTest(resetPsw("test_resetPsw_telNull"))
    suite.addTest(resetPsw("test_resetPsw_pswNull"))
    suite.addTest(resetPsw("test_resetPsw_confirmPswNull"))
    return suite