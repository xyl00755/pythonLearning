#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0183.订单取消
http://127.0.0.1:8280/mallws/orders/oper/cancel.json
{
    "token":"123",                      // 必须
    "paymentNo":"123123123",            // 必须 大订单号
    "payType":"123123",                 // 必须 1-在线支付 2-货到付款 3-公司转账
    "cancelType":"1"                    // 必须 1-C020待发货 2-C017已出库 3-C019交易完成 5-C017已出库
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                 // 0-成功 1-订单状态发生变化取消失败 2-取消失败
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
param说明:
    cancelType指的是订单列表接口里的 paymentOrderButtomList 里面的第四位数字
"""

import unittest

from www.api.webservice import *
from www.common.excel import wsData
from www.operation.order import createOrder


class cancel(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    DealMgr = wsData('DealMager')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    # S1.取消货到付款待发货订单
    def test_cancel_cod(self):
        order = createOrder(self.UserShop, self.Merch1)
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo)
        self.assertEqual(cancelOrder.model['success'], '0')

    # S2.取消货到付款待收货订单（及重复取消该订单）
    def test_cancel_coddeliver(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        ws.deliver(orderNo=order.orderNo)
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo, cancelType='3')
        self.assertEqual(cancelOrder.model['success'], '0')
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo, cancelType='3')
        self.assertEqual(cancelOrder.model['success'], '1')

    # S3.取消在线支付待付款订单
    def test_cancel_onlineNoPay(self):
        order = createOrder(self.UserShop, self.Merch1, payWay='1')
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo, payType='1', cancelType='1')
        self.assertEqual(cancelOrder.model['success'], '0')
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo, payType='1', cancelType='1')
        self.assertEqual(cancelOrder.model['success'], '1')

    # S4.取消在线支付待发货订单


    # S5.重复取消货到付款待发货订单
    def test_cancel_again(self):
        order = createOrder(self.UserShop, self.Merch1)
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo)
        self.assertEqual(cancelOrder.model['success'], '0')
        cancelOrder = order.ws.cancel(paymentNo=order.paymentNo)
        self.assertEqual(cancelOrder.model['success'], '1')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(cancel("test_cancel_cod"))
    suite.addTest(cancel("test_cancel_coddeliver"))
    suite.addTest(cancel("test_cancel_onlineNoPay"))
    suite.addTest(cancel("test_cancel_again"))
    return suite