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
http://127.0.0.1:8280/orderSplit/getSplitOrderInfo.html?orderNo=243534545465
request:orderNo
response:
    {
        "status":0,
        "msg":"",
        "data":{
            "splitOrders":[
                {"payOrderNo":"3435446456546","payAmt":4000,"payStatus":"00"},
                {"payOrderNo":"2323453545466","payAmt":3000,"payStatus":"03"}
            ]
        }
    }
"""
class getSplitOrderInfo(unittest.TestCase):

    UserShop=wsData('DealMager2')
    TmlShop=wsData('TmlShop')
    Merch = wsData('Merch1')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    def setUp(self):
        self.tearDown()

    #成功获取订单拆分信息
    def test_getSplitOrderInfo_success(self):
        #创建订单
        order = createOrder(self.TmlShop, self.Merch)
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='4000',maxTimes='3')
        self.dlservice.doSplitOrder(self.s,orderNo=order.orderNo,splitItems='4000,4000,4000')
        getSplitOrderResult=self.dlservice.getSplitOrderInfo(self.s,orderNo=order.orderNo)
        self.assertEqual(getSplitOrderResult['status'],0)
        payOrderNo=select('select pay_order_no from dlpay.dl_payment_split_order where pay_no = ?',order.paymentNo)
        payOrderNos=[]
        for item in payOrderNo:
            payOrderNos.append(item['pay_order_no'])
        for i in range (2):
             self.assertEqual(getSplitOrderResult['data']['splitOrders'][i]['payOrderNo'] in payOrderNos,True)
        #删除拆单信息
        update('delete from dlpay.dl_payment_split_order where pay_no = ?',order.paymentNo)
        #清楚清单
        cleanOrders(orderNo=order.orderNo)

    #不存在订单拆分信息
    def test_getSplitOrderInfo_spiltInfoNotExist(self):
        getSplitOrderResult=self.dlservice.getSplitOrderInfo(self.s,orderNo=self.TmlShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(getSplitOrderResult['status'],1)
        self.assertEqual(getSplitOrderResult['msg'],u'获取拆分支付单失败')

    #传入小订单号
    def test_getSplitOrderInfo_payOrderNo(self):
        order = createOrder(self.TmlShop, self.Merch)
        self.dlservice.saveOrderSplitInfo(self.s,status='1',minAmount='4000',maxTimes='3')
        self.dlservice.doSplitOrder(self.s,orderNo=order.orderNo,splitItems='4000,4000,4000')
        payOrderNo=select('select pay_order_no from dlpay.dl_payment_split_order where pay_no = ?',order.paymentNo)
        getSplitOrderResult=self.dlservice.getSplitOrderInfo(self.s,orderNo=payOrderNo[0]['pay_order_no'])
        cleanOrders(orderNo=order.orderNo)
        self.assertEqual(getSplitOrderResult['status'],1)
        self.assertEqual(getSplitOrderResult['msg'],u'获取拆分支付单失败')

    # 未传入订单号
    def test_getSplitOrderInfo_orderNoNull(self):
        getSplitOrderResult=self.dlservice.getSplitOrderInfo(self.s)
        self.assertEqual(getSplitOrderResult['status'],1)
        self.assertEqual(getSplitOrderResult['msg'],u'获取拆分支付单失败')

    #传入的订单号不存在
    def test_getSplitOrderInfo_orderNoNotExist(self):
        getSplitOrderResult=self.dlservice.getSplitOrderInfo(self.s,orderNo='564387924')
        self.assertEqual(getSplitOrderResult['status'],1)
        self.assertEqual(getSplitOrderResult['msg'],u'获取拆分支付单失败')

    #用例执行完成后清理数据库
    def tearDown(self):
        update('delete from dlcompany.dl_payment_split_info where company_id = ?', self.UserShop.companyId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getSplitOrderInfo("test_getSplitOrderInfo_success"))
    suite.addTest(getSplitOrderInfo("test_getSplitOrderInfo_spiltInfoNotExist"))
    suite.addTest(getSplitOrderInfo("test_getSplitOrderInfo_orderNoNull"))
    suite.addTest(getSplitOrderInfo("test_getSplitOrderInfo_orderNoNotExist"))
    suite.addTest(getSplitOrderInfo("test_getSplitOrderInfo_payOrderNo"))
    return suite