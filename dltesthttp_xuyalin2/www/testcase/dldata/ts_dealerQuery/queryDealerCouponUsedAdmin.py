#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time
import datetime
from www.api.dldata import *
from www.common.excel import *
#from www.common.database import *

"""
POST
http://data.danlu.com/V1/dealer_coupon
 {
    "couponEntityId" : "0001210212",
    "couponId" : "1002012",
    "couponName" : "测试经销商红包",
    "payerName" : "testzwq的终端店",
    "sellerName" : "testyuxi冒烟测试经销商",
    "sellerId" : "60984ad4c5844cf9b46eb86d551e323b",
    "couponUseFlg" : "1",
    "orderStatus" : "C019",
    "couponUseStartTime" : "2016-09-05",
    "couponUseEndTime" : "2016-09-10",
    "couponReceiveStartTime" : "2016-09-01",
    "couponReceiveEndTime" : "2016-09-30",
    "sort" : "id:asc,name:desc",
    "pageIndex" : 1,
    "pageSize" : 10
}
"""


class queryDealerCouponUsedAdmin(unittest.TestCase):

    UsedDealerCouponInfo = eData('UsedDealerCoupon')
    dlservice = dldata()
    StartTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple())))  # 30天前的时间
    EndTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=3)).timetuple())))  # 3天前的时间

    #入参为空时可以查询到红包,
    def test_queryDealerCouponUsed_nullPara(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin()
        self.assertEqual(queryResult['status'], 0)
        self.assertIn('payerId', queryResult['data']['result'][0].keys(),'result中券信息没有 payerId')
        self.assertIn('payNo', queryResult['data']['result'][0].keys(), 'result中券信息没有 payNo')
        self.assertIn('couponTypeId', queryResult['data']['result'][0].keys(), 'result中券信息没有 couponTypeId')
        self.assertIn('promotionId', queryResult['data']['result'][0].keys(), 'result中券信息没有 promotionId')
        self.assertIn('promotionName', queryResult['data']['result'][0].keys(), 'result中券信息没有 promotionName')
        self.assertIn('promotionTypeId', queryResult['data']['result'][0].keys(), 'result中券信息没有 promotionTypeId')
        self.assertIn('couponAmt', queryResult['data']['result'][0].keys(), 'result中券信息没有 couponAmt')
        self.assertIn('discountAmt', queryResult['data']['result'][0].keys(), 'result中券信息没有 discountAmt')
        self.assertIn('couponReceiveTime', queryResult['data']['result'][0].keys(), 'result中券信息没有 couponReceiveTime')
        self.assertIn('couponUseTime', queryResult['data']['result'][0].keys(), 'result中券信息没有 couponUseTime')
        self.assertIn('orderCreateTime', queryResult['data']['result'][0].keys(), 'result中券信息没有 orderCreateTime')
        self.assertIn('orderConfirmTime', queryResult['data']['result'][0].keys(), 'result中券信息没有 orderConfirmTime')
        self.assertIn('logicDeleteFlg', queryResult['data']['result'][0].keys(), 'result中券信息没有 logicDeleteFlg')
        self.assertIn('couponUseFlg', queryResult['data']['result'][0].keys(), 'result中券信息没有 couponUseFlg')
        self.assertIn('payerAreaName', queryResult['data']['result'][0].keys(), 'result中券信息没有 payerAreaName')
        self.assertIn('sellerAreaName', queryResult['data']['result'][0].keys(), 'result中券信息没有 sellerAreaName')
        self.assertIn('total', queryResult['data'].keys(), 'result中券信息没有 total')
        self.assertEqual(len(queryResult['data']['result'][0]), 31, 'result中每张券应有31对键值，当前返回' + str(len(queryResult['data']['result'][0])) + '对')

    #根据couponEntityId查询到唯一的一个红包,
    def test_queryDealerCouponUsed_couponEntityId(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(self.UsedDealerCouponInfo.couponEntityId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['data']['result'][0]['couponEntityId'],self.UsedDealerCouponInfo.couponEntityId)

    #根据couponId精确查询到红包,
    def test_queryDealerCouponUsed_couponId_accurate(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponId=self.UsedDealerCouponInfo.couponId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponId'],str(self.UsedDealerCouponInfo.couponId))


    #根据couponId模糊查询到红包,
    def test_queryDealerCouponUsed_couponId_fuzzy(self):
        #self.UsedDealerCouponInfo.couponId[2:6] 表示取excel中coupon从第二位到第五位字符串切片
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponId=self.UsedDealerCouponInfo.couponId[2:6],pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
                self.assertIn(str(self.UsedDealerCouponInfo.couponId[2:6]),queryResult['data']['result'][i]['couponId'],queryResult['data']['result'][i]['couponId']+' shouldn\'t be quried out')

    #根据couponName精确查询到红包,
    def test_queryDealerCouponUsed_couponName_accurate(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponName=self.UsedDealerCouponInfo.couponName,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponName'].encode("UTF-8"),self.UsedDealerCouponInfo.couponName )

    #根据couponName模糊查询到红包,
    def test_queryDealerCouponUsed_couponName_fuzzy(self):
        s=self.UsedDealerCouponInfo.couponName.decode('utf-8')[1:3].encode('utf-8')
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponName=s
                                                            ,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
                self.assertIn(s ,queryResult['data']['result'][i]['couponName'].encode("UTF-8"),queryResult['data']['result'][i]['couponName'].encode("UTF-8")+' shouldn\'t be quried out')

    #根据payerName精确查询到红包,
    def test_queryDealerCouponUsed_payerName_accurate(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(payerName=self.UsedDealerCouponInfo.payerName,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['payerName'].encode("UTF-8"), self.UsedDealerCouponInfo.payerName )

    #根据payerName模糊查询到红包,
    def test_queryDealerCouponUsed_payerName_fuzzy(self):
        s=self.UsedDealerCouponInfo.payerName.decode('utf-8')[2:4].encode('utf-8')
        queryResult=self.dlservice.queryDealerCouponOnAdmin(s,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertIn(s, queryResult['data']['result'][i]['payerName'].encode("UTF-8"),
                          queryResult['data']['result'][i]['payerName'] + ' shouldn\'t be quried out')


    #根据sellerName精确查询到红包
    def test_queryDealerCouponUsed_sellerName_accurate(self):
        s=self.UsedDealerCouponInfo.sellerName.decode('utf-8').encode('utf-8')
        queryResult=self.dlservice.queryDealerCouponOnAdmin(sellerName=s,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['sellerName'].encode("UTF-8") , s)

    #根据sellerName模糊查询到红包,
    def test_queryDealerCouponUsed_sellerName_fuzzy(self):
        s=self.UsedDealerCouponInfo.sellerName.decode('utf-8')[1:3].encode('utf-8')
        queryResult=self.dlservice.queryDealerCouponOnAdmin(sellerName=s,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertIn(s , queryResult['data']['result'][i]['sellerName'].encode("UTF-8"),
                          queryResult['data']['result'][i]['sellerName'] .encode("UTF-8")+ ' shouldn\'t be quried out')

    #根据sellerId查询到红包,
    def test_queryDealerCouponUsed_sellerId(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(sellerId=self.UsedDealerCouponInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['sellerId'], self.UsedDealerCouponInfo.sellerId)

    #根据orderNo查询到红包,
    def test_queryDealerCouponUsed_orderNo(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(orderNo=self.UsedDealerCouponInfo.orderNo,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['orderNo'], self.UsedDealerCouponInfo.orderNo)

    #根据couponUseFlg查询到红包,
    def test_queryDealerCouponUsed_couponUseFlg(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponUseFlg=self.UsedDealerCouponInfo.couponUseFlg,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponUseFlg'], self.UsedDealerCouponInfo.couponUseFlg)

    #根据orderStatus查询到红包,
    def test_queryDealerCouponUsed_orderStatus(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(orderStatus=self.UsedDealerCouponInfo.orderStatus,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['orderStatus'], self.UsedDealerCouponInfo.orderStatus)

    #根据couponUseStartTime查询到红包,
    def test_queryDealerCouponUsed_couponUseStartTime(self):
        couponUseStartTime=self.StartTime
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponUseStartTime=couponUseStartTime,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        if queryResult['data']['result']!=[]:
            for i in range(0, len(queryResult['data']['result'])):
                self.assertGreaterEqual(queryResult['data']['result'][i]['couponUseTime'],
                                        couponUseStartTime)
        else:
            self.assertEqual(queryResult['data']['total'],0)

    #根据couponUseEndTime查询到红包,
    def test_queryDealerCouponUsed_couponUseEndTime(self):
        couponUseEndTime=self.EndTime
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponUseEndTime=couponUseEndTime,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        if queryResult['data']['result'] != []:
            for i in range(0, len(queryResult['data']['result'])):
                self.assertLessEqual(queryResult['data']['result'][i]['couponUseTime'],
                                     couponUseEndTime)
        else:
             self.assertEqual(queryResult['data']['total'], 0)
        #self.assertEqual(queryResult['data']['result'][0]['couponUseEndTime'],self.UsedDealerCouponInfo.couponUseEndTime)

    #根据couponReceiveStartTime查询到红包,
    def test_queryDealerCouponUsed_couponReceiveStartTime(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(couponReceiveStartTime=self.StartTime,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        if queryResult['data']['result'] != []:
            for i in range(0, len(queryResult['data']['result'])):
                self.assertGreaterEqual(queryResult['data']['result'][i]['couponReceiveTime'],
                                        self.StartTime)
        else:
            self.assertEqual(queryResult['data']['total'], 0)

    #根据couponReceiveEndTime查询到红包,
    def test_queryDealerCouponUsed_couponReceiveEndTime(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(
            couponReceiveEndTime=self.EndTime,pageIndex=1, pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        if queryResult['data']['result'] != []:
            for i in range(0, len(queryResult['data']['result'])):
                self.assertLessEqual(queryResult['data']['result'][i]['couponReceiveTime'],
                                     self.EndTime)
        else:
            self.assertEqual(queryResult['data']['total'], 0)

    #验证查询到红包page正确
    def test_queryDealerCouponUsed_sort(self):
        queryResult=self.dlservice.queryDealerCouponOnAdmin(sort=self.UsedDealerCouponInfo.sort,pageIndex=1,pageSize=4)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['data']['pageIndex'], 1)
        self.assertEqual(queryResult['data']['pageSize'], 4)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'


def suite():
    suite=unittest.TestSuite()
    # suite.addTest(queryDealerCouponUsedAdmin("test_functions"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponEntityId"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponId_accurate"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponId_fuzzy"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponName_accurate"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponName_fuzzy"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponReceiveEndTime"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponReceiveStartTime"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponUseEndTime"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponUseFlg"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_couponUseStartTime"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_nullPara"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_orderNo"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_orderStatus"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_payerName_accurate"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_payerName_fuzzy"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_sellerId"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_sellerName_accurate"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_sellerName_fuzzy"))
    suite.addTest(queryDealerCouponUsedAdmin("test_queryDealerCouponUsed_sort"))
    return suite
