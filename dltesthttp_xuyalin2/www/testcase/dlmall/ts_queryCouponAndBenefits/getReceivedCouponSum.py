#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.common.excel import *
from www.common.database import *
from www.api.dlmall import *

"""
GET /dealer/getReceivedCouponSum.html
{
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "dealerId": dealerId
        }
返回：
  {
    "data": {
      "isUsedNum": 0,
      "unUsedNum": 1,
      "expired": 2,
    },
    "status": 0,
    "msg":"查询成功"
  }
"""


class getReceivedCouponSum(unittest.TestCase):
    companyInfo = eData('ReceivedCouponsBenefits')
    #dlservice = dlpromotionx()
    dlservice = dlmall()
    s = dlservice.login('testzwq', 123456)

    #查询已领取的红包个数
    def test_getReceivedCouponSum_couponOnlyRequiredPara(self):
        queryResult=self.dlservice.getReceivedCouponSum(self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10')
        #print queryResult
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['isUsedNum'],0)
        self.assertGreaterEqual(queryResult['data']['unUsedNum'], 0)
        self.assertGreaterEqual(queryResult['data']['expired'], 0)
        self.assertEqual(len(queryResult['data']), 3,
                         'data节点中应有3对键值，当前返回' + str(len(queryResult['data'])) + '对')

    #查询已领取的优惠券个数
    def test_getReceivedCouponSum_benefitOnlyRequiredPara(self):
        queryResult=self.dlservice.getReceivedCouponSum(self.s,companyId=self.companyInfo.companyId1,dealerCouponType='11')
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['isUsedNum'],0)
        self.assertGreaterEqual(queryResult['data']['unUsedNum'], 0)
        self.assertGreaterEqual(queryResult['data']['expired'], 0)

    #查询已领取的某经销商的红包个数
    def test_getReceivedCouponSum_couponWithDealerId(self):
        queryResult=self.dlservice.getReceivedCouponSum(self.s,companyId=self.companyInfo.companyId1,dealerCouponType='10',dealerId=self.companyInfo.DealerID1)
        #print queryResult
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['isUsedNum'],0)
        self.assertGreaterEqual(queryResult['data']['unUsedNum'], 0)
        self.assertGreaterEqual(queryResult['data']['expired'], 0)

    # 查询已领取的某经销商的优惠券个数
    def test_getReceivedCouponSum_benefitWithDealerId(self):
        queryResult = self.dlservice.getReceivedCouponSum(self.s,companyId=self.companyInfo.companyId1, dealerCouponType='11',dealerId=self.companyInfo.DealerID1)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['msg'], u'查询成功')
        self.assertGreaterEqual(queryResult['data']['isUsedNum'], 0)
        self.assertGreaterEqual(queryResult['data']['unUsedNum'], 0)
        self.assertGreaterEqual(queryResult['data']['expired'], 0)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'

def suite():
    suite=unittest.TestSuite()
    #suite.addTest(getReceivedCouponSum("test_functions"))
    suite.addTest(getReceivedCouponSum("test_getReceivedCouponSum_couponOnlyRequiredPara"))
    suite.addTest(getReceivedCouponSum("test_getReceivedCouponSum_benefitWithDealerId"))
    suite.addTest(getReceivedCouponSum("test_getReceivedCouponSum_couponOnlyRequiredPara"))
    suite.addTest(getReceivedCouponSum("test_getReceivedCouponSum_couponWithDealerId"))
    return suite


