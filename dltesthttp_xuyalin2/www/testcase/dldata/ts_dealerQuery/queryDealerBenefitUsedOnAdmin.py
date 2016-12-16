#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest,datetime,time
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
   "couponReceiveEndTime" : "2016-09-30",
   "sort" : "id:asc,name:desc",
   "pageIndex" : 1,
   "pageSize" : 10
}

"""
class queryDealerBenefitUsedOnAdmin(unittest.TestCase):

    UsedDealerBenefitInfo = eData('UsedDealerBenefit')
    dlservice = dldata()
    StartTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple())))  # 30天前的时间
    EndTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=3)).timetuple())))  # 3天前的时间


    #入参为空时可以查询到优惠券
    def test_queryDealerBenefitUsed_nullPara(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin()
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

    #根据couponEntityId查询到唯一的一个优惠券,
    def test_queryDealerBenefitUsed_couponEntityId(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(self.UsedDealerBenefitInfo.couponEntityId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(len(queryResult['data']['result']),1,'结果唯一')
        self.assertEqual(queryResult['data']['result'][0]['couponEntityId'],self.UsedDealerBenefitInfo.couponEntityId)

    #根据couponId精确查询到优惠券
    def test_queryDealerBenefitUsed_couponId_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponId=self.UsedDealerBenefitInfo.couponId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponId'],str(self.UsedDealerBenefitInfo.couponId))

    #根据couponId模糊查询到优惠券,
    def test_queryDealerBenefitUsed_couponId_fuzzy(self):
        #self.UsedDealerBenefitInfo.couponId[2:6] 表示取excel中coupon从第二位到第五位字符串切片
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponId=self.UsedDealerBenefitInfo.couponId[2:6],pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
                self.assertIn(str(self.UsedDealerBenefitInfo.couponId[2:6]),queryResult['data']['result'][i]['couponId'],queryResult['data']['result'][i]['couponId']+' shouldn\'t be quried out')


    #根据couponName精确查询到优惠券,
    def test_queryDealerBenefitUsed_couponName_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponName=self.UsedDealerBenefitInfo.couponName,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponName'].encode("UTF-8"),self.UsedDealerBenefitInfo.couponName)

    #根据couponName模糊查询到优惠券,
    def test_queryDealerBenefitUsed_couponName_fuzzy(self):
        s = self.UsedDealerBenefitInfo.couponName.decode('utf-8')[1:3].encode('utf-8')
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponName=s,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
                self.assertIn(s,queryResult['data']['result'][i]['couponName'],queryResult['data']['result'][i]['couponName']+' shouldn\'t be quried out')

    #根据payerName精确查询到优惠券
    def test_queryDealerBenefitUsed_payerName_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(payerName=self.UsedDealerBenefitInfo.payerName,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['payerName'].encode("UTF-8"), self.UsedDealerBenefitInfo.payerName)

    #根据payerName模糊查询到优惠券
    def test_queryDealerBenefitUsed_payerName_fuzzy(self):
        s = self.UsedDealerBenefitInfo.payerName.decode('utf-8').encode('utf-8')
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(payerName=s,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertIn(s, queryResult['data']['result'][i]['payerName'].encode("UTF-8"),
                          queryResult['data']['result'][i]['payerName'] + ' shouldn\'t be quried out')

    #根据sellerName精确查询到优惠券
    def test_queryDealerBenefitUsed_sellerName_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(sellerName=self.UsedDealerBenefitInfo.sellerName,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['sellerName'].encode("UTF-8"), self.UsedDealerBenefitInfo.sellerName)

    #根据sellerName模糊查询到优惠券
    def test_queryDealerBenefitUsed_sellerName_fuzzy(self):
        s = self.UsedDealerBenefitInfo.sellerName.decode('utf-8')[1:3].encode('utf-8')
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(sellerName=s,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertIn(s, queryResult['data']['result'][i]['sellerName'].encode("UTF-8"),
                          queryResult['data']['result'][i]['sellerName'] + ' shouldn\'t be quried out')

    #根据sellerId查询到优惠券
    def test_queryDealerBenefitUsed_sellerId(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['sellerId'], self.UsedDealerBenefitInfo.sellerId)

    #根据orderNo查询到优惠券
    def test_queryDealerBenefitUsed_orderNo(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(orderNo=self.UsedDealerBenefitInfo.orderNo,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['orderNo'], self.UsedDealerBenefitInfo.orderNo)

    #根据couponUseFlg查询到优惠券
    def test_queryDealerBenefitUsed_couponUseFlg(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponUseFlg=self.UsedDealerBenefitInfo.couponUseFlg,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponUseFlg'], self.UsedDealerBenefitInfo.couponUseFlg)

    #根据orderStatus查询到优惠券
    def test_queryDealerBenefitUsed_orderStatus(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(orderStatus=self.UsedDealerBenefitInfo.orderStatus,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['orderStatus'], self.UsedDealerBenefitInfo.orderStatus)

    #根据couponUseStartTime查询到优惠券
    def test_queryDealerBenefitUsed_couponUseStartTime(self):
        couponUseStartTime = self.StartTime
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponUseStartTime=couponUseStartTime,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertGreaterEqual(queryResult['data']['result'][i]['couponUseTime'],
                                    couponUseStartTime)

    #根据couponUseEndTime查询到优惠券
    def test_queryDealerBenefitUsed_couponUseEndTime(self):
        couponUseEndTime = self.EndTime
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponUseEndTime=couponUseEndTime,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertLessEqual(queryResult['data']['result'][i]['couponUseTime'],
                                 couponUseEndTime)
        #self.assertEqual(queryResult['data']['result'][0]['couponUseEndTime'],self.UsedDealerBenefitInfo.couponUseEndTime)

    #根据couponReceiveStartTime查询到优惠券
    def test_queryDealerBenefitUsed_couponReceiveStartTime(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(couponReceiveStartTime=self.StartTime,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertGreaterEqual(queryResult['data']['result'][i]['couponReceiveTime'],
                                    self.StartTime)

    #根据couponReceiveEndTime查询到优惠券
    def test_queryDealerBenefitUsed_couponReceiveEndTime(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(
            couponReceiveEndTime=self.EndTime,pageIndex=1, pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertLessEqual(queryResult['data']['result'][i]['couponReceiveTime'],
                                 self.EndTime)

    #验证查询到优惠券page正确
    def test_queryDealerBenefitUsed_sort(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnAdmin(sort=self.UsedDealerBenefitInfo.sort,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(queryResult['data']['pageIndex'], 1)
        self.assertEqual(queryResult['data']['pageSize'], 10)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'


def suite():
    suite=unittest.TestSuite()
    #suite.addTest(queryDealerBenefitUsedOnAdmin("test_functions"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponEntityId"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponId_accurate"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponId_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponName_accurate"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponName_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponReceiveEndTime"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponReceiveStartTime"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponUseEndTime"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponUseFlg"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_couponUseStartTime"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_nullPara"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_orderNo"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_orderStatus"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_payerName_accurate"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_payerName_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_sellerId"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_sellerName_accurate"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_sellerName_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnAdmin("test_queryDealerBenefitUsed_sort"))
    return suite
