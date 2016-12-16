#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
url:
http://127.0.0.1:8280/businessInfoModify/saveOrderSplitInfo.html
request:
{
    "status":"1",   //状态（0-不支持，1-支持）
    "minAmount":"5000",  //	多次支付订单最低金额，单位：分（正整数）
    "maxTimes":"3"  //最多支付次数（正整数）
}
response:
{
    "status":1,
    "msg":"",
    "data":{}
}
"""

class saveOrderSplitInfo(unittest.TestCase):

    UserShop=wsData('DealMager2')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    def setUp(self):
        self.tearDown()

    #新增订单支付拆分信息
    def test_saveOrderSplitInfo_add(self):
        splitInfo=self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='3000',maxTimes='3')
        self.assertEqual(splitInfo['status'],'1')

    #修改订单支付拆分信息
    def test_saveOrderSplitInfo_modify(self):
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='3000',maxTimes='3')
        splitInfo=self.dlservice.saveOrderSplitInfo(self.s,status='0',minAmount='4000',maxTimes='2')
        self.assertEqual(splitInfo['status'],'1')

    #最多支付次数格式不正确
    def test_saveOrderSplitInfo_minAmountformatError(self):
        splitInfo=self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='hhhhh',maxTimes='3')
        self.assertEqual(splitInfo['status'],'3')

    #最低支付金额格式不正确
    def test_saveOrderSplitInfo_maxTimesformatError(self):
        splitInfo=self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='3000',maxTimes='hhhhh')
        self.assertEqual(splitInfo['status'],'2')

    #最多支付次数为空
    def test_saveOrderSplitInfo_minAmountNull(self):
        splitInfo=self.dlservice.saveOrderSplitInfo(self.s,status='1',maxTimes='3')
        self.assertEqual(splitInfo['status'],'3')

    #最低支付金额为空
    def test_saveOrderSplitInfo_maxTimesNull(self):
        splitInfo=self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='3000')
        self.assertEqual(splitInfo['status'],'2')

    #用例执行完成后清理数据库
    def tearDown(self):
        update('delete from dlcompany.dl_payment_split_info where company_id = ?', self.UserShop.companyId)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(saveOrderSplitInfo("test_saveOrderSplitInfo_add"))
    suite.addTest(saveOrderSplitInfo("test_saveOrderSplitInfo_modify"))
    suite.addTest(saveOrderSplitInfo("test_saveOrderSplitInfo_minAmountformatError"))
    suite.addTest(saveOrderSplitInfo("test_saveOrderSplitInfo_maxTimesformatError"))
    suite.addTest(saveOrderSplitInfo("test_saveOrderSplitInfo_minAmountNull"))
    suite.addTest(saveOrderSplitInfo("test_saveOrderSplitInfo_maxTimesNull"))
    return suite