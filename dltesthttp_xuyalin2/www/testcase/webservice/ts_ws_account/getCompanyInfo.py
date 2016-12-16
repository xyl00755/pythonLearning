#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import *

"""
0288.获取企业信息
http://127.0.0.1:8280/mallws/mydl/account/getCompanyInfo.json
{
	"token":"123",
	"companyId":"company01"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                    // 0-成功 1-失败
	    "companyId":"company01",                           // 企业Id
		"companyName":"T01",                               // 企业名字
	    "userAcct":"testsun",                              // 用户帐户
		"terminalType":"名烟名酒店",                       // 终端店类型
	    "regDistrict":"CHNP035C345D2998",                  // 注册地址Code(预留)
		"regAreaName":"四川-成都-青羊"                     // 注册地址全名(预留)
	    "purchaseAreaCode":"CHNP035C345D2998",             // 采购地址Code(预留)
		"purchaseAreaName":"四川-成都-高新"                // 采购地址全名
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.account.GetCompanyInfoResponse"
    }
}
"""

class getCompanyInfo(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2=wsData('TmlShop2')

    #正确获取企业信息
    def test_getCompanyInfo(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getCompInfo=ws.getCompanyInfo(companyId=self.UserShop1.companyId)
        self.assertEqual(getCompInfo.model['success'],'0')
        self.assertGetCompanyInfoSuccess(getCompInfo)

    #获取其他用户的企业信息(已提交Bug5603)
    def test_getCompanyInfo_other(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getCompInfo=ws.getCompanyInfo(companyId=self.UserShop2.companyId)
        self.assertEqual(getCompInfo.model['success'], '1')

    #获取不存在的企业信息
    def test_getCompanyInfo_notExist(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getCompInfo=ws.getCompanyInfo(companyId='123456789')
        self.assertEqual(getCompInfo.model['success'], '1')

    #token为空获取企业信息
    def test_getCompanyInfo_nullToken(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getCompInfo=ws.getCompanyInfo(companyId=self.UserShop1.companyId,token='null')
        self.assertEqual(getCompInfo.model,None)
        self.assertEqual(getCompInfo.code,600)

    #token错误获取企业信息
    def test_getCompanyInfo_ErrorToken(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getCompInfo=ws.getCompanyInfo(companyId=self.UserShop1.companyId,token='123456789')
        self.assertEqual(getCompInfo.model,None)
        self.assertEqual(getCompInfo.code,100)




    #验证获取企业信息正确
    def assertGetCompanyInfoSuccess(self,companyInfo=None):
        self.assertEqual(companyInfo.model['companyId'],self.UserShop1.companyId)
        self.assertEqual(companyInfo.model['companyName'],self.UserShop1.fullName)
        self.assertEqual(companyInfo.model['userAcct'],self.UserShop1.username)
        self.assertEqual(companyInfo.model['terminalType'],self.UserShop1.shopType)
        self.assertEqual(companyInfo.model['regDistrict'],self.UserShop1.areaCode)
        self.assertEqual(companyInfo.model['purchaseAreaCode'],self.UserShop1.areaCode)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getCompanyInfo("test_getCompanyInfo"))
    suite.addTest(getCompanyInfo("test_getCompanyInfo_other"))
    suite.addTest(getCompanyInfo("test_getCompanyInfo_notExist"))
    suite.addTest(getCompanyInfo("test_getCompanyInfo_ErrorToken"))
    suite.addTest(getCompanyInfo("test_getCompanyInfo_nullToken"))
    return suite