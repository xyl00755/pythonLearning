#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest,time,datetime
from www.api.dldata import *
from www.common.excel import *
#from www.common.database import *

"""
POST
    {
        "couponEntityId" : "0001210212",
        "couponId" : "1002012",
        "couponName" : "测试经销商优惠劵",
        "payerName" : "testzwq的终端店",
        "sellerName" : "testyuxi冒烟测试经销商",
        "sellerId" : "60984ad4c5844cf9b46eb86d551e323b",
        "couponUseFlg" : "1",
        "orderStatus" : "C019",
        "couponUseStartTime" : "2016-09-05",
        "couponUseEndTime" : "2016-09-10",
        "couponReceiveStartTime" : "2016-09-01",
        "couponReceiveEndTime" : "2016-09-30"
    }
response:
   {
    "status": 0,
    "msg":"",
    "data": {
        "grantAmt":10000,
        "discountAmt":6000,
    }
  }
"""

class queryDealerBenefitTotalAmtOnMall(unittest.TestCase):
    UsedDealerCouponInfo = eData('UsedDealerBenefit')
    dlservice = dldata()
    StartTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=100)).timetuple())))  # 30天前的时间
    EndTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=3)).timetuple())))  # 3天前的时间

    #入参为空时不可查询，sellerId必填
    def test_queryDealerBenefitTotalAmtOnMall_nullPara(self):
        queryResult=self.dlservice.queryDealerBenefitTotalAmtOnMall()
        self.assertEqual(queryResult['status'], -1)
        self.assertEqual(queryResult['msg'], u'sellerId不能为空.')

      #sellerId必填
    def test_queryDealerBenefitTotalAmtOnMall_onlyRequired(self):
        queryResult=self.dlservice.queryDealerBenefitTotalAmtOnMall(sellerId=self.UsedDealerCouponInfo.sellerId)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(len(queryResult['data']), 3, 'data节点中应有3对键值，当前返回' + str(len(queryResult['data'])) + '对')
        self.assertGreaterEqual(queryResult['data']['grantAmt'],0)
        self.assertGreaterEqual(queryResult['data']['grantNum'], 0)
        self.assertGreaterEqual(queryResult['data']['discountAmt'], 0)

    #入参完整时查询到所有红包
    def test_queryDealerBenefitTotalAmtOnMall_AllPara(self):
        couponUseStartTime = self.StartTime
        couponUseEndTime = self.EndTime
        couponReceiveStartTime = self.StartTime
        couponReceiveEndTime = self.EndTime
        queryResult=self.dlservice.queryDealerBenefitTotalAmtOnMall(couponEntityId=self.UsedDealerCouponInfo.couponEntityId,
                                                              couponId= self.UsedDealerCouponInfo.couponId,couponName= self.UsedDealerCouponInfo.couponName,
                                                              payerName= self.UsedDealerCouponInfo.payerName,sellerName= self.UsedDealerCouponInfo.sellerName,
                                                              sellerId= self.UsedDealerCouponInfo.sellerId,orderNo= self.UsedDealerCouponInfo.orderNo,
                                                              couponUseFlg= self.UsedDealerCouponInfo.couponUseFlg,orderStatus= self.UsedDealerCouponInfo.orderStatus,
                                                              couponUseStartTime= couponUseStartTime,couponUseEndTime= couponUseEndTime,
                                                              couponReceiveStartTime= couponReceiveStartTime,couponReceiveEndTime= couponReceiveEndTime
                                                              )
        self.assertEqual(queryResult['status'], 0)
        self.assertGreaterEqual(queryResult['data']['grantAmt'],0)
        self.assertGreaterEqual(queryResult['data']['grantNum'], 0)
        self.assertGreaterEqual(queryResult['data']['discountAmt'], 0)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'


def suite():
    suite=unittest.TestSuite()
    #suite.addTest(queryDealerBenefitTotalAmtOnMall("test_functions"))
    suite.addTest(queryDealerBenefitTotalAmtOnMall("test_queryDealerBenefitTotalAmtOnMall_nullPara"))
    suite.addTest(queryDealerBenefitTotalAmtOnMall("test_queryDealerBenefitTotalAmtOnMall_onlyRequired"))
    suite.addTest(queryDealerBenefitTotalAmtOnMall("test_queryDealerBenefitTotalAmtOnMall_AllPara"))
    return suite
