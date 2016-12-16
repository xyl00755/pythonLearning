#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *
import random
"""
GET dlmall/dealer/getAvailableCouponOfDealer.html
{
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "dealerId": dealerId,
            "showWay": showWay,
            "typeCode": typeCode,
            "dealerName": dealerName,
            "goodsName": goodsName,
            "goodsId": goodsId,
            "getWay": getWay,
            "pageIndex": pageIndex,
            "pageSize": pageSize,
            "sort": sort
}
  {
    "status": 0,
    "data": {
        "couponList":[{
            "dealerCouponDto":{
              "availableChannel":"S011",
              "goodsName":"白云边2979 45度 500mL",
              "goodsId":"absdsdsdfs",
              "dealerCouponImgUrl":"",
              "dealerId":"",
              "dealerName":"河北人人大的店铺名称",
              "platformLimit":"WEB",
              "dealerCouponName":"",
              "dealerCouponId":"",
              "dealerCouponAmounts":[
               {
                 "couponAmt":"5",
                 "effectiveAmt":"200"
               }]
            }，
            "activityId":"abc",
            "activityName":"该名称与优惠券的名称一样",
            "activityType":"10",
            "effectiveTime":"2016-08-31",
            "uneffectiveTime":"2017-08-31",
            "goodsName":"白云边2979 45度 500mL",
            "goodsId":"absdsdsdfs",
            "dealerName":"河北人人大的店铺名称",
        }]
    },
    "msg":"查询成功"
  }
"""


class getMoreAvailableCoupon(unittest.TestCase):
    couponInfo = eData('AvailableCouponsBenfits')
    benefitInfo = eData('AvailableCouponsBenfits')
    dealerInfo=wsData('DealMager')
    goodsInfo=wsData('Merch1')
    dlservice = dlmall()
    s = dlservice.login('testatzdd01', 'Danlu99')

    #空入参-查询出所有红包及优惠券
    def test_getMoreAvailableCouponSum_nullPara(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(self.s)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(len(queryResult['data'][0]), 50, 'data-couponList中一个coupon中应有50对键值，当前返回' + str(len(queryResult['data'][0])) + '对')
        self.assertEqual(len(queryResult['data'][0]['dealerCouponDto']), 33, 'data-couponList中一个coupon中应有33对键值，当前返回' + str(len(queryResult['data'][0]['dealerCouponDto'])) + '对')
        self.assertEqual(len(queryResult['data'][0]['dealerCouponDto']['dealerCouponAmounts'][0]), 9,
                         'data-couponList中一个coupon中应有9对键值，当前返回' + str(len(queryResult['data'][0]['dealerCouponDto']['dealerCouponAmounts'][0])) + '对')
        self.assertIn('availableChannel', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('goodsName', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('goodsId', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('dealerCouponImgUrl', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('dealerId', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('dealerName', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('platformLimit', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('dealerCouponName', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('dealerCouponId', queryResult['data'][0]['dealerCouponDto'])
        self.assertIn('activityId', queryResult['data'][0])
        self.assertIn('activityName', queryResult['data'][0])
        self.assertIn('activityType', queryResult['data'][0])
        self.assertIn('effectiveTime', queryResult['data'][0])
        self.assertIn('uneffectiveTime', queryResult['data'][0])

    #仅用必填字段查询
    def test_getMoreAvailableCouponSum_OnlyRequiredPara(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,companyId=self.couponInfo.tmlCompanyId2)
        self.assertEqual(queryResult['status'], 0)

    #仅查询红包
    def test_getMoreAvailableCouponSum_couponOnlyRequiredPara(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,dealerCouponType='10')
        couponInSQL=select_one('select * from dlcoupon.dl_dealer_coupon where dealer_coupon_id =?',self.couponInfo.dealerCouponId)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data'])):
            if queryResult['data'][i]['dealerCouponId'] !=self.couponInfo.dealerCouponId:
                self.assertEqual(queryResult['data'][i]['activityType'], '10')
            else:
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerCouponName'], couponInSQL.dealer_coupon_name)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerName'], couponInSQL.dealer_name)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerId'], couponInSQL.dealer_id)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['totalNum'], couponInSQL.total_num)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['totalAmount'], couponInSQL.total_amount)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['availableChannel'], couponInSQL.available_channel)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['areaLimit'], couponInSQL.area_limit)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerCouponAmounts'][0]['couponId'], couponInSQL.dealer_coupon_id)
                self.assertEqual(queryResult['data'][i]['activityName'], couponInSQL.dealer_coupon_name)
                self.assertEqual(queryResult['data'][i]['dealerId'], couponInSQL.dealer_id)
                self.assertEqual(queryResult['data'][i]['dealerName'], couponInSQL.dealer_name)
        # print couponInSQL


    #仅查询优惠券
    def test_getMoreAvailableCouponSum_benefitOnlyRequiredPara(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,dealerCouponType='11')
        benefitInSQL=select_one('select * from dlcoupon.dl_dealer_coupon where dealer_coupon_id =?',self.couponInfo.dealerBenefitId)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data'])):
            if queryResult['data'][i]['dealerCouponId'] !=self.couponInfo.dealerCouponId:
                self.assertEqual(queryResult['data'][i]['activityType'], '11')
            else:
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerCouponName'], benefitInSQL.dealer_coupon_name)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerName'], benefitInSQL.dealer_name)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerId'], benefitInSQL.dealer_id)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['totalNum'], benefitInSQL.total_num)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['totalAmount'], benefitInSQL.total_amount)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['availableChannel'], benefitInSQL.available_channel)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['goodsId'], benefitInSQL.goods_id)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['goodsName'], benefitInSQL.goods_name)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['areaLimit'], benefitInSQL.area_limit)
                self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerCouponAmounts'][0]['couponId'], benefitInSQL.dealer_coupon_id)
                self.assertEqual(queryResult['data'][i]['activityName'], benefitInSQL.dealer_coupon_name)
                self.assertEqual(queryResult['data'][i]['dealerId'], benefitInSQL.dealer_id)
                self.assertEqual(queryResult['data'][i]['dealerName'], benefitInSQL.dealer_name)
        # print benefitInSQL

    #dealerId,经销商Id，不为空时查询展示在搜索结果页，终端店可领的该经销商红包和优惠券
    def test_getMoreAvailableCouponSum_dealerId(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,dealerId=self.dealerInfo.companyId)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data'])):
            self.assertEqual(self.dealerInfo.companyId,queryResult['data'][i]['dealerCouponDto']['dealerId'])


    #showWay：展示方式（0：领券中心，1：我的丹露页，2：搜索结果页，3：商品详情页）
    def test_getMoreAvailableCouponSum_benefitShowWay0(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,showWay='0')
        self.assertEqual(queryResult['status'], 0)

    #showWay：展示方式（0：领券中心，1：我的丹露页，2：搜索结果页，3：商品详情页）
    def test_getMoreAvailableCouponSum_benefitShowWayMulti(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,showWay='0,1,2,3')
        self.assertEqual(queryResult['status'], 0)

    #dealerName店铺名称
    def test_getMoreAvailableCouponSum_dealerName(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,dealerName=self.dealerInfo.companyId)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data'])):
            self.assertEqual(queryResult['data'][i]['dealerCouponDto']['dealerName'], '')

    #goodsName商品名称
    def test_getMoreAvailableCouponSum_goodsName(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,goodsName=self.goodsInfo.goodsName)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data'])):
            self.assertEqual(queryResult['data'][i]['dealerCouponDto']['goodsName'],self.goodsInfo.goodsName)

    # goodsId商品Id
    def test_getMoreAvailableCouponSum_goodsId(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,goodsId=self.goodsInfo.goodsId)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data'])):
            self.assertEqual(queryResult['data'][i]['dealerCouponDto']['goodsId'],self.goodsInfo.goodsId)

    # getWayweb平台：0,app平台：1,链接的方式：2
    def test_getMoreAvailableCouponSum_getWay0(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,getWay='0')
        self.assertEqual(queryResult['status'], 0)

    # getWay:web平台：0,app平台：1,链接的方式：2
    def test_getMoreAvailableCouponSum_GetWayMulti(self):
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,getWay='0,1,2')
        self.assertEqual(queryResult['status'], 0)

    # pageIndex    分页参数,pageSize    分页参数
    def test_getMoreAvailableCouponSum_benefitGetWayMulti(self):
        pageSize=random.randint(0,10)
        queryResult=self.dlservice.getMoreAvailableCoupon(session=self.s,pageSize=pageSize,pageIndex=1)
        self.assertEqual(queryResult['status'], 0)
        self.assertLessEqual(len(queryResult['data']), pageSize)

    # sort    排序。默认desc多列排序使用, 分割sort = id，name：asc    --暂时不需要


    #Hook method for deconstructing the class fixture after running all tests in the class.
    # def tearDownClass(self):
    #     print 'tearDown'

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'

def suite():
    suite=unittest.TestSuite()
    # suite.addTest(getMoreAvailableCoupon("test_functions"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_GetWayMulti"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_nullPara"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_benefitGetWayMulti"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_benefitOnlyRequiredPara"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_benefitShowWay0"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_benefitShowWayMulti"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_couponOnlyRequiredPara"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_dealerId"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_dealerName"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_getWay0"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_goodsId"))
    suite.addTest(getMoreAvailableCoupon("test_getMoreAvailableCouponSum_goodsName"))
    return suite
