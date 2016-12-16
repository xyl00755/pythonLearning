#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
url:
http:dealerPayRate/payRate.html
request:null
response:
 {
    "data": {
        "payRate": 3000
    },
    "msg": "",
    "status": 0
  }
"""

class getPayRate(unittest.TestCase):

    UserShop=wsData('DealMager')

    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    def setUp(self):
        update('update dlpay.dl_payment_dealer_pay_rate set rate = ? where company_id = ?',self.UserShop.defaultPayRate,self.UserShop.companyId)

    #获取默认最高支付比
    def test_getDefaultPayRate(self):
        getPayRateInfo = self.dlservice.getPayRate(self.s)
        self.assertEqual(getPayRateInfo['status'],0)
        self.assertEqual(getPayRateInfo['data']['payRate'],int(self.UserShop.defaultPayRate))

    #修改符合要求的最高支付比，获取为修改后的值
    def test_getCorrectPayRate(self):
        self.dlservice.setPayRate(self.s,5000)
        getPayRateInfo = self.dlservice.getPayRate(self.s)
        self.assertEqual(getPayRateInfo['data']['payRate'],5000)

    #用例执行完成后清理数据库
    def tearDown(self):
        update('update dlpay.dl_payment_dealer_pay_rate set rate = ? where company_id = ?',self.UserShop.defaultPayRate,self.UserShop.companyId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getPayRate("test_getDefaultPayRate"))
    suite.addTest(getPayRate("test_getCorrectPayRate"))
    return suite
