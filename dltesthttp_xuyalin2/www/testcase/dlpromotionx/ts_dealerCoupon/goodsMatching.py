#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *

"""
URL：http://127.0.0.1:8280/dealerCoupon/goodsMatching
请求示例：
{
    'goodsName':测试商品,
    'pageIndex':1,
    'pageSize':10
}

返回示例：
 {
    "status": 0,
    "data":[{
        "goodsId":"0002d80653bdcb4d542b0fc91267dbbb",
        "sellerId":"c315141bbcdf42b5ada1fbb83467899f",
        "storeId":"432279c19c0ea75bc3c2f5e2c377b30a",
        "goodsName":"简优湘泉酒",
        "goodsComment":"十二年陈红星二锅头",
        "unitsConvertion":1,
        "packagesTypePropertyValue":"瓶",
        "priceRetail":13800,
        "priceDanlu":,
        "goodsStatus":"01",
        "onHandInventory":"999"
      }]
    }
    "msg":"查询成功"
  }
"""


class goodsMatching(unittest.TestCase):

    #执行用例前的操作
    #def setUp(self):

    #最多返回10个商品名称中带有"test"的商品（前提：商品名包含“test”的商品数量超过10个）
    def test_goodsMatching_number10(self):
        dlservice = dlpromotionx()
        goodsMatchingInfo = dlservice.goodsMatching(goodsName="test",pageIndex = 1,pageSize = 10)
        self.assertEqual(len(goodsMatchingInfo['data']),10)

    #验证返回值的每一个商品名称都带有“test”（前提：商品名包含“test”的数量超过10个）
    def test_goodsMatching_contain(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.goodsMatching(goodsName='test',pageIndex = 1,pageSize = 10)
        for each in nameMatchingInfo['data']:
            self.assertEqual("test" in each['goodsName'] or "TEST" in each['goodsName'],True)

    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite=unittest.TestSuite()
    #suite.addTest(goodsMatching("test_goodsMatching_number10"))
    suite.addTest(goodsMatching("test_goodsMatching_contain"))
    return suite