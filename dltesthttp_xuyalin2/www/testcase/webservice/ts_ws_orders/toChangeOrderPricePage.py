#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import update
from www.common.excel import wsData
from www.operation.order import  createOrder

"""
获取订单改价页面展示信息0185.获取订单改价页面展示信息
http://127.0.0.1:8280/mallws/orders/toChangeOrderPricePage.json
{
	"token":"123",   		//必须 token校验登录状态
	"orderNo":"123456"		//必须 订单号
}

{
	"code":200,
	"description":"执行成功!",
	"model":{
		"success":"0",						//成功 0-成功
		"orderMessage":{
			"orderNo":"123456",				//订单号
			"buyerName":"xxxx",				//买家名称
			"orderRetailAmount":"1000",		//订单原始金额
			"orderDiscountAmount":"-100"	//订单折扣金额
			"orderStatus":"C011"			//订单状态
		}

	},
	"metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.OrderChangePriceResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""
class toChangeOrderPricePage(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')

    # 获取已经存在的订单页面展示信息
    def test_getChangeOrderPricePage_exist(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id,
        #                   sellerName=self.Merch1.sellerName)
        # shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId,
        #                                    self.Merch1.goodsId)
        # invoice = {"invoiceId": self.UserShop.invoiceId, "invoiceType": "N011", "needInvoice": "0",
        #            "invoiceHeader": self.UserShop.invoiceHeader}
        # deliverAddress = {"deliverAddress": self.UserShop.deliverAddress, "deliverMobile": self.UserShop.deliverMobile,
        #                   "deliverPerson": self.UserShop.deliverPerson}
        # sellerList = []
        # sellerList.append({"sellerId": self.Merch1.shopcartSellerId, "sellerName": self.Merch1.sellerName,
        #                    "isYijipayAccount": self.Merch1.isYijipayAccount, "codFlag": self.Merch1.codFlag,
        #                    "supportVatInvoice": self.Merch1.supportVatInvoice,
        #                    "comment": "createOrderByShoppingcart comment.", "merchList":
        #                        [{"id": shopcart.id, "merchId": self.Merch1.goodsId,
        #                          "merchBarCode": self.Merch1.productBarCode}]})

        # order = ws.createOrderByShoppingcart(payWay='2', invoice=invoice, deliverAddress=deliverAddress,
        #                                      sellerList=sellerList)
        order = createOrder(buyer=self.UserShop, merch=self.Merch1)
        OrderPricePageRst = ws.getChangeOrderPricePage(orderNo=order.orderNo)
        self.assertEqual(OrderPricePageRst.code, 200)
        self.assertEquals(OrderPricePageRst.model["success"], '0')
        self.assertEquals(OrderPricePageRst.model["orderMessage"]["buyerName"], self.UserShop.fullName)
        self.assertEquals(OrderPricePageRst.model["orderMessage"]["orderStatus"], 'C020')

    #获取其他账户的订单信息——bug#
    def test_getChangeOrderPricePage_OtherUser(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        OrderPricePageRst = ws.getChangeOrderPricePage(orderNo=self.UserShop2.orderNo)
        self.assertEqual(OrderPricePageRst.code, 200)
        self.assertEquals(OrderPricePageRst.model["success"], '0')


    #获取不存在的订单页面信息
    def test_getChangeOrderPricePage_notexist(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        OrderPricePageRst = ws.getChangeOrderPricePage(orderNo='123456789')
        self.assertEqual(OrderPricePageRst.code, 500)

    def tearDown(self):
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(toChangeOrderPricePage('test_getChangeOrderPricePage_exist'))
    suite.addTest(toChangeOrderPricePage('test_getChangeOrderPricePage_notexist'))
    suite.addTest(toChangeOrderPricePage('test_getChangeOrderPricePage_OtherUser'))
    return suite