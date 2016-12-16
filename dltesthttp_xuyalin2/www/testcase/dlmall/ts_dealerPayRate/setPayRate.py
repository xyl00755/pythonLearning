#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
url:
http://127.0.0.1:8280/dealerPayRate/payRate.html
request:payRate
response:
 {
    "data": {
        "payRate": 3000
    },
    "msg": "",
    "status": 0
  }
"""

class setPayRate(unittest.TestCase):

    UserShop=wsData('DealMager')

    def setUp(self):
        update('update dlpay.dl_payment_dealer_pay_rate set rate = ? where company_id = ?',self.UserShop.defaultPayRate,self.UserShop.companyId)

    #设置符合要求的新的最高支付比
    def test_setPayRate_true(self):
        dlservice = dlmall()
        s = dlservice.login(self.UserShop.username,self.UserShop.password)
        setPayRateResult = dlservice.setPayRate(s,5000)
        self.assertEqual(setPayRateResult['status'],0)
        self.assertEqual(setPayRateResult['data']['payRate'],5000)

    #设置不符合要求的最高支付比(非整数)
    def test_setPayRate_wrong1(self):
        dlservice = dlmall()
        s = dlservice.login(self.UserShop.username,self.UserShop.password)
        setPayRateResult = dlservice.setPayRate(s,5050)
        self.assertEqual(setPayRateResult['status'],0)
        self.assertEqual(setPayRateResult['data']['payRate'],3000)

    #设置不符合要求的最高支付比(汉字)
    def test_setPayRate_wrong2(self):
        dlservice = dlmall()
        s = dlservice.login(self.UserShop.username,self.UserShop.password)
        setPayRateResult = dlservice.setPayRate(s,"测试")
        self.assertEqual(setPayRateResult['status'],1)
        self.assertEqual(setPayRateResult['data']['payRate'],3000)

    #设置不符合要求的最高支付比(字母)
    def test_setPayRate_wrong3(self):
        dlservice = dlmall()
        s = dlservice.login(self.UserShop.username,self.UserShop.password)
        setPayRateResult = dlservice.setPayRate(s,"a")
        self.assertEqual(setPayRateResult['status'],1)
        self.assertEqual(setPayRateResult['data']['payRate'],3000)

    #设置不符合要求的最高支付比(特殊字符)
    def test_setPayRate_wrong4(self):
        dlservice = dlmall()
        s = dlservice.login(self.UserShop.username,self.UserShop.password)
        setPayRateResult = dlservice.setPayRate(s,"!")
        self.assertEqual(setPayRateResult['status'],1)
        self.assertEqual(setPayRateResult['data']['payRate'],3000)

    #用例执行完成后清理数据库
    def tearDown(self):
        update('update dlpay.dl_payment_dealer_pay_rate set rate = ? where company_id = ?',self.UserShop.defaultPayRate,self.UserShop.companyId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(setPayRate("test_setPayRate_true"))
    # suite.addTest(setPayRate("test_setPayRate_wrong1"))
    # suite.addTest(setPayRate("test_setPayRate_wrong2"))
    # suite.addTest(setPayRate("test_setPayRate_wrong3"))
    # suite.addTest(setPayRate("test_setPayRate_wrong4"))
    return suite