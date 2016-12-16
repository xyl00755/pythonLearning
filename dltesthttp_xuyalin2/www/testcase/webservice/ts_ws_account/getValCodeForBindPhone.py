#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0269.获取新手机号激活验证码(4位验证码)
http://127.0.0.1:8280/mallws/mydl/account/getValCodeForBindPhone.json
{
	"token":"123",				//必须
	"tel": "13800138000"        //必须 新手机号码
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                //0-成功 1-手机号格式错误 2-发送间隔少于1分钟 3-未进行解绑操作 4-发送失败	5-手机号在系统存在
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}
"""
class getValCodeForBindPhone(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    #正确获取新手机号激活验证码(设置新手机号：18500000008)
    def test_getValCodeForBindPhone(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel='18500000008')
        self.assertEqual(bindPhone.model['success'],'0')

    #手机号长度不正确
    def test_getValCodeForBindPhone_long(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel='18500000008123')
        self.assertEqual(bindPhone.model['success'],'1')

    #手机号号段不存在
    def test_getValCodeForBindPhone_style(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel='12345678945')
        self.assertEqual(bindPhone.model['success'],'1')

    #输入已解绑的手机号
    def test_getValCodeForBindPhone_unbind(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(bindPhone.model['success'],'5')

    #手机号已激活
    def test_getValCodeForBindPhone_activate(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel=self.UserShop1.mobileNumber)
        self.assertEqual(bindPhone.model['success'],'5')

    #手机号未激活
    def test_getValCodeForBindPhone_noActivate(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop1.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(bindPhone.model['success'],'5')

    #手机号待审批（待审批账号：testsun456789 密码：123456 手机号：18349200236）
    def test_getValCodeForBindPhone_approve(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel='18349200236')
        self.assertEqual(bindPhone.model['success'],'5')

    #手机号审批拒绝
    def test_getValCodeForBindPhone_approveRefused(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop1.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','05','testsun456789')
        bindPhone=ws.getValCodeForBindPhone(tel='18349200236')
        self.assertEqual(bindPhone.model['success'],'5')
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','02','testsun456789')

    #手机号未进行解绑
    def test_getValCodeForBindPhone_noUnbind(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        bindPhone=ws.getValCodeForBindPhone(tel='18500000008')
        self.assertEqual(bindPhone.model['success'],'3')

    #一分钟内重复发送验证码
    def test_getValCodeForBindPhone_oneMinute(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel='18500000008')
        self.assertEqual(bindPhone.model['success'],'0')
        bindPhone2=ws.getValCodeForBindPhone(tel='18500000008')
        self.assertEqual(bindPhone.model['success'],'2')

    #非一分钟内重复发送验证码
    def test_getValCodeForBindPhone_noOneMinute(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        unbindPhone=ws.getValCodeForUnbindPhone(tel=self.UserShop2.mobileNumber)
        self.assertEqual(unbindPhone.model['success'],'0')
        bindPhone=ws.getValCodeForBindPhone(tel='18500000008')
        self.assertEqual(bindPhone.model['success'],'0')
        time.sleep(65)
        bindPhone=ws.getValCodeForBindPhone(tel='18500000008')
        self.assertEqual(bindPhone.model['success'],'0')

def suite():
    suite=unittest.TestSuite()
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_long"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_style"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_unbind"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_activate"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_noActivate"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_approve"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_approveRefused"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_noUnbind"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_oneMinute"))
    #suite.addTest(getValCodeForBindPhone("test_getValCodeForBindPhone_noOneMinute"))
    return suite