#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0040.修改指定商品在购物车中的数量
http://127.0.0.1:8280/mallws/shoppingcart/modifyShoppingcartCount.json
{
    "token":"123",                  // 必须
    "shoppingCartId":"123123",      // 必须 购物车id
    "merchId":"123123123",          // 必须 商品id
    "merchCount":"123",             // 必须 商品数量 (变更后的数量)
    "sellerId":"123123"             // 必须 卖家id (是列表接口商品的businessId)
    "usePromotion":"0",             // 必须 是否使用优惠 0-使用 1-没使用
    "promotionId":"123",            // usePromotion为1-不传 usePromotion为0-必须 促销id 如果选没有返回-1
    "promotionType":"0",            // usePromotion为1-不传 usePromotion为0-必须 促销类型 0-满赠 1-满减
    "reductionType":"0"             // usePromotion为1-不传 usePromotion为0-必须 满减类型 0-减单价 1-减总额
    "ruleId":"123"                  // usePromotion为1-不传 usePromotion为0-必须 规则
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                 // 是否成功 0-成功 1-未知失败
        "unitPrice": "100"              // 成功之后的单价
        "isPromotion":"1",              // 是否满足促销 -0-不满足促销 1-满足促销
        "promotionType":"0",            // 优惠类型 0-满增 1-满减单 2-满减总
        "diffPrice":"100",              // 优惠差价
        "presentationInfo":"123123",    // 满增促销语
        "reachMiniStartSaleQuantity":"0"// 到达最小起售量
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.ModifyShoppingCartCountResponse"
    }
}

参数校验:
    // 必须验证
    merchCount              @NotNull        @Pattern(regexp = "[1-9][0-9]{0,8}")        // 数据库为11位 限制为9位
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
param说明:
    如果没有选择促销 usePromotion传1 此时不传promotionId/reductionType
    如果选择了促销 usePromotion传0 此时必须传promotionId/reductionType
result说明:
    promotionType如果为0 则diffPrice没有 presentationInfo有
    promotionType如果为1/2 则diffPrice有 presentationInfo没有
    如果不满足促销 只有diffPrice
"""

import unittest

from www.api.webservice import *
from www.common.database import update
from www.common.excel import wsData


class modifyShoppingcartCount(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    def setUp(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)

    # S1.修改购物车商品数量
    def test_modifyShoppingcartCount_add(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        modMerch = ws.modifyShoppingcartCount(shoppingCartId=shopcartId,merchId=self.Merch1.goodsId,merchCount='99',sellerId=self.Merch1.sellerId,usePromotion='1')
        self.assertEqual(modMerch.model['success'], '0')
        shopcart = ws.toShoppingcart()
        shopcartNum = shopcart.model['sellerList'][0]['merchList'][0]['merchQuantity']
        self.assertEqual(shopcartNum,'99')

    # S2.减少购物车商品数量
    def test_modifyShoppingcartCount_reduce(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='99', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        modMerch = ws.modifyShoppingcartCount(shoppingCartId=shopcartId,merchId=self.Merch1.goodsId,merchCount='1',sellerId=self.Merch1.sellerId,usePromotion='1')
        self.assertEqual(modMerch.model['success'], '0')
        shopcart = ws.toShoppingcart()
        shopcartNum = shopcart.model['sellerList'][0]['merchList'][0]['merchQuantity']
        self.assertEqual(shopcartNum,'1')

    # S3.减少购物车数量到0——bug5398
    def test_modifyShoppingcartCount_zero(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='99', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        modMerch = ws.modifyShoppingcartCount(shoppingCartId=shopcartId,merchId=self.Merch1.goodsId,merchCount='0',sellerId=self.Merch1.sellerId,usePromotion='1')
        self.assertEqual(modMerch.model['success'], '1')

    # S4.修改购物车数量达到库存上限
    def test_modifyShoppingcartCount_up(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        modMerch = ws.modifyShoppingcartCount(shoppingCartId=shopcartId,merchId=self.Merch1.goodsId,merchCount=self.Merch1.onHandInventory,sellerId=self.Merch1.sellerId,usePromotion='1')
        self.assertEqual(modMerch.model['success'], '0')
        shopcart = ws.toShoppingcart()
        shopcartNum = shopcart.model['sellerList'][0]['merchList'][0]['merchQuantity']
        self.assertEqual(shopcartNum,self.Merch1.onHandInventory)

    # S5.修改购物车数量超过库存上限
    def test_modifyShoppingcartCount_limit(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        modMerch = ws.modifyShoppingcartCount(shoppingCartId=shopcartId,merchId=self.Merch1.goodsId,merchCount=int(self.Merch1.onHandInventory)+1,sellerId=self.Merch1.sellerId,usePromotion='1')
        self.assertEqual(modMerch.model['success'], '0')
        shopcart = ws.toShoppingcart()
        shopcartNum = shopcart.model['sellerList'][0]['merchList'][0]['merchQuantity']
        self.assertEqual(shopcartNum,self.Merch1.onHandInventory)

    # S6.修改其他人的购物车商品数量——错误 #5423
    def test_modifyShoppingcartCount_other(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = ws.toShoppingcart()
        shopcartId = shopcart.model['sellerList'][0]['merchList'][0]['id']
        ws.login(self.UserShop2.username, self.UserShop2.password)
        modMerch = ws.modifyShoppingcartCount(shoppingCartId=shopcartId,merchId=self.Merch1.goodsId,merchCount=int(self.Merch1.onHandInventory)+1,sellerId=self.Merch1.sellerId,usePromotion='1')
        self.assertEqual(modMerch.model['success'], '1')



    def tearDown(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(modifyShoppingcartCount("test_modifyShoppingcartCount_add"))
    suite.addTest(modifyShoppingcartCount("test_modifyShoppingcartCount_reduce"))
    suite.addTest(modifyShoppingcartCount("test_modifyShoppingcartCount_zero"))
    suite.addTest(modifyShoppingcartCount("test_modifyShoppingcartCount_up"))
    suite.addTest(modifyShoppingcartCount("test_modifyShoppingcartCount_limit"))
    suite.addTest(modifyShoppingcartCount("test_modifyShoppingcartCount_other"))
    return suite