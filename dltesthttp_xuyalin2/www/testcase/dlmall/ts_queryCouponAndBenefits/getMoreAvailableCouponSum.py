#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
GET dlmall/dealer/getMoreAvailableCouponSum.html
{
	"companyId": companyId,
	"dealerCouponType": dealerCouponType,
	"showWay": showWay,
	"goodsId": goodsId,
	"dealerId": dealerId,
	"getWay": getWay
}
{
  "data": {
      "benefitNum":"5",
      "couponNum":"10"
  }
   "status": 0,
   "msg":"查询成功"
}
"""


class getMoreAvailableCouponSum(unittest.TestCase):
    companyInfo = eData('ReceivedCouponsBenefits')
    dlservice = dlmall()
    s = dlservice.login('testatzdd01', 'Danlu99')

    # 查询可以领取的红包&优惠券个数
    def test_getMoreAvailableCouponSum_nullPara(self):
        queryResult = self.dlservice.getMoreAvailableCouponSum(session=self.s)
        # self.assertEqual(queryResult['status'], 0)
        # self.assertEqual(queryResult['msg'], '查询失败')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        self.assertGreaterEqual(queryResult['data']['couponNum'], 0)


    #查询可以领取的红包个数
    def test_getMoreAvailableCouponSum_couponOnlyRequiredPara(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertGreaterEqual(queryResult['data']['couponNum'], 0)

    #展示方式（0：领券中心，1：我的丹露页，2：搜索结果页，3：商品详情页）
    def test_getMoreAvailableCouponSum_couponShowWay0(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10',showWay='0')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        # self.assertEqual(queryResult['data']['benefitNum'],0)
        self.assertGreaterEqual(queryResult['data']['couponNum'], 0)

    #展示方式（0：领券中心，1：我的丹露页，2：搜索结果页，3：商品详情页）
    def test_getMoreAvailableCouponSum_couponShowWayMulti(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10',showWay='0,1,2,3')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        # self.assertEqual(queryResult['data']['benefitNum'],0)
        self.assertGreaterEqual(queryResult['data']['couponNum'], 0)

    #经销商Id，Id不为空时，查询搜索结果页该终端店可领红包个数
    def test_getMoreAvailableCouponSum_couponDealerId(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10',dealerId=self.companyInfo.DealerID1)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        # self.assertEqual(queryResult['data']['benefitNum'],0)
        self.assertGreaterEqual(queryResult['data']['couponNum'], 0)

    #getWay:web平台：0 app平台：1 链接的方式：2
    def test_getMoreAvailableCouponSum_couponGetWay0(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10',getWay='0')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        # self.assertEqual(queryResult['data']['benefitNum'],0)
        self.assertGreaterEqual(queryResult['data']['couponNum'], 0)

    #getWay:web平台：0 app平台：1 链接的方式：2
    def test_getMoreAvailableCouponSum_couponGetWayMulti(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10',getWay='0,1,2')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        # self.assertEqual(queryResult['data']['benefitNum'],0)
        self.assertGreaterEqual(queryResult['data']['couponNum'], 0)

    #查询可以领取的优惠券个数
    def test_getMoreAvailableCouponSum_benefitOnlyRequiredPara(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertEqual(queryResult['data']['couponNum'], 0)

    #展示方式（0：领券中心，1：我的丹露页，2：搜索结果页，3：商品详情页）
    def test_getMoreAvailableCouponSum_benefitShowWay0(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11',showWay='0')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertEqual(queryResult['data']['couponNum'], 0)

    #展示方式（0：领券中心，1：我的丹露页，2：搜索结果页，3：商品详情页）
    def test_getMoreAvailableCouponSum_benefitShowWayMulti(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11',showWay='0,1,2,3')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertEqual(queryResult['data']['couponNum'], 0)

    #经销商Id，Id不为空时，查询搜索结果页该终端店可领优惠券个数
    def test_getMoreAvailableCouponSum_benefitDealerId(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11',dealerId=self.companyInfo.DealerID1)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertEqual(queryResult['data']['couponNum'], 0)

    #优惠券getWay:web平台：0 app平台：1 链接的方式：2
    def test_getMoreAvailableCouponSum_benefitGetWay0(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11',getWay='0')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertEqual(queryResult['data']['couponNum'], 0)

    #优惠券getWay:web平台：0 app平台：1 链接的方式：2
    def test_getMoreAvailableCouponSum_benefitGetWayMulti(self):
        queryResult=self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11',getWay='0,1,2')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['benefitNum'],0)
        # self.assertEqual(queryResult['data']['couponNum'], 0)

    #商品Id不为空时，查询商品详情页该商品可领优惠券个数
    def test_getMoreAvailableCouponSum_benefitGoodsId(self):
        def test_getMoreAvailableCouponSum_benefitGetWayMulti(self):
            queryResult = self.dlservice.getMoreAvailableCouponSum(session=self.s,companyId=self.companyInfo.companyId1,goodsId=self.companyInfo.goodsID)
            self.assertEqual(queryResult['status'], 0)
            self.assertEqual(queryResult['msg'], u'查询成功')
            self.assertGreaterEqual(queryResult['data']['benefitNum'], 0)
            # self.assertEqual(queryResult['data']['couponNum'], 0)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'

def suite():
    suite=unittest.TestSuite()
    # suite.addTest(getMoreAvailableCouponSum("test_functions"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitDealerId"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitGetWay0"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitGetWayMulti"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitGoodsId"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitOnlyRequiredPara"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitShowWay0"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_benefitShowWayMulti"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_couponDealerId"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_couponGetWay0"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_couponGetWayMulti"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_couponOnlyRequiredPara"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_couponShowWay0"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_couponShowWayMulti"))
    suite.addTest(getMoreAvailableCouponSum("test_getMoreAvailableCouponSum_nullPara"))

    return suite
