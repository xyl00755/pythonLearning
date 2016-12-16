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
http://127.0.0.1:8280/orderSplit/doSplitOrder.html
request:
 {
    "orderNo": "2324353454645",
    "splitItems": "4000,3000"
  }
response:
  {
    "status": 0,
    "msg": "保存成功",
    "data":{
        "orderNo": "2324353454645",
        "splitOrders": [
            {"payOrderNo":"3435446456546","payAmt":4000},
            {"payOrderNo":"2323453545466","payAmt":3000}
         ]
    }
  }
"""
class doSplitOrder(unittest.TestCase):

    UserShop=wsData('DealMager2')
    TmlShop=wsData('TmlShop')
    Merch = wsData('Merch1')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    def setUp(self):
        self.tearDown()

    #保存经销商拆分的订单信息成功
    def test_doSplitOrder_success(self):
        #创建订单
        order = createOrder(self.TmlShop, self.Merch)
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='4000',maxTimes='3')
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo=order.orderNo,splitItems='4000,4000,4000')
        self.assertEqual(doSplitOrderResult['status'],0)
        # payNo = select_one('select pay_no from dlorder.dl_order_orderinfo where order_no = ?', order.orderNo)
        payOrderNo=select('select pay_order_no from dlpay.dl_payment_split_order where pay_no = ?',order.paymentNo)
        payOrderNos=[]
        for item in payOrderNo:
            payOrderNos.append(item['pay_order_no'])
        for i in range (2):
             self.assertEqual(doSplitOrderResult['data']['splitOrders'][i]['payOrderNo'] in payOrderNos,True)
        #删除拆单信息
        update('delete from dlpay.dl_payment_split_order where pay_no = ?',order.paymentNo)
        #清楚清单
        cleanOrders(orderNo=order.orderNo)


    #拆分支付单金额总和不等于订单金额，订单总额为12000
    def test_doSplitOrder_payAmtError(self):
        order = createOrder(self.TmlShop, self.Merch)
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='4000',maxTimes='3')
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo=order.orderNo,splitItems='4000,4000,3000')
        cleanOrders(orderNo=order.orderNo)
        self.assertEqual(doSplitOrderResult['status'],2)
        self.assertEqual(doSplitOrderResult['msg'],u'保存订单拆分信息失败')


    #拆分支付单个数大于最多支付单数，经销商设置最多支付次数为2，实际支付次数为3
    def test_doSplitOrder_maxTimesfailed(self):
        order = createOrder(self.TmlShop, self.Merch)
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='4000',maxTimes='2')
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo=order.orderNo,splitItems='4000,4000,4000')
        cleanOrders(orderNo=order.orderNo)
        self.assertEqual(doSplitOrderResult['status'],2)

    #卖家未设置订单拆分开关
    def test_doSplitOrder_nonsupport(self):
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo=self.TmlShop.orderCodWaitDeliver.orderNo,splitItems='4000,4000,4000')
        self.assertEqual(doSplitOrderResult['status'],1)
        self.assertEqual(doSplitOrderResult['msg'],u'订单不能拆分')

    #未传入订单号
    def test_doSplitOrder_orderNoNull(self):
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,splitItems='4000,4000,4000')
        self.assertEqual(doSplitOrderResult['status'],1)
        self.assertEqual(doSplitOrderResult['msg'],u'订单不能拆分')

    #传入的订单号不存在
    def test_doSplitOrder_orderNoNotExist(self):
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo='3698754215',splitItems='4000,4000,4000')
        self.assertEqual(doSplitOrderResult['status'],1)
        self.assertEqual(doSplitOrderResult['msg'],u'订单不能拆分')

    #未传入支付单金额
    def test_doSplitOrder_splitItemsNull(self):
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo=self.TmlShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(doSplitOrderResult['status'],1)
        self.assertEqual(doSplitOrderResult['msg'],u'订单不能拆分')

    #传入的支付订单金额中包含非数字
    def test_doSplitOrder_splitItemsError(self):
        doSplitOrderResult=self.dlservice.doSplitOrder(self.s,orderNo=self.TmlShop.orderCodWaitDeliver.orderNo,splitItems='dfadaf,50000000,20000000')
        self.assertEqual(doSplitOrderResult['status'],1)
        self.assertEqual(doSplitOrderResult['msg'],u'订单不能拆分')

     #用例执行完成后清理数据库
    def tearDown(self):
        update('delete from dlcompany.dl_payment_split_info where company_id = ?', self.UserShop.companyId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(doSplitOrder("test_doSplitOrder_success"))
    suite.addTest(doSplitOrder("test_doSplitOrder_payAmtError"))
    suite.addTest(doSplitOrder("test_doSplitOrder_maxTimesfailed"))
    suite.addTest(doSplitOrder("test_doSplitOrder_nonsupport"))
    suite.addTest(doSplitOrder("test_doSplitOrder_orderNoNull"))
    suite.addTest(doSplitOrder("test_doSplitOrder_orderNoNotExist"))
    suite.addTest(doSplitOrder("test_doSplitOrder_splitItemsNull"))
    suite.addTest(doSplitOrder("test_doSplitOrder_splitItemsError"))
    return suite