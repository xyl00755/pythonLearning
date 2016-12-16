#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0184.订单取消审批
http://127.0.0.1:8280/mallws/orders/oper/auditCancel.json
{
    "token":"123",                      // 必须
    "paymentNo":"123123123",            // 必须 大订单号
    "orderNo":"123123",                 // 必须 订单号
    "auditStatus":"1"                   // 必须 批准结果 0-同意 1-拒绝
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                      // 0-成功 1-失败 2-订单已被处理
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


class auditCancel(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    DealMgr = wsData('DealMager')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    # S1.拒绝取消订单
    def test_auditCancel_reject(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        ws.deliver(orderNo=order.orderNo)
        order.ws.cancel(paymentNo=order.paymentNo, cancelType='3')
        auditCancel = ws.auditCancel(paymentNo=order.paymentNo, orderNo=order.orderNo, auditStatus='1')
        self.assertEqual(auditCancel.model['success'], '0')

    # S2.同意取消订单
    def test_auditCancel_agree(self):
        order = createOrder(self.UserShop, self.Merch1)
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        ws.deliver(orderNo=order.orderNo)
        order.ws.cancel(paymentNo=order.paymentNo, cancelType='3')
        auditCancel = ws.auditCancel(paymentNo=order.paymentNo, orderNo=order.orderNo, auditStatus='0')
        self.assertEqual(auditCancel.model['success'], '0')



def suite():
    suite = unittest.TestSuite()
    suite.addTest(auditCancel("test_auditCancel_reject"))
    suite.addTest(auditCancel("test_auditCancel_agree"))
    return suite