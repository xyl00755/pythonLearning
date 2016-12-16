#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0181.订单发货
http://127.0.0.1:8280/mallws/orders/oper/deliver.json
{
    "token":"123",                      // 必须
    "orderNo":"123123"                  // 必须 订单号
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                      // 0-成功 1-已经发过货 2-交易处于异常状态
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import *
from www.common.excel import wsData
from www.operation.order import createOrder


class deliver(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    DealMgr = wsData('DealMager')
    DealMgr2 = wsData('DealMager2')
    DealSaler = wsData('DealSaler')
    DealBuyer = wsData('DealBuyer')
    UserDealSed = wsData('DealSeder')
    UserDealFin = wsData('DealFiner')
    Merch1 = wsData('Merch1')

    # S1.货到付款订单发货
    def test_deliver_cod(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        deliverOrder = ws.deliver(orderNo=order.orderNo)
        self.assertEqual(deliverOrder.model['success'], '0')

    # S2.在线支付订单发货

    # S3.重复发货
    def test_deliver_codAgain(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        deliverOrder = ws.deliver(orderNo=order.orderNo)
        self.assertEqual(deliverOrder.model['success'], '0')
        deliverOrderAgain = ws.deliver(orderNo=order.orderNo)
        self.assertEqual(deliverOrderAgain.model['success'], '1')

    # S4.发不存在的订单
    def test_deliver_notExist(self):
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        deliverOrder = ws.deliver(orderNo='12345678901234')
        self.assertEqual(deliverOrder.code, 500)

    # S5.发其他用户的订单
    def test_deliver_other(self):
        ws = webservice()
        ws.login(self.DealMgr2.username, self.DealMgr2.password)
        deliverOrder = ws.deliver(orderNo=self.UserShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(deliverOrder.model['success'], '1')

    # S6.token错误或不存在发货
    def test_deliver_token(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealMgr2.username, self.DealMgr2.password)
        deliverOrder = ws.deliver(orderNo=order.orderNo, token='null')
        self.assertEqual(deliverOrder.code, 600)
        deliverOrder = ws.deliver(orderNo=order.orderNo, token='ErrorToken')
        self.assertEqual(deliverOrder.code, 100)

    # S7.销售员发货
    def test_deliver_saler(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealSaler.username, self.DealSaler.password)
        deliverOrder = ws.deliver(orderNo=order.orderNo)
        self.assertEqual(deliverOrder.model['success'], '0')

    # S8.无权限用户发货
    def test_deliver_noRight(self):
        ws = webservice()
        ws.login(self.DealBuyer.username, self.DealBuyer.password)
        deliverOrder = ws.deliver(orderNo=self.UserShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(deliverOrder.code, 300)
        ws.login(self.UserDealSed.username, self.UserDealSed.password)
        deliverOrder = ws.deliver(orderNo=self.UserShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(deliverOrder.code, 300)
        ws.login(self.UserDealFin.username, self.UserDealFin.password)
        deliverOrder = ws.deliver(orderNo=self.UserShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(deliverOrder.code, 300)

    # S9.不在待发货状态订单发货
    def test_deliver_errorStatus(self):
        #对待付款订单发货
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        deliverOrder = ws.deliver(orderNo=self.UserShop.orderOnlineWaitPay.orderNo)
        self.assertEqual(deliverOrder.model['success'], '1')

        #对交易完成订单发货
        deliverOrder = ws.deliver(orderNo=self.UserShop.orderCodComplete.orderNo)
        self.assertEqual(deliverOrder.model['success'], '1')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(deliver("test_deliver_cod"))
    suite.addTest(deliver("test_deliver_codAgain"))
    suite.addTest(deliver("test_deliver_notExist"))
    #suite.addTest(deliver("test_deliver_other"))
    suite.addTest(deliver("test_deliver_token"))
    suite.addTest(deliver("test_deliver_saler"))
    suite.addTest(deliver("test_deliver_noRight"))
    suite.addTest(deliver("test_deliver_errorStatus"))
    return suite