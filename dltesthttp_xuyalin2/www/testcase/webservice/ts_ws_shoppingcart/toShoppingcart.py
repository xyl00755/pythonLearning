#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0041.获取购物车中的商品信息
http://127.0.0.1:8280/mallws/shoppingcart/toShoppingcart.json
{
    "token":"123"                   // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                                         // 成功 0-成功
        "sellerList": [
            {
                "sellerId": "7b632e29789d406595e93246fdb50fa4",                                 // 卖家id
                "sellerName": "黄尾超市",                                                       // 卖家名
				"isYijipayAccount": "0",                                    					// 卖家是否是易极付账户 0-是 1-不是
                "paymentFlag":"0",                                                              // 付款标志 结算用
                "codFlag":"0",                                                                  // 货到付款标志 结算用
                "supportCod": "0",                                                              // 支持货到付款 0-支持 1-不支持
                "supportVatInvoice": null,                                                      // 支持增值税发票 0-支持 1-不支持
                "merchList": [                                                                  // 商品列表
                    {
                        "id": "b8d8f93a5eae48b4a8918f741982d405",                               // 购物车id
                        "merchId": "67d4cb03595348cdacd61000bc96ba03",                          // 商品id
                        "merchName": "珍品古钟红星二锅头 46度 450ml（6瓶/箱）(APP专用)",        // 商品名
                        "merchBarCode": "TM003",                                                // 条形码
                        "merchQuantity": "19990",                                               // 商品数量
                        "picUrl": null,                                                         // 商品图片
                        "specName": "3",                                                        // 规格
                        "priceRetail": "3",                                                     // 零售价
                        "priceDanlu": "3",                                                      // 丹露价
                        "unitPrice": "31",                                                      // 单价
                        "merchStatus": "0",                                                     // 商品状态 0 正常 1 暂时缺货 2 已下架 3 已失效 4 商品不存在
                        "promotionModelList" [
                            {
                                "promotionId":"123",                                            // 促销id
                                "promotionType":"0",                                            // 0-满赠 1-满减
                                "reductionType":"1",                                            // 满减类型 -1-无此选项 0-减单价 1-减总额
                                "promotionInfo":"123123",                                       // 促销语
                                "ruleId":"123"                                                  // 规则
                                "isDefaultPromotion":"0",                                       // 是否是默认促销 0-是 1-不是
                                "isPromotion":"1",                                              // 是否满足促销 0-不满足促销 1-满足促销
                                "promotionFlag":"0",                                            // 优惠类型 0-满增 1-满减单 2-满减总
                                "diffPrice":"100",                                              // 优惠差价
                                "presentationDetail":"123123"                                   // 满增促销语
                            }
                        ],
                        "onHandInventory": "20000",                                             // 库存
                        "miniStartSaleQuantityChanged":"0",                                     // 最小起售量发生变化 0-变化 1-没变化
                        "sellerId": "7b632e29789d406595e93246fdb50fa4",                         // 卖家id
                        "sellerName": "黄尾超市"                                                // 卖家名
                    }
                ]
            }
        ],
        "merchTypeCount": "4"                                                                   // 购物车商品种类数
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.ToShoppingcartResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import *
from www.common.database import update,select_one
from www.common.excel import wsData


class toShoppingcart(unittest.TestCase):

    UserShop = wsData('TmlShop')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    def setUp(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)

    # S1.获取购物车商品信息
    def test_toShoppingcart_one(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        toShoppingcart = ws.toShoppingcart()
        self.assertShoppingcart(toShoppingcart, self.Merch1)



    # S2.没有商品时获取购物车商品信息
    def test_toShoppingcart_null(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        toShoppingcart = ws.toShoppingcart()
        self.assertEqual(toShoppingcart.code, 200)
        self.assertEqual(toShoppingcart.model['success'], '0')
        self.assertEqual(toShoppingcart.model['merchTypeCount'], '0')

    # S3.获取多个购物车商品信息
    def test_toShoppingcart_more(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
        ws.addShoppingcar(merchId=self.Merch4.goodsId, merchCount='1', sellerId=self.Merch4.seller_store_id, sellerName=self.Merch4.sellerName)
        toShoppingcart = ws.toShoppingcart()
        self.assertShoppingcart(toShoppingcart, self.Merch1, merchTypeCount='3')




    # 判断获取购物车信息是否正确
    def assertShoppingcart(self, rsp, merch, code = 200, success = '0', merchTypeCount = '1'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['merchTypeCount'], merchTypeCount)


        testFlag = False
        testFlag2 = False
        testFlag3 = False
        for i in range(0, len(rsp.model['sellerList'])):
            if rsp.model['sellerList'][i]['sellerId'].decode('utf-8') == merch.seller_store_id+'_split_'+merch.storeName.decode('utf-8'):
                testFlag = True
                self.assertEqual(rsp.model['sellerList'][i]['sellerName'], merch.sellerName)
                self.assertEqual(rsp.model['sellerList'][i]['isYijipayAccount'], merch.isYijipayAccount)
                if rsp.model['sellerList'][i]['paymentFlag'] is not None:
                    self.assertEqual(rsp.model['sellerList'][i]['paymentFlag'], merch.paymentFlag)
                if merch.supportCod == '0':
                    self.assertEqual(rsp.model['sellerList'][i]['codFlag'], '0_split_0')
                else:
                    self.assertEqual(rsp.model['sellerList'][i]['codFlag'], '1_split_1')
                self.assertEqual(rsp.model['sellerList'][i]['supportCod'], merch.supportCod)
                self.assertEqual(rsp.model['sellerList'][i]['supportVatInvoice'], merch.supportVatInvoice)
                for j in range(0,len(rsp.model['sellerList'][i]['merchList'])):
                    if rsp.model['sellerList'][i]['merchList'][j]['merchId'] == merch.goodsId :
                        testFlag2 = True
                        shopcart = select_one('select * from danlu_cd_database.dl_shoppingcart where user_id = ? and goods_id = ?',self.UserShop.userId, merch.goodsId)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['id'],shopcart.id)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['merchName'], merch.fullName)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['merchBarCode'], merch.productBarCode)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['merchQuantity'],str(shopcart.goods_quantity))
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['picUrl'], merch.picUrl)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['specName'], merch.merchSpec)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['priceRetail'], merch.priceRetail)
                        self.assertIsNone(rsp.model['sellerList'][i]['merchList'][j]['priceDanlu'])
                        # self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['priceDanlu'], merch.priceDanlu)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['unitPrice'], merch.unitPrice)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['merchStatus'], merch.merchStatus)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['onHandInventory'], merch.onHandInventory)
                        self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['miniStartSaleQuantityChanged'], '1')
                        for k in range(0,len(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'])):
                            if rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['promotionInfo'] == merch.promotionInfo :
                                testFlag3 = True
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['promotionId'], merch.promotionId)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['promotionType'], merch.promotionType)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['reductionType'], merch.reductionType)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['promotionInfo'], merch.promotionInfo)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['isDefaultPromotion'], merch.isDefaultPromotion)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['isPromotion'], merch.isPromotionCart)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['diffPrice'], merch.diffPrice)
                                self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['promotionFlag'], merch.promotionFlag)
                                if rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['presentationDetail'] == merch.presentationDetail:
                                    self.assertEqual(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'][k]['presentationDetail'], merch.presentationDetail)
                                #testFlag = True
                            if k == len(rsp.model['sellerList'][i]['merchList'][j]['promotionModelList'])-1:
                                self.assertEqual(testFlag3,True,merch.promotionInfo + ' is not found.')
                    if j == len(rsp.model['sellerList'][i]['merchList'])-1 :
                        self.assertEqual(testFlag2,True,merch.goodsId + ' is not found.')
            if i == len(rsp.model['sellerList'])-1:
                self.assertEqual(testFlag,True,merch.seller_store_id+'_split_'+merch.storeName.decode('utf-8') + ' is not found.')




    def tearDown(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(toShoppingcart("test_toShoppingcart_one"))
    suite.addTest(toShoppingcart("test_toShoppingcart_null"))
    suite.addTest(toShoppingcart("test_toShoppingcart_more"))
    return suite