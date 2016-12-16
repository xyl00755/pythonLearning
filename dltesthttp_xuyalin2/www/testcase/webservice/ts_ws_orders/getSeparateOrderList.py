#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GJ04.查看已拆分订单（新增）
http://127.0.0.1:8080/mallws/orders/getSeparateOrderList.json
{

    "token":"123",                          // 必须
    "orderNo":"123123123"                   // 必须 订单号
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                     // 成功 0-成功 1-不成功
        "paymentInfoList":[
            {
                "separatePaymentNo":"201510021725-A-01",    // 拆分后的支付单号
                "separateOrderAmount":"50000"               // 拆分后的子订单号对应的支付金额（单位：分）
                "payStatus":"01"                           //  支付状态(00-未支付，01-已支付)
            }
        ]
     },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.CheckSeparateOrderListsResponse"
    }
}
"""

import unittest

from www.api.webservice import *
from www.common.excel import *

class getSeparateOrderList(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')

    wsUserShop = webservice()
    wsUserShop.login(UserShop.username, UserShop.password)
    wsUserShop2 = webservice()
    wsUserShop2.login(UserShop2.username, UserShop2.password)

    # S1.查看拆分订单(待发货)
    def test_getSeparateOrderList_getWaitDeliver(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo=self.UserShop.orderCodWaitDeliverSeparat.orderNo)
        self.assertEqual(orderList.model['success'], '0')
        self.assertEqual(orderList.model['paymentInfoList'], self.UserShop.orderCodWaitDeliverSeparatSub)


    # S2.查看拆分订单（待收货）
    def test_getSeparateOrderList_getWaitReceive(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo=self.UserShop.orderCodWaitReceiveSeparat.orderNo)
        self.assertEqual(orderList.model['success'], '0')
        self.assertEqual(orderList.model['paymentInfoList'], self.UserShop.orderCodWaitReceiveSeparatSub)

    # S3.查看拆分订单（支付中）
    def test_getSeparateOrderList_getPaying(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo=self.UserShop.orderCodPayingSeparat.orderNo)
        self.assertEqual(orderList.model['success'], '0')
        self.assertEqual(orderList.model['paymentInfoList'], self.UserShop.orderCodPayingSeparatSub)

    # S4.查看拆分订单（交易完成）
    def test_getSeparateOrderList_getComplete(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo=self.UserShop.orderCodCompleteSeparat.orderNo)
        self.assertEqual(orderList.model['success'], '0')
        self.assertEqual(orderList.model['paymentInfoList'], self.UserShop.orderCodCompleteSeparatSub)

    # S5.查看拆分订单（已取消）
    def test_getSeparateOrderList_getCancel(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo=self.UserShop.orderCodCancelSeparat.orderNo)
        self.assertEqual(orderList.model['success'], '0')
        self.assertEqual(orderList.model['paymentInfoList'], self.UserShop.orderCodCancelSeparatSub)

    # S6.查看其他人的拆分订单
    def test_getSeparateOrderList_other(self):
        orderList = self.wsUserShop2.getSeparateOrderList(orderNo=self.UserShop.orderCodWaitReceive.orderNo)
        self.assertEqual(orderList.model['success'], '1')

    # S7.查看未拆分订单
    def test_getSeparateOrderList_noSeparate(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo=self.UserShop.orderCodWaitReceive.orderNo)
        self.assertEqual(orderList.model['success'], '1')

    # S8.查看不存在订单
    def test_getSeparateOrderList_notExist(self):
        orderList = self.wsUserShop.getSeparateOrderList(orderNo='notExist')
        self.assertEqual(orderList.model['success'], '1')





def suite():
    suite=unittest.TestSuite()
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_getWaitDeliver'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_getWaitReceive'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_getPaying'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_getComplete'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_getCancel'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_other'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_noSeparate'))
    suite.addTest(getSeparateOrderList('test_getSeparateOrderList_notExist'))
    return suite