#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0262.密码找回验证码短信发送
http://127.0.0.1:8280/mallws/login/getValCodeForPsw.json
{
    "tel": "13800138000"        @NotNull，不为空字符串
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                //0-成功 1-手机号格式错误  2-手机号未注册 3-手机号未激活  4-发送间隔少于1分钟 9-验证码发送失败
		"valCode": "123456"           //验证码
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.login.GetValCodeForPswResponse"
    }
}

"""

class getValCodeForPsw(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')



    #正确获取密码找回验证码短信
    def test_getValCodeForPsw(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel=self.UserShop1.mobileNumber)
        self.assertEqual(getValCodeForPsw.model['success'],'0')
        self.assertNotEqual(getValCodeForPsw.model['valCode'],None)

    #手机号长度不正确
    def test_getValCodeForPsw_long(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel='185498565897845')
        self.assertEqual(getValCodeForPsw.model['success'],'1')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)

    #手机号号段不存在
    def test_getValCodeForPsw_style(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel='22345678901')
        self.assertEqual(getValCodeForPsw.model['success'],'1')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)

    #手机号未注册
    def test_getValCodeForPsw_noRegister(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel='18500000008')
        self.assertEqual(getValCodeForPsw.model['success'],'2')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)

    #手机号未激活
    def test_getValCodeForPsw_noActivate(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel=self.UserShop2.mobileNumber)
        self.assertEqual(getValCodeForPsw.model['success'],'3')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)

    #手机号待审批（待审批账号：testsun456789 密码：123456 手机号：18349200236）
    def test_getValCodeForPsw_approve(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel='18349200236')
        self.assertEqual(getValCodeForPsw.model['success'],'2')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)


    #手机号审批已拒绝（待审批账号：testsun456789 密码：123456 手机号：18349200236）
    def test_getValCodeForPsw_approveRefused(self):
        ws=webservice()
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','05','testsun456789')
        getValCodeForPsw=ws.getValCodeForPsw(tel='18349200236')
        self.assertEqual(getValCodeForPsw.model['success'],'2')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)

    #一分钟内重复发送短信验证码
    def test_getValCodeForPsw_oneMinute(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel=self.UserShop1.mobileNumber)
        self.assertEqual(getValCodeForPsw.model['success'],'0')
        self.assertNotEqual(getValCodeForPsw.model['valCode'],None)
        getValCodeForPswRepeat=ws.getValCodeForPsw(tel=self.UserShop1.mobileNumber)
        self.assertEqual(getValCodeForPsw.model['success'],'4')
        self.assertEqual(getValCodeForPsw.model['valCode'],None)

    #大于一分钟重复发送短信验证码
    def test_getValCodeForPsw_notOneMinute(self):
        ws=webservice()
        getValCodeForPsw=ws.getValCodeForPsw(tel=self.UserShop1.mobileNumber)
        self.assertEqual(getValCodeForPsw.model['success'],'0')
        self.assertNotEqual(getValCodeForPsw.model['valCode'],None)
        time.sleep(65)
        getValCodeForPswRepeat=ws.getValCodeForPsw(tel=self.UserShop1.mobileNumber)
        self.assertEqual(getValCodeForPswRepeat.model['success'],'0')
        self.assertNotEqual(getValCodeForPsw.model['valCode'],None)

    def tearDown(self):
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','02','testsun456789')

def suite():
    suite=unittest.TestSuite()
    # 暂不获取短信
    # suite.addTest(getValCodeForPsw("test_getValCodeForPsw"))
    suite.addTest(getValCodeForPsw("test_getValCodeForPsw_long"))
    suite.addTest(getValCodeForPsw("test_getValCodeForPsw_style"))
    suite.addTest(getValCodeForPsw("test_getValCodeForPsw_noRegister"))
    suite.addTest(getValCodeForPsw("test_getValCodeForPsw_noActivate"))
    suite.addTest(getValCodeForPsw("test_getValCodeForPsw_approve"))
    suite.addTest(getValCodeForPsw("test_getValCodeForPsw_approveRefused"))
    #suite.addTest(getValCodeForPsw("test_getValCodeForPsw_oneMinute"))
    #suite.addTest(getValCodeForPsw("test_getValCodeForPsw_notOneMinute"))
    return suite
