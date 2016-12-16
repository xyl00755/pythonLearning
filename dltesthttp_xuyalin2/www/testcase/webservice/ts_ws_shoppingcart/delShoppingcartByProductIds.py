#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0042.删除购物车中的商品信息
http://127.0.0.1:8280/mallws/shoppingcart/delShoppingcartByProductIds.json
{
    "token":"123",                          // 必须
    "delList":[
        {
            "shoppingCartId":"123123",      // 必须 购物车id
            "merchId":"123123123"           // 必须 商品id
        },
        {
            "shoppingCartId":"123123",      // 必须 购物车id
            "merchId":"123123123"           // 必须 商品id
        }
    ]
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "1"                      // 是否成功 0-成功 1-未知失败
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

"""

import unittest

from www.api.webservice import *
from www.common.database import update,select_int
from www.common.excel import wsData


class delShoppingcartByProductIds(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    def setUp(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)

    # S1.删除购物车中商品
    def test_delShoppingcartByProductIds_one(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        delMerch = ws.delShoppingcartByProductIds(delList=[{"shoppingCartId":shopcartId,"merchId":self.Merch1.goodsId}])
        self.assertEqual(delMerch.model['success'], '0')
        shopNum = select_int('select count(*) from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)
        self.assertEqual(shopNum, 0)

    # S2.删除多个购物车中商品
    def test_delShoppingcartByProductIds_many(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        #ws.addShoppingcar(merchId=self.Merch4.goodsId, merchCount='1', sellerId=self.Merch4.seller_store_id, sellerName=self.Merch4.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId1 = None
        shopcartId2 = None
        if shopcart.model['sellerList'][0]['merchList'][0]['merchId'] == self.Merch1.goodsId:
            shopcartId1 = shopcart.model['sellerList'][0]['merchList'][0]['id']
            shopcartId2 = shopcart.model['sellerList'][0]['merchList'][1]['id']
        elif shopcart.model['sellerList'][0]['merchList'][0]['merchId'] == self.Merch2.goodsId:
            shopcartId1 = shopcart.model['sellerList'][0]['merchList'][1]['id']
            shopcartId2 = shopcart.model['sellerList'][0]['merchList'][0]['id']
        list1 = {"shoppingCartId":shopcartId1,"merchId":self.Merch1.goodsId}
        list2 = {"shoppingCartId":shopcartId2,"merchId":self.Merch2.goodsId}
        delMerch = ws.delShoppingcartByProductIds(delList=[list1,list2])
        self.assertEqual(delMerch.model['success'], '0')
        shopNum = select_int('select count(*) from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)
        self.assertEqual(shopNum, 0)

    # S3.删除其他用户的购物车——错误 #5423
    def test_delShoppingcartByProductIds_other(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        ws.login(self.UserShop2.username, self.UserShop2.password)
        delMerch = ws.delShoppingcartByProductIds(delList=[{"shoppingCartId":shopcartId,"merchId":self.Merch1.goodsId}])
        self.assertEqual(delMerch.model['success'], '1')

    # S4.删除不存在的购物车
    def test_delShoppingcartByProductIds_notExist(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        delMerch = ws.delShoppingcartByProductIds(delList=[{"shoppingCartId":'NotExist',"merchId":'NotExist'}])
        self.assertEqual(delMerch.model['success'], '1')

    # S5.删除购物车时购物车ID和商品ID不匹配——错误 #5427 不做修改
    # def test_delShoppingcartByProductIds_notMatch(self):
    #     ws = webservice()
    #     ws.login(self.UserShop.username, self.UserShop.password)
    #     ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
    #     shopcart = ws.toShoppingcart()
    #     shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
    #     delMerch = ws.delShoppingcartByProductIds(delList=[{"shoppingCartId":shopcartId,"merchId":self.Merch2.goodsId}])
    #     self.assertEqual(delMerch.model['success'], '1')


    def tearDown(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(delShoppingcartByProductIds("test_delShoppingcartByProductIds_one"))
    suite.addTest(delShoppingcartByProductIds("test_delShoppingcartByProductIds_many"))
    suite.addTest(delShoppingcartByProductIds("test_delShoppingcartByProductIds_other"))
    suite.addTest(delShoppingcartByProductIds("test_delShoppingcartByProductIds_notExist"))
    #suite.addTest(delShoppingcartByProductIds("test_delShoppingcartByProductIds_notMatch"))
    return suite