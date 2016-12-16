#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0050.获取卖家订单的数量
http://127.0.0.1:8280/mallws/orders/getSellerOrderCount.json
{
    "token":"123"                           // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                 // 成功 0-成功
        "orderCount": {
            "pendingPaymentOrderCount": "0",            // 待付款订单数量
            "waitingShipmentOrderCount": "1",           // 待发货订单数量
            "waitingReceiveOrderCount": "1",            // 待收货订单数量
            "finishedOrderCount": "1",                  // 已完成订单数量
            "cancelledOrderCount": "1"                  // 已取消订单数量
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.OrderCountResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    卖家没有待付款订单 返回-1
"""

import unittest

from www.api.webservice import *
from www.common.database import select_int
from www.common.excel import wsData


class getSellerOrderCount(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShopMin = wsData('TmlShopMin')
    DealMgr = wsData('DealMager')
    DealMgr2 = wsData('DealMager2')
    DealSaler = wsData('DealSaler')
    DealBuyer = wsData('DealBuyer')

    # S1.终端店获取买家订单数量失败
    def test_getSellerOrderCount_shopBuyer(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        orderCount = ws.getSellerOrderCount()
        self.assertEqual(orderCount.code, 300)


    # S2、订单为空时获取订单数量
    def test_getSellerOrderCount_null(self):
        ws = webservice()
        ws.login(self.DealMgr2.username, self.DealMgr2.password)
        orderCount = ws.getSellerOrderCount()
        self.assertEqual(orderCount.model['success'], '0')
        self.assertOrderCount(orderCount, self.DealMgr2)

    # S3.经销商管理员获取订单数量
    def test_getSellerOrderCount_dealMgr(self):
        ws = webservice()
        ws.login(self.DealMgr.username, self.DealMgr.password)
        orderCount = ws.getSellerOrderCount()
        self.assertEqual(orderCount.model['success'], '0')
        self.assertOrderCount(orderCount, self.DealMgr)

    # S4.经销商采购员获取买家订单数量
    def test_getSellerOrderCount_dealBuyer(self):
        ws = webservice()
        ws.login(self.DealBuyer.username, self.DealBuyer.password)
        orderCount = ws.getSellerOrderCount()
        self.assertEqual(orderCount.code, 300)

    # S5.经销商销售员获取买家订单数量失败
    def test_getSellerOrderCount_dealSaler(self):
        ws = webservice()
        ws.login(self.DealSaler.username, self.DealSaler.password)
        orderCount = ws.getSellerOrderCount()
        self.assertEqual(orderCount.model['success'], '0')
        self.assertOrderCount(orderCount, self.DealBuyer)

    def assertOrderCount(self, rsq, seller):
        # C011待付款(买家没有待付款订单返回-1)
        orderCountWaitPayDB = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_seller_detail where seller_id = ?) and order_status = ?', seller.companyId, 'C011')
        #self.assertEqual(rsq.model['orderCount']['pendingPaymentOrderCount'], str(orderCountWaitPayDB))
        self.assertEqual(rsq.model['orderCount']['pendingPaymentOrderCount'], '-1')
        # C012已取消
        orderCountCancelDB = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_seller_detail where seller_id = ?) and order_status = ?', seller.companyId, 'C012')
        self.assertEqual(rsq.model['orderCount']['cancelledOrderCount'], str(orderCountCancelDB))
        # C015已退款

        # C017待收货
        orderCountWatiRecDB = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_seller_detail where seller_id = ?) and order_status = ?', seller.companyId, 'C017')
        self.assertEqual(rsq.model['orderCount']['waitingReceiveOrderCount'], str(orderCountWatiRecDB))
        # C019交易完成
        orderCountFinishDB = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_seller_detail where seller_id = ?) and order_status = ?', seller.companyId, 'C019')
        self.assertEqual(rsq.model['orderCount']['finishedOrderCount'], str(orderCountFinishDB))
        # C020待发货
        orderCountWaitDeliverDB = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_seller_detail where seller_id = ?) and order_status = ?', seller.companyId, 'C020')
        self.assertEqual(rsq.model['orderCount']['waitingShipmentOrderCount'], str(orderCountWaitDeliverDB))
        # C021交易异常

        # C025支付中





def suite():
    suite = unittest.TestSuite()
    suite.addTest(getSellerOrderCount("test_getSellerOrderCount_shopBuyer"))
    suite.addTest(getSellerOrderCount("test_getSellerOrderCount_null"))
    suite.addTest(getSellerOrderCount("test_getSellerOrderCount_dealMgr"))
    suite.addTest(getSellerOrderCount("test_getSellerOrderCount_dealBuyer"))
    suite.addTest(getSellerOrderCount("test_getSellerOrderCount_dealSaler"))
    return suite