#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GJ05.请求拆分订单（新增）
http://127.0.0.1:8080/mallws/orders/preSeparateOrder.json
{
    "token":"123",                          // 必须
    "orderNo":"123123123",                  // 必须 订单号
}
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "orderNo":"123123123",              // 订单号
        "orderAmount":"50000",              // 订单金额
        "success": "0",                     // 成功 0-成功  1-不成功
        "separateOrderTimes":"7",           // 订单可以拆分次数  如果不能拆分，则为0
        "buyerName":"123",                  // 买家名

     },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.PreSeparateOrderResponse"
    }

}
"""

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

class preSeparateOrder(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    DealMager2 = wsData('DealMager2')


    wsUserShop = webservice()
    wsUserShop.login(UserShop.username, UserShop.password)
    wsDealMager = webservice()
    wsDealMager.login(DealMager.username, DealMager.password)
    wsDealMager2 = webservice()
    wsDealMager2.login(DealMager2.username, DealMager2.password)

    # S1.货到付款待发货请求拆分
    def test_preSeparateOrder_codWaitDeliver(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(sepOrder.model['success'], '0')
        self.assertPreSepOrder(sepOrder, self.UserShop.orderCodWaitDeliver, self.UserShop, self.DealMager)

    # S2.货到付款待收货订单请求拆分
    def test_preSeparateOrder_codWaitReceive(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.UserShop.orderCodWaitReceive.orderNo)
        self.assertEqual(sepOrder.model['success'], '0')
        self.assertPreSepOrder(sepOrder, self.UserShop.orderCodWaitReceive, self.UserShop, self.DealMager)

    # S3.货到付款交易完成订单请求拆分
    def test_preSeparateOrder_codWaitComplete(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.UserShop.orderCodComplete.orderNo)
        self.assertEqual(sepOrder.model['success'], '0')
        self.assertPreSepOrder(sepOrder, self.UserShop.orderCodComplete, self.UserShop, self.DealMager)

    # S4.货到付款交易取消订单请求拆分
    def test_preSeparateOrder_codWaitCancel(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.UserShop.orderCodCancel.orderNo)
        self.assertEqual(sepOrder.model['success'], '0')
        self.assertPreSepOrder(sepOrder, self.UserShop.orderCodCancel, self.UserShop, self.DealMager)

    # S5.在线支付待付款订单请求拆分
    def test_preSeparateOrder_onlineWaitPay(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.UserShop.orderOnlineWaitPay.orderNo)
        self.assertEqual(sepOrder.model['success'], '1')

    # S6.不允许拆单经销商获取订单拆分请求
    def test_preSeparateOrder_null(self):
        sepOrder = self.wsDealMager2.preSeparateOrder(orderNo=self.DealMager2.orderNo)
        self.assertEqual(sepOrder.model['success'], '1')

    # S7.金额未达到拆分要求获取订单拆分请求
    def test_preSeparateOrder_lessPrice(self):
        update('update dlcompany.dl_payment_split_info set min_amount = ? where company_id = ?', '50000', self.DealMager.companyId)
        sepOrder = self.wsDealMager2.preSeparateOrder(orderNo=self.DealMager2.orderNo)
        self.assertEqual(sepOrder.model['success'], '1')

    # S8.获取其他用户订单拆分请求——获取成功
    def test_preSeparateOrder_other(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.DealMager2.orderNo)
        self.assertEqual(sepOrder.model['success'], '1')

    # S9.终端店获取订单拆分请求
    def test_preSeparateOrder_shop(self):
        sepOrder = self.wsUserShop.preSeparateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo)
        self.assertEqual(sepOrder.code, 300)

    # S10.已拆分订单请求拆分
    def test_preSeparateOrder_sparateAgain(self):
        sepOrder = self.wsDealMager.preSeparateOrder(orderNo=self.UserShop.orderCodWaitReceiveSeparat.orderNo)
        self.assertEqual(sepOrder.model['success'], '1')

    def assertPreSepOrder(self, rsp, order, buyer, seller):
        self.assertEqual(rsp.model['orderNo'], order.orderNo)
        self.assertEqual(rsp.model['orderAmount'], order.price)
        self.assertEqual(rsp.model['separateOrderTimes'], seller.separateOrderTimes)
        self.assertEqual(rsp.model['buyerName'], buyer.fullName)


    def tearDown(self):
        update('update dlcompany.dl_payment_split_info set min_amount = ? where company_id = ?', self.DealMager.separateMinAmount, self.DealMager.companyId)




def suite():
    suite=unittest.TestSuite()
    suite.addTest(preSeparateOrder('test_preSeparateOrder_codWaitDeliver'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_codWaitReceive'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_codWaitComplete'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_codWaitCancel'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_onlineWaitPay'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_null'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_lessPrice'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_other'))
    suite.addTest(preSeparateOrder('test_preSeparateOrder_shop'))
    # suite.addTest(preSeparateOrder('test_preSeparateOrder_sparateAgain'))
    return suite