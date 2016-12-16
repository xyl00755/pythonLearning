#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0045.获取购物车商品数量
http://127.0.0.1:8280/mallws/shoppingcart/getShoppingcartSize.json
{
    "token":"123",                          // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success":"0",                      // 成功 0-成功
        "shoppingCartSize":123              // 商品种类数量
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.ShoppingCartSizeResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import *
from www.common.database import update
from www.common.excel import wsData


class getShoppingcartSize(unittest.TestCase):

    UserShop = wsData('TmlShop')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    def setUp(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)

    # S1.添加一件商品获取购物车数量
    def test_getShoppingcartSize_one(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        getMerchCount = ws.getShoppingcartSize()
        self.assertEqual(getMerchCount.model['success'], '0')
        self.assertEqual(getMerchCount.model['shoppingCartSize'], 1)

    # S2.添加多件商品获取购物车数量
    def test_getShoppingcartSize_many(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='9', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='99', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        ws.addShoppingcar(merchId=self.Merch4.goodsId, merchCount='999', sellerId=self.Merch4.seller_store_id, sellerName=self.Merch4.sellerName)
        getMerchCount = ws.getShoppingcartSize()
        self.assertEqual(getMerchCount.model['success'], '0')
        self.assertEqual(getMerchCount.model['shoppingCartSize'], 3)

    # S3.无商品获取购物车商品数量
    def test_getShoppingcartSize_null(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        getMerchCount = ws.getShoppingcartSize()
        self.assertEqual(getMerchCount.model['success'], '0')
        self.assertEqual(getMerchCount.model['shoppingCartSize'], 0)

    def tearDown(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(getShoppingcartSize("test_getShoppingcartSize_one"))
    suite.addTest(getShoppingcartSize("test_getShoppingcartSize_many"))
    suite.addTest(getShoppingcartSize("test_getShoppingcartSize_null"))
    return suite