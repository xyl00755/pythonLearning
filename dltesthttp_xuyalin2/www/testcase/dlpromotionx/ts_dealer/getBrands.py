#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *

"""
GET /dealerCoupon/getBrands
{
	"categoryCodesStr": 'C01L0101',
	"initial": 'A',
	"brandName": 'brandName'
}
  {
    "status": 0,
    "data": {
      "brandList":[{
        "brandId":"045f5561758241af8f5e72513dbb8707",
        "brandName":"怡宝",
        "brandProfile":"怡宝好",
        "brandLogo":"品牌Logo",
        "detailLink":"www.google.com",
        "brandOrder":"1",
        "brandStatus":"02",
        "brandNamePinyin":"yibao",
      }]
    },
    "msg":"查询成功"
  }
"""

class getBrands(unittest.TestCase):
    dlservice = dlpromotionx()

    #查询品类所有品牌
    def test_getBrands_nullPara(self):
        queryResult=self.dlservice.getBrands()
        self.assertEqual(queryResult['status'], -1)

    # 查询白酒品类所有品牌
    def test_getBrands_categoryCodesStr1(self):
        queryResult=self.dlservice.getBrands(categoryCodesStr='C01L0101')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertEqual(len(queryResult), 3)
        self.assertEqual(len(queryResult['data'][0]), 12)   #文档规定8个，但实际上多了
        self.assertIn('brandId',queryResult['data'][0].keys())
        self.assertIn('brandProfile', queryResult['data'][0].keys())
        self.assertIn('brandProfile', queryResult['data'][0].keys())
        self.assertIn('brandLogo', queryResult['data'][0].keys())
        self.assertIn('detailLink', queryResult['data'][0].keys())
        self.assertIn('brandOrder', queryResult['data'][0].keys())
        self.assertIn('brandStatus', queryResult['data'][0].keys())




    #查询葡萄酒品类所有品牌
    def test_getBrands_categoryCodesStr2(self):
        queryResult=self.dlservice.getBrands(categoryCodesStr='C01L0102')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')

    #查询白酒品类M开头品牌
    def test_getBrands_initialM(self):
        queryResult=self.dlservice.getBrands(categoryCodesStr='C01L0101',initial='M')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        for i in range(0,len(queryResult['data'])):
            #print queryResult['data']['brandList'][i]['brandNamePinyin'][0]
            self.assertEqual(queryResult['data'][i]['brandNamePinyin'][0],u'M')

    #查询指定的品牌名称
    def test_getBrands_brandName(self):
        queryResult=self.dlservice.getBrands(categoryCodesStr='C01L0101',brandName='茅台')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        for i in range(0,len(queryResult['data'])):
            #print queryResult['data']['brandList'][i]['brandName']
            self.assertEqual(queryResult['data'][i]['brandName'],u'茅台')
            self.assertEqual(queryResult['data'][i]['brandId'], u'B00010')
            self.assertEqual(queryResult['data'][i]['brandNamePinyin'][0], u'M')


def suite():
    suite=unittest.TestSuite()
    suite.addTest(getBrands("test_getBrands_categoryCodesStr1"))
    suite.addTest(getBrands("test_getBrands_categoryCodesStr2"))
    suite.addTest(getBrands("test_getBrands_initialM"))
    suite.addTest(getBrands("test_getBrands_nullPara"))
    suite.addTest(getBrands("test_getBrands_brandName"))
    return suite


