#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
GET /dealer/getReceivedCoupon.html
{
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "dealerCouponEntityStatus": dealerCouponEntityStatus,
            "dealerIdList": dealerIdList,
            "goodsId": goodsId,
            "pageIndex": pageIndex,
            "pageSize": pageSize,
            "sort": sort
        }
返回：
  {
    "status": 0,
    "data": {
        "data_list":[
            {
                "dealerCouponEntityId":"asa",
                "dealerCouponEntityStatus":"01",
                "dealerCouponId":"a123",
                "dealerCouponName":"优惠券1",
                "dealerCouponType":"10",
                "dealerName":"河北人人大",
                "dealerId":"abc",
                "dealerCouponImgUrl":"http://www.baidu.com/img.jpg",
                "dealerCouponAmount":213,
                "effectiveTime":"12321321212",
                "uneffectiveTime":"12312312312",
                "availableChannel":"S011,S012",
                "goodsId":"1232",
                "goodsName":"国窖1753 500mL",
                "areaLimit":"code1,code2",
                "platformLimit":"WEB",
                "effectiveAmount":154,
                "orderNo":"bcd",
                "activityId":"abc",
                "goodsFlag":true,
                "effectivityStatus":"01"
            },
        ]
        "index":3,
        "size":2,
        "total":5,
    },
    "msg":"查询成功"
  }
"""


class getReceivedCoupon(unittest.TestCase):
    companyInfo=eData('ReceivedCouponsBenefits')
    UserShop=wsData('DealMager')
    TmlShop=wsData('TmlShop')
    dlservice = dlmall()
    #s = dlservice.login(UserShop.username, UserShop.password)
    s = dlservice.login('testatzdd01', "Danlu99")

    #直接手工构造 领取红包、优惠券
    # def setUp(self):
    #     print 'setUp'

    #仅用必填字段查询红包
    def test_getReceivedCoupon_couponOnlyRequiredPara(self):
        queryResult=self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10')
        # print queryResult
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(len(queryResult['data']['data_list'][0]), 25, 'data节点中应有25对键值，当前返回' + str(len(queryResult['data']['data_list'][0])) + '对')
        self.assertIn('dealerCouponEntityId', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerCouponEntityStatus', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerCouponId', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerName', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerId', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerCouponImgUrl', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerCouponAmount', queryResult['data']['data_list'][0].keys())
        self.assertIn('uneffectiveTime', queryResult['data']['data_list'][0].keys())
        self.assertIn('availableChannel', queryResult['data']['data_list'][0].keys())
        self.assertIn('goodsId', queryResult['data']['data_list'][0].keys())
        self.assertIn('goodsName', queryResult['data']['data_list'][0].keys())
        self.assertIn('areaLimit', queryResult['data']['data_list'][0].keys())
        self.assertIn('platformLimit', queryResult['data']['data_list'][0].keys())
        self.assertIn('effectiveAmount', queryResult['data']['data_list'][0].keys())
        self.assertIn('orderNo', queryResult['data']['data_list'][0].keys())
        self.assertIn('dealerActivityId', queryResult['data']['data_list'][0].keys())
        self.assertIn('goodsFlag', queryResult['data']['data_list'][0].keys())
        self.assertIn('effectivityStatus', queryResult['data']['data_list'][0].keys())
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponType'], '10')

    # 用dealerCouponEntityStatus字段查询未使用红包
    def test_getReceivedCoupon_dealerCouponEntityStatus01	(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='10',dealerCouponEntityStatus='01')
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponEntityStatus'], '01')

    # 用dealerCouponEntityStatus字段查询已使用红包
    def test_getReceivedCoupon_dealerCouponEntityStatus02(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='10',
                                                           dealerCouponEntityStatus='02')
        #print queryResult
        if queryResult['data']['data_list'] != None:
            for i in range(0, len(queryResult['data']['data_list'])):
                self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponEntityStatus'], '02')
        else:
            self.assertEqual(queryResult['data']['data_list'],None)



    # 用dealerCouponEntityStatus字段查询已过期红包
    def test_getReceivedCoupon_dealerCouponEntityStatus04(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='10',dealerCouponEntityStatus='04')
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponEntityStatus'], '04')
            self.assertLess(queryResult['data']['data_list'][i]['uneffectiveTime'],time.strftime('%Y-%m-%d %X', time.localtime()))

    #仅用必填字段查询优惠券
    def test_getReceivedCoupon_benefitOnlyRequiredPara(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11')
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponType'], '11')

    # 用dealerCouponEntityStatus字段查询未使用优惠券
    def test_getReceivedCoupon_dealerBenefitEntityStatus01	(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',dealerCouponEntityStatus='01')
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponEntityStatus'], '01')

    # 用dealerCouponEntityStatus字段查询已使用优惠券
    def test_getReceivedCoupon_dealerBenefitEntityStatus02(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',
                                                           dealerCouponEntityStatus='02')
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponEntityStatus'], '02')

    # 用dealerCouponEntityStatus字段查询已过期优惠券
    def test_getReceivedCoupon_dealerBenefitEntityStatus04(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',dealerCouponEntityStatus='04')
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['dealerCouponEntityStatus'], '04')
            self.assertLess(queryResult['data']['data_list'][i]['uneffectiveTime'],time.strftime('%Y-%m-%d %X', time.localtime()))

    #检查红包pageIndex，pageSize
    def test_getReceivedCoupon_couponPages(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='10',pageIndex=1,pageSize=4)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['data']['index'], 1)
        self.assertEqual(queryResult['data']['size'], 4)
        self.assertLessEqual(queryResult['data']['total'], 4)

    #检查优惠券pageIndex，pageSize
    def test_getReceivedCoupon_BenefitPages(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',pageIndex=1,pageSize=4)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['data']['index'], 1)
        self.assertEqual(queryResult['data']['size'], 4)
        self.assertLessEqual(queryResult['data']['total'], 4)

    #goodsFlag检查该优惠券该商品是否有效
    def test_getReceivedCoupon_BenefitgoodsFlag(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',goodsId=self.companyInfo.goodsID)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['data_list'])):
            if queryResult['data']['data_list'][i]['dealerCouponEntityId']==self.companyInfo.dealerCouponEntityId1:
                self.assertLess(queryResult['data']['data_list'][i]['goodsFlag'],'true')
            elif queryResult['data']['data_list'][i]['dealerCouponEntityId']==self.companyInfo.dealerCouponEntityId2:
                self.assertLess(queryResult['data']['data_list'][i]['goodsFlag'], 'false')

    #用goodsId字段查询优惠券
    def test_getReceivedCoupon_benefitGoodsId(self):
        queryResult = self.dlservice.getReceivedCoupon(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',goodsId=self.companyInfo.goodsID)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['data_list'])):
            self.assertEqual(queryResult['data']['data_list'][i]['goodsId'], self.companyInfo.goodsID)

    #用例执行完成后的操作
    # def tearDown(self):
    #     print 'tearDown'


def suite():
    suite=unittest.TestSuite()
    #suite.addTest(getReceivedCoupon("test_functions"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_BenefitPages"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_BenefitgoodsFlag"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_benefitGoodsId"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_benefitOnlyRequiredPara"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_couponOnlyRequiredPara"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_couponPages"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_dealerBenefitEntityStatus01"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_dealerBenefitEntityStatus02"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_dealerBenefitEntityStatus04"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_dealerCouponEntityStatus01"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_dealerCouponEntityStatus02"))
    suite.addTest(getReceivedCoupon("test_getReceivedCoupon_dealerCouponEntityStatus04"))
    return suite

