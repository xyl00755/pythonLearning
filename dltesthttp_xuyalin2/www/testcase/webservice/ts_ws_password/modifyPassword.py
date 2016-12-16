#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0010.修改密码
http://127.0.0.1:8280/mallws/mydl/password/modifyPassword.json
{
    "token":"51aca877e23e4e5f900d7664f56263d8",         // 必须
    "oldPassword":"4f7c733d0ff9b1f83822d71ec98a6529",   // md5以后的原密码
    "newPassword":"e10adc3949ba59abbe56e057f20f883e"    // md5以后的新密码
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                  // 成功 0-成功 1-原密码校验不过
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    oldPassword        @NotNull     @Pattern(regexp = "\\w{32}")            // md5
    newPassword        @NotNull     @Pattern(regexp = "\\w{32}")            // md5
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import hashlib
import unittest

from www.api.webservice import webservice
from www.common.database import update
from www.common.excel import wsData


class modifyPassword(unittest.TestCase):

    UserShop = wsData('TmlShop')

    # S1.修改登录密码
    def test_modifyPwd_mod(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        modifyPwd = ws.modiyfPassword(self.UserShop.password, 'ModifyPwd')
        self.assertEqual(modifyPwd.model['success'], '0')
        modifyPwdOld = ws.login(self.UserShop.username, self.UserShop.password, 'null')
        self.assertEqual(modifyPwdOld.model['success'], '4')
        modifyPwdNew = ws.login(self.UserShop.username, 'ModifyPwd')
        self.assertEqual(modifyPwdNew.model['success'], '0')

    # S2.原密码错误
    def test_modifyPwd_pwdWrong(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        modifyPwd = ws.modiyfPassword('WorngPwd', 'ModifyPwd')
        self.assertEqual(modifyPwd.model['success'], '1')

    # S3.新旧密码相同——能够保存成功
    def test_modifyPwd_pwdSame(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        modifyPwd = ws.modiyfPassword(self.UserShop.password, self.UserShop.password)
        self.assertEqual(modifyPwd.model['success'], '0')


    # S4.token为空
    def test_modifyPwd_tokenNull(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        modifyPwd = ws.modiyfPassword(self.UserShop.password, 'ModifyPwd', '')
        self.assertEqual(modifyPwd.code, 100)

    # S5.token错误
    def test_modifyPwd_tokenWrong(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        modifyPwd = ws.modiyfPassword(self.UserShop.password, 'ModifyPwd', 'WrongToken')
        self.assertEqual(modifyPwd.code, 100)

    def tearDown(self):
        update('update dluser.dl_user set user_passwd= ? where user_id = ?', hashlib.md5(self.UserShop.password).hexdigest(), self.UserShop.userId)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(modifyPassword("test_modifyPwd_mod"))
    suite.addTest(modifyPassword("test_modifyPwd_pwdWrong"))
    suite.addTest(modifyPassword("test_modifyPwd_pwdSame"))
    suite.addTest(modifyPassword("test_modifyPwd_tokenNull"))
    suite.addTest(modifyPassword("test_modifyPwd_tokenWrong"))
    return suite