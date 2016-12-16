#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
URL:http://127.0.0.1:8280/dealer/getGoodsCoupon
请求示例：
{
    'goodsIds':XX,
    'companyId':XX,
    'showWay':XX
}

返回示例：
{
    "code": 0,
    "data":{
        "goodsList":[
            {
                "goodsId":"123",
                "flag":"true"
            },
            {
                "goodsId":"456",
                "flag":"false"
            }
        ]
    }
}
"""

class getGoodsCoupon(unittest.TestCase):

    UserShop1=wsData('TmlShop')
    UserShop2=eData('goodsCoupon')

    dlservice = dlmall()
    s = dlservice.login(UserShop1.username,UserShop1.password)

    #执行用例前的操作
    #def setUp(self):

    #验证配置了优惠券且已启用的商品的flag为true（前提：该商品配置了优惠券,优惠券处于启用状态）
    def test_getGoodsCouponFlag_true1(self):
        goodsList = [self.UserShop2.goods_id1,self.UserShop2.goods_id2]
        goodsCouponFlagInfo = self.dlservice.getGoodsCoupon(self.s,goodsIds=goodsList,companyId=self.UserShop1.companyId)
        for each in goodsCouponFlagInfo['data']:
            self.assertEqual(each["flag"],True)

    #验证配置了优惠券但未启用的商品的flag为false（前提：该商品配置了优惠券,优惠券处于未启用状态）
    def test_getGoodsCouponFlag_true2(self):
        goodsCouponFlagInfo = self.dlservice.getGoodsCoupon(self.s,goodsIds=[self.UserShop2.goods_id3,self.UserShop2.goods_id4],companyId=self.UserShop1.companyId)
        for each in goodsCouponFlagInfo['data']:
            self.assertEqual(each["flag"],False)

    #验证没有配置优惠券的商品flag为false
    def test_getGoodsCouponFlag_false(self):
        goodsCouponFlagInfo = self.dlservice.getGoodsCoupon(self.s,goodsIds=[self.UserShop2.goods_id5],companyId=self.UserShop1.companyId)
        for each in goodsCouponFlagInfo['data']:
                self.assertEqual(each["flag"],False)

    #验证接口一致性（入参和返回都是同一商品）
    def test_getGoodsCouponFlag_GoodsIsSame(self):
        goodsCouponFlagInfo = self.dlservice.getGoodsCoupon(self.s,goodsIds=[self.UserShop2.goods_id1],companyId=self.UserShop1.companyId)
        self.assertEqual(goodsCouponFlagInfo['data'][0]['goodsId'],self.UserShop2.goods_id1)

    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getGoodsCoupon("test_getGoodsCouponFlag_true1"))
    suite.addTest(getGoodsCoupon("test_getGoodsCouponFlag_true2"))
    suite.addTest(getGoodsCoupon("test_getGoodsCouponFlag_false"))
    suite.addTest(getGoodsCoupon("test_getGoodsCouponFlag_GoodsIsSame"))
    return suite