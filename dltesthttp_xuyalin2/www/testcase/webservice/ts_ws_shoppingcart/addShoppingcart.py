#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0039.添加商品到购物车
http://127.0.0.1:8280/mallws/shoppingcart/addShoppingcart.json
{
    "token":"123",              // 必须
    "merchId":"123123123",      // 必须 商品id
    "merchCount":"123",         // 必须 商品数量
    "sellerId":"123123",        // 必须 卖家id
    "sellerName":"烟酒旗舰店"   // 必须 卖家名字
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "1"              // 是否成功 0-成功 1-未知失败 2-库存不足 3-商品种类超过限制
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 必须验证
    merchCount              @NotNull        @Pattern(regexp = "[1-9][0-9]{0,8}")        // 数据库为11位 限制为9位
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import *
from www.common.database import update
from www.common.excel import wsData
from www.common.model import Shoppingcart


class addShoppingcart(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    def setUp(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)

    # S1.添加商品进入购物车
    def test_addShoppingcart_addMerch(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        addMerch = ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        self.assertEqual(addMerch.code, 200)
        self.assertEqual(addMerch.model['success'], '0')
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch1.goodsId)
        self.assertEqual(shopcart.goods_quantity, 1)


    # S2.多次添加同样商品进入购物车
    def test_addShoppingcart_addMerchAgain(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='10', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='100', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch1.goodsId)
        self.assertEqual(shopcart.goods_quantity, 111)


    # S3.添加不同的商品进入购物车
    def test_addShoppingcart_addMerchDiff(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        shopcartNum = Shoppingcart.count_by('where user_id = ?', self.UserShop.userId)
        self.assertEqual(shopcartNum, 2)

    # S4.添加起购量为5的商品进入购物车
    def test_addShoppingcart_addMerchStart(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch2.goodsId)
        self.assertEqual(shopcart.goods_quantity, 5)

    # S5.添加不存在的商品进入购物车
    def test_addShoppingcart_addMerchNotExist(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        addMerch = ws.addShoppingcar(merchId='NotExist', merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        self.assertEqual(addMerch.model['success'], '1')

    # S6.添加商品ID为空进入购物车
    def test_addShoppingcart_addMerchNull(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        addMerch = ws.addShoppingcar(merchId=None, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        self.assertEqual(addMerch.model['success'], '1')

    # S7.添加无售卖权的商品进入购物车
    def test_addShoppingcart_addMerchNoSaleRight(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addMerch = ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        self.assertEqual(addMerch.model['success'], '1')

    # S8.添加无库存的商品进入购物车
    def test_addShoppingcart_addMerchNoSold(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', '0', self.Merch1.goodsId)
        addMerch = ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        self.assertEqual(addMerch.model['success'], '2')

    # S9.添加商品数量超过库存
    def test_addShoppingcart_addMerchUpSold(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        addMerch = ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount=int(self.Merch1.onHandInventory)+1, sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        self.assertEqual(addMerch.model['success'], '2')

    # S10.配送商名称、id和商品id不匹配——错误 #5399 不做修改
    # def test_addShoppingcart_addMerchUnMatch(self):
    #     ws = webservice()
    #     ws.login(self.UserShop.username, self.UserShop.password)
    #     addMerch = ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch4.seller_store_id, sellerName=self.Merch4.sellerName)
    #     self.assertEqual(addMerch.model['success'], '1')

    def tearDown(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerch"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchAgain"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchDiff"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchStart"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchNotExist"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchNull"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchNoSaleRight"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchNoSold"))
    suite.addTest(addShoppingcart("test_addShoppingcart_addMerchUpSold"))
    #suite.addTest(addShoppingcart("test_addShoppingcart_addMerchUnMatch"))
    return suite