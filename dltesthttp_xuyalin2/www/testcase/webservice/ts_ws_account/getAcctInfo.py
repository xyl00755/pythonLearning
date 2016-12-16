#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import *

"""
0289.获取账户信息
http://127.0.0.1:8280/mallws/mydl/account/getAcctInfo.json
{
	"token":"123",
	"userId":"user01",
    "userAcct":"testliqi"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 0-成功 1-失败
	    "userId":"user01"                                   // 用户Id
		"userAcct":"testsun",                               // 帐号
	    "userName":"张三"                                   // 姓名
		"position":"经理"                                   // 职位
		"email":"test@danlu.com",                           // Email
		"tel":"13800138000",                                // 手机号
		"telStatus":"1"                                     // 0-激活 1-未激活

    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.account.GetAcctInfoResponse"
    }
}

"""

class getAcctInfo(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    #正确获取账号信息
    def test_getAcctInfo(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAccountInfo=ws.getAcctInfo(userId=self.UserShop1.userId,userAcct=self.UserShop1.username)
        self.assertEqual(getAccountInfo.model['success'],'0')
        self.assertGetAccInfoSuccess(getAccountInfo)

    #userId与userAcc不一致获取账号信息(已提交bug5607)
    def test_getAcctInfo_inconsistent(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAccountInfo=ws.getAcctInfo(userId=self.UserShop1.userId,userAcct=self.UserShop2.username)
        self.assertEqual(getAccountInfo.model['success'], '1')

    #获取其他用户的账号信息
    def test_getAcctInfo_other(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getAccountInfo=ws.getAcctInfo(userId=self.UserShop1.userId,userAcct=self.UserShop1.username)
        self.assertEqual(getAccountInfo.model['success'],'0')
        self.assertGetAccInfoSuccess(getAccountInfo)

    #获取不存在的userId用户账号信息
    def test_getAcctInfo_notExistUserId(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAccountInfo=ws.getAcctInfo(userId='123456789',userAcct=self.UserShop1.username)
        self.assertEqual(getAccountInfo.model['success'],'1')

    #获取不存在的userAccount用户账号信息
    def test_getAcctInfo_notExistUserAcct(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAccountInfo=ws.getAcctInfo(userId=self.UserShop1.userId,userAcct='123456789')
        self.assertEqual(getAccountInfo.model['success'],'1')



    #验证获取账号信息成功
    def assertGetAccInfoSuccess(self,accountInfo):
        self.assertEqual(accountInfo.model['userId'],self.UserShop1.userId)
        self.assertEqual(accountInfo.model['userAcct'],self.UserShop1.username)
        self.assertEqual(accountInfo.model['userName'],self.UserShop1.userName)
        self.assertEqual(accountInfo.model['position'],self.UserShop1.userPosition)
        self.assertEqual(accountInfo.model['email'],self.UserShop1.userEmail)
        self.assertEqual(accountInfo.model['tel'],self.UserShop1.leaderPhone)
        self.assertEqual(accountInfo.model['telStatus'],self.UserShop1.telStatus)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getAcctInfo("test_getAcctInfo"))
    #suite.addTest(getAcctInfo("test_getAcctInfo_inconsistent"))
    suite.addTest(getAcctInfo("test_getAcctInfo_other"))
    suite.addTest(getAcctInfo("test_getAcctInfo_notExistUserId"))
    suite.addTest(getAcctInfo("test_getAcctInfo_notExistUserAcct"))
    return suite