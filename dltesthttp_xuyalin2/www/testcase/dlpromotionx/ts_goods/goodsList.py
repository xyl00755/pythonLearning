#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *

class goodsList(unittest.TestCase):

    dlservice = dlpromotionx()

    #正确获取商品
    def test_goodsList_success(self):
        brandIdList = ['B00003','B00008','B00010']
        getGoodsListResult = self.dlservice.goodsList(goodsNameOrNumber=u'测试',brandIdList=brandIdList)
        self.assertEqual(getGoodsListResult['status'],0)
        for i in range(len(getGoodsListResult['data']['result'])):
            self.assertEqual(u'测试' in getGoodsListResult['data']['result'][i]['goodsFullName'],True)
            self.assertEqual(getGoodsListResult['data']['result'][i]['brandId'] in brandIdList,True)

    #输入不存在的商品名称
    def test_goodsList_goodNotExist(self):
        brandIdList = ['B00003','B00008','B00010']
        getGoodsListResult = self.dlservice.goodsList(goodsNameOrNumber=u'我就不信还有商品叫这个名字',brandIdList=brandIdList)
        self.assertEqual(getGoodsListResult['status'],0)
        self.assertEqual(len(getGoodsListResult['data']['result']),0)

    #分页展示
    def test_goodsList_paging(self):
        brandIdList = ['B00003','B00008','B00010']
        getGoodsListResult = self.dlservice.goodsList(goodsNameOrNumber=u'测试',brandIdList=brandIdList,pageIndex=1,pageSize=3)
        self.assertEqual(getGoodsListResult['status'],0)
        self.assertEqual(len(getGoodsListResult['data']['result']),3)
        self.assertEqual(getGoodsListResult['data']['count']>len(getGoodsListResult['data']['result']),True)
        for i in range(len(getGoodsListResult['data']['result'])):
            self.assertEqual(u'测试' in getGoodsListResult['data']['result'][i]['goodsFullName'],True)
            self.assertEqual(getGoodsListResult['data']['result'][i]['brandId'] in brandIdList,True)

    #不选品牌
    def test_goodsList_brandNull(self):
        brandIdList = ['B00003','B00008','B00010']
        getGoodsListResult = self.dlservice.goodsList(goodsNameOrNumber=u'测试')
        self.assertEqual(getGoodsListResult['status'],0)
        self.assertEqual(len(getGoodsListResult['data']['result'])>len(self.dlservice.goodsList(goodsNameOrNumber=u'测试',brandIdList=brandIdList)),True)
        for i in range(len(getGoodsListResult['data']['result'])):
            self.assertEqual(u'测试' in getGoodsListResult['data']['result'][i]['goodsFullName'],True)

    #不输入商品名称
    def test_goodsList_goodNameNull(self):
        brandIdList = ['B00003','B00008','B00010']
        getGoodsListResult = self.dlservice.goodsList(brandIdList=brandIdList)
        self.assertEqual(getGoodsListResult['status'],0)
        self.assertEqual(len(getGoodsListResult['data']['result'])>len(self.dlservice.goodsList(goodsNameOrNumber=u'测试',brandIdList=brandIdList)),True)
        for i in range(len(getGoodsListResult['data']['result'])):
            self.assertEqual(getGoodsListResult['data']['result'][i]['brandId'] in brandIdList,True)

    #不输入信息直接搜索，会返回所有商品
    def test_goodsList_inputNull(self):
        getGoodsListResult = self.dlservice.goodsList()
        self.assertEqual(getGoodsListResult['status'],0)
        self.assertEqual(len(getGoodsListResult['data']['result']),getGoodsListResult['data']['count'])

def suite():
    suite=unittest.TestSuite()
    suite.addTest(goodsList("test_goodsList_success"))
    suite.addTest(goodsList("test_goodsList_goodNotExist"))
    suite.addTest(goodsList("test_goodsList_paging"))
    suite.addTest(goodsList("test_goodsList_brandNull"))
    suite.addTest(goodsList("test_goodsList_goodNameNull"))
    suite.addTest(goodsList("test_goodsList_inputNull"))
    return suite