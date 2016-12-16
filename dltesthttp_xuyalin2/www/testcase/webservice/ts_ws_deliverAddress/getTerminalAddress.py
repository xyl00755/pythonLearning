#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import *

"""
0215.获取终端店地址
http://127.0.0.1:8880/mallws/mydl/deliverAddress/getTerminalAddress.json
{
    "token": "2e6dfb67ad64449dadf1598fb9fc8378",                     // 必须
    "terminalCustomerId": "b3ab3b01308d4be09df1ce8715f70405"         // 终端店id
}

{
  "code": 200,
  "description": "执行成功!",
  "model": {
    "success": "0",                                                 // 成功 0-成功
    "terminalAreaProvinceCode": "CHNP013",                          // 终端店地址-省code
    "terminalAreaProvinceValue": "福建",                            // 终端店地址-省name
    "terminalAreaCityCode": "CHNP013C115",                          // 终端店地址-市code
    "terminalAreaCityValue": "福州市",                              // 终端店地址-市name
    "terminalAreaDistrictCode": "CHNP013C115D1079",                 // 终端店地址-区县code
    "terminalAreaDistrictValue": "鼓楼区"                           // 终端店地址-区县name
  },
  "metadata": {
    "type": 0,
    "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.deliveraddr.GetTerminalAddressReponse"
  }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class getTerminalAddress(unittest.TestCase):

    UserShop1=wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')

    # S1.获取终端店注册地址
    def test_getTerminalAddress(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        terminal=ws.login(self.UserShop1.username,self.UserShop1.password)
        getTerAddresss=ws.getTerminalAddress(terminalCustomerId=terminal.model['userId'])
        self.assertEqual(getTerAddresss.model['success'],'0')
        self.assertTerminalAddressSuccess(getTerAddresss)


    # S2.userid为空，获取终端店地址
    def test_getTerminalAddress_userId_null(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getTerAddresss=ws.getTerminalAddress(terminalCustomerId='')
        self.assertEqual(getTerAddresss.code,500)
        self.assertEqual(getTerAddresss.model,None)

    # S3.userid不存在，获取终端店地址
    def test_getTerminalAddress_notExistUserId(self):
         ws=webservice()
         ws.login(self.UserShop1.username,self.UserShop1.password)
         getTerAddresss=ws.getTerminalAddress(terminalCustomerId='123456789')
         self.assertEqual(getTerAddresss.code,500)
         self.assertEqual(getTerAddresss.model,None)

    # S4.无token值，获取终端店地址
    def test_getTerminalAddress_noToken(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        terminal=ws.login(self.UserShop1.username,self.UserShop1.password)
        getTerAddresss=ws.getTerminalAddress(terminalCustomerId=terminal.model['userId'],token='null')
        self.assertEqual(getTerAddresss.model['success'],'0')
        self.assertTerminalAddressSuccess(getTerAddresss)

    # 验证获取终端店地址正确
    def assertTerminalAddressSuccess(self,terminalAddress):
        self.assertEqual(terminalAddress.model['terminalAreaProvinceValue'],self.UserShop1.localProvince)
        self.assertEqual(terminalAddress.model['terminalAreaCityValue'],self.UserShop1.localCity)
        self.assertEqual(terminalAddress.model['terminalAreaDistrictValue'],self.UserShop1.localCountry)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getTerminalAddress("test_getTerminalAddress"))
    suite.addTest(getTerminalAddress("test_getTerminalAddress_userId_null"))
    suite.addTest(getTerminalAddress("test_getTerminalAddress_notExistUserId"))
    suite.addTest(getTerminalAddress("test_getTerminalAddress_noToken"))
    return suite