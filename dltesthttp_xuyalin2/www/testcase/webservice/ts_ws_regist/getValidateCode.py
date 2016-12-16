#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0245.获取短信验证码
http://127.0.0.1:8280/mallws/regist/getValidateCode.json
{
    "tel": ""                             					//必填 手机号
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-手机号格式错误 2-发送间隔少于1分钟 3-发送失败 4-手机号已被注册
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.VerificationCodeResponse"
    }
}


参数校验:
    // 必须验证
    "tel"                         				@NotNull，不为空字符串，@Pattern(regexp = "^((13[0-9])|(15[^4,\\D])|(18[0,5-9]))\\d{8}$")

code说明:
    200-成功 400-非法的参数 500-服务器异常
"""
class getValidateCode(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    UserShop3 = wsData('RegistTmlShop')

    #手机号长度不正确
    def test_getValidateCode_long(self):
        ws=webservice()
        getCode=ws.getValidateCode(tel='185458956231')
        self.assertEqual(getCode.code,200)
        self.assertEqual(getCode.model['success'],'1')

    #手机号号段不正确
    def test_getValidateCode_style(self):
        ws=webservice()
        getCode=ws.getValidateCode(tel='21345678901')
        self.assertEqual(getCode.code,200)
        self.assertEqual(getCode.model['success'],'1')

    #手机号处于待审批状态（待审批账号：testsun456789 密码：123456 手机号：18349200236）
    def test_getValidateCode_approve(self):
        ws=webservice()
        getCode=ws.getValidateCode(tel='18349200236')
        self.assertEqual(getCode.code,200)
        self.assertEqual(getCode.model['success'],'4')

    #手机号处于审批拒绝状态
    def test_getValidateCode_refused(self):
        ws=webservice()
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','05','testsun456789')
        getCode=ws.getValidateCode(tel='18349200236')
        self.assertEqual(getCode.code,200)
        self.assertEqual(getCode.model['success'],'4')
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','02','testsun456789')

    #获取其他用户已成功注册的手机号验证码
    def test_getValidateCode_exist(self):
        ws=webservice()
        getCode=ws.getValidateCode(tel=self.UserShop1.registerTel)
        self.assertEqual(getCode.code,200)
        self.assertEqual(getCode.model['success'],'4')

    #获取其他用户未激活手机号的验证码
    def test_getValidateCode_noActivate(self):
        ws=webservice()
        getCode=ws.getValidateCode(tel=self.UserShop2.registerTel)
        self.assertEqual(getCode.code,200)
        self.assertEqual(getCode.model['success'],'4')


def suite():
    suite=unittest.TestSuite()
    suite.addTest(getValidateCode("test_getValidateCode_long"))
    suite.addTest(getValidateCode("test_getValidateCode_style"))
    suite.addTest(getValidateCode("test_getValidateCode_approve"))
    suite.addTest(getValidateCode("test_getValidateCode_refused"))
    suite.addTest(getValidateCode("test_getValidateCode_exist"))
    suite.addTest(getValidateCode("test_getValidateCode_noActivate"))
    return suite

