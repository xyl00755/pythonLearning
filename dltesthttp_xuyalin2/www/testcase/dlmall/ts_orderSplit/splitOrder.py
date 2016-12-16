#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *
from www.operation.order import createOrder
from www.operation.order import cleanOrders

"""
url:
http://127.0.0.1:8280/orderSplit/splitOrder.html?orderNo=24324354654656
request:orderNo
response:
{
    "status":0,
    "msg":"",
    "data":{
        "orderNo": "234353454657656",
        "orderAmt": 5000,
        "buyerName": "XX终端店",
        "maxTimes": 3
    }
}
"""

class splitOrder(unittest.TestCase):

    UserShop=wsData('DealMager2')
    TmlShop=wsData('TmlShop')
    Merch = wsData('Merch1')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    def setUp(self):
        self.tearDown()

    #成功获取待拆分信息
    def test_splitOrder_success(self):
        order = createOrder(self.TmlShop, self.Merch)
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='4000',maxTimes='3')
        splitOrderInfo=self.dlservice.splitOrder(self.s,orderNo=order.orderNo)
        self.assertEqual(splitOrderInfo['status'],0)
        orderAmt = select_one('select total_amount from dlorder.dl_order_orderdetail where order_no = ?', order.orderNo)
        buyerName = select_one('select buyer_name from dlorder.dl_order_orderdetail where order_no = ?',order.orderNo)
        maxTimes = select_one('select max_times from dlcompany.dl_payment_split_info where company_id = ?', self.UserShop.companyId)
        cleanOrders(orderNo=order.orderNo)
        self.assertEqual(splitOrderInfo['data']['orderNo'],order.orderNo)
        self.assertEqual(splitOrderInfo['data']['orderAmt'],orderAmt['total_amount'])
        self.assertEqual(splitOrderInfo['data']['buyerName'],buyerName['buyer_name'])
        self.assertEqual(splitOrderInfo['data']['maxTimes'],maxTimes['max_times'])


    #卖家未设置订单拆分开关
    def test_splitOrder_nonsupport(self):
        splitOrderInfo=self.dlservice.splitOrder(self.s,orderNo=self.TmlShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(splitOrderInfo['status'],1)
        self.assertEqual(splitOrderInfo['data'],None)

    #未传入订单号
    def test_splitOrder_orderNoNull(self):
        splitOrderInfo=self.dlservice.splitOrder(self.s)
        self.assertEqual(splitOrderInfo['status'],2)
        self.assertEqual(splitOrderInfo['msg'],u'未传入订单号')

    #传入不存在的订单号
    def test_splitOrder_orderNoNotExist(self):
        splitOrderInfo=self.dlservice.splitOrder(self.s,orderNo='12365478542')
        self.assertEqual(splitOrderInfo['status'],1)
        self.assertEqual(splitOrderInfo['data'],None)

    #获取订单拆分信息是否正确的验证方法
    def assertGetNormalSuccess(self,splitOrderInfo):
        orderAmt = select_one('select total_amount from dlorder.dl_order_orderdetail where order_no = ?', self.TmlShop.orderCodWaitDeliver.orderNo)
        buyerName = select_one('select buyer_name from dlorder.dl_order_orderdetail where order_no = ?',self.TmlShop.orderCodWaitDeliver.orderNo)
        maxTimes = select_one('select max_times from dlcompany.dl_payment_split_info where company_id = ?', self.UserShop.companyId)
        self.assertEqual(splitOrderInfo['data']['orderNo'],self.TmlShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(splitOrderInfo['data']['orderAmt'],orderAmt['total_amount'])
        self.assertEqual(splitOrderInfo['data']['buyerName'],buyerName['buyer_name'])
        self.assertEqual(splitOrderInfo['data']['maxTimes'],maxTimes['max_times'])

    #用例执行完成后清理数据库
    def tearDown(self):
        update('delete from dlcompany.dl_payment_split_info where company_id = ?', self.UserShop.companyId)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(splitOrder("test_splitOrder_success"))
    suite.addTest(splitOrder("test_splitOrder_nonsupport"))
    suite.addTest(splitOrder("test_splitOrder_orderNoNull"))
    suite.addTest(splitOrder("test_splitOrder_orderNoNotExist"))
    return suite
