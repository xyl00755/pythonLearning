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
class queryDealerBenefitUsedOnMall(unittest.TestCase):

    UsedDealerBenefitInfo = eData('UsedDealerBenefit')
    dlservice = dldata()
    StartTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple())))  # 30天前的时间
    EndTime = time.strftime('%Y-%m-%d %X', time.localtime(
        time.mktime((datetime.datetime.now() - datetime.timedelta(days=3)).timetuple())))  # 3天前的时间

    #入参为空时不可以查询到优惠券
    def test_queryDealerBenefitUsed_nullPara(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall()
        self.assertEqual(queryResult['status'], -1)


    #sellerID必填
    def test_queryDealerBenefitUsed_onlyRequired(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(sellerId=self.UsedDealerBenefitInfo.sellerId)
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
        self.assertIn('logicDeleteFlg', queryResult['data']['result'][0].keys(), 'result中券信息没有 logicDeleteFlg')
        self.assertIn('payerAreaName', queryResult['data']['result'][0].keys(), 'result中券信息没有 payerAreaName')
        self.assertIn('sellerAreaName', queryResult['data']['result'][0].keys(), 'result中券信息没有 sellerAreaName')
        self.assertIn('total', queryResult['data'].keys(), 'result中券信息没有 total')
        self.assertGreaterEqual(len(queryResult['data']['result'][0]), 22, 'result中每张券应至少有22对键值，当前返回' + str(len(queryResult['data']['result'][0])) + '对')


    #根据couponEntityId查询到唯一的一个优惠券,
    def test_queryDealerBenefitUsed_couponEntityId(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(self.UsedDealerBenefitInfo.couponEntityId,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        self.assertEqual(len(queryResult['data']['result']),1,'结果唯一')
        self.assertEqual(queryResult['data']['result'][0]['couponEntityId'],self.UsedDealerBenefitInfo.couponEntityId)

    #根据couponId精确查询到优惠券
    def test_queryDealerBenefitUsed_couponId_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponId=self.UsedDealerBenefitInfo.couponId,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0,len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponId'],str(self.UsedDealerBenefitInfo.couponId))

    #根据couponId模糊查询到优惠券,
    def test_queryDealerBenefitUsed_couponId_fuzzy(self):
        #self.UsedDealerBenefitInfo.couponId[2:6] 表示取excel中coupon从第二位到第五位字符串切片
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponId=self.UsedDealerBenefitInfo.couponId[2:6],sellerId=self.UsedDealerBenefitInfo.sellerId,
                                                                pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
                self.assertIn(str(self.UsedDealerBenefitInfo.couponId[2:6]),queryResult['data']['result'][i]['couponId'],queryResult['data']['result'][i]['couponId']+' shouldn\'t be quried out')


    #根据couponName精确查询到优惠券,
    def test_queryDealerBenefitUsed_couponName_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponName=self.UsedDealerBenefitInfo.couponName,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponName'].encode("UTF-8"),self.UsedDealerBenefitInfo.couponName)

    #根据couponName模糊查询到优惠券,
    def test_queryDealerBenefitUsed_couponName_fuzzy(self):
        s = self.UsedDealerBenefitInfo.couponName.decode('utf-8')[1:3].encode('utf-8')
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponName=s,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
                self.assertIn(s,queryResult['data']['result'][i]['couponName'],queryResult['data']['result'][i]['couponName']+' shouldn\'t be quried out')

    #根据payerName精确查询到优惠券
    def test_queryDealerBenefitUsed_payerName_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(payerName=self.UsedDealerBenefitInfo.payerName,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['payerName'].encode("UTF-8"), self.UsedDealerBenefitInfo.payerName)

    #根据payerName模糊查询到优惠券
    def test_queryDealerBenefitUsed_payerName_fuzzy(self):
        s = self.UsedDealerBenefitInfo.payerName.decode('utf-8').encode('utf-8')
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(payerName=s,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertIn(s, queryResult['data']['result'][i]['payerName'].encode("UTF-8"),
                          queryResult['data']['result'][i]['payerName'] + ' shouldn\'t be quried out')

    #根据sellerName精确查询到优惠券
    def test_queryDealerBenefitUsed_sellerName_accurate(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(sellerName=self.UsedDealerBenefitInfo.sellerName,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['sellerName'].encode("UTF-8"), self.UsedDealerBenefitInfo.sellerName)

    #根据sellerName模糊查询到优惠券
    def test_queryDealerBenefitUsed_sellerName_fuzzy(self):
        s = self.UsedDealerBenefitInfo.sellerName.decode('utf-8')[1:3].encode('utf-8')
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(sellerName=s,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertIn(s, queryResult['data']['result'][i]['sellerName'].encode("UTF-8"),
                          queryResult['data']['result'][i]['sellerName'] + ' shouldn\'t be quried out')

    #根据sellerId查询到优惠券
    def test_queryDealerBenefitUsed_sellerId(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['sellerId'], self.UsedDealerBenefitInfo.sellerId)

    #根据orderNo查询到优惠券
    def test_queryDealerBenefitUsed_orderNo(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(orderNo=self.UsedDealerBenefitInfo.orderNo,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['orderNo'], self.UsedDealerBenefitInfo.orderNo)

    #根据couponUseFlg查询到优惠券
    def test_queryDealerBenefitUsed_couponUseFlg(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponUseFlg=self.UsedDealerBenefitInfo.couponUseFlg,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponUseFlg'], self.UsedDealerBenefitInfo.couponUseFlg)

    #根据orderStatus查询到优惠券
    def test_queryDealerBenefitUsed_orderStatus(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(orderStatus=self.UsedDealerBenefitInfo.orderStatus,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['orderStatus'], self.UsedDealerBenefitInfo.orderStatus)

    #根据couponUseStartTime查询到优惠券
    def test_queryDealerBenefitUsed_couponUseStartTime(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponUseStartTime=self.StartTime,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertGreaterEqual(queryResult['data']['result'][i]['couponUseTime'],
                                    self.StartTime)

    #根据couponUseEndTime查询到优惠券
    def test_queryDealerBenefitUsed_couponUseEndTime(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponUseEndTime=self.EndTime,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertLessEqual(queryResult['data']['result'][i]['couponUseTime'],
                                 self.EndTime)
        #self.assertEqual(queryResult['data']['result'][0]['couponUseEndTime'],self.UsedDealerBenefitInfo.couponUseEndTime)

    #根据couponReceiveStartTime查询到优惠券
    def test_queryDealerBenefitUsed_couponReceiveStartTime(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(couponReceiveStartTime=self.StartTime,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertGreaterEqual(queryResult['data']['result'][i]['couponReceiveTime'],
                                    self.StartTime)

    #根据couponReceiveEndTime查询到优惠券
    def test_queryDealerBenefitUsed_couponReceiveEndTime(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(
            couponReceiveEndTime=self.EndTime,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1, pageSize=10)
        self.assertEqual(queryResult['status'], 0)
        for i in range(0, len(queryResult['data']['result'])):
            self.assertLessEqual(queryResult['data']['result'][i]['couponReceiveTime'],
                                 self.EndTime)

    #验证查询到优惠券sort正确
    def test_queryDealerBenefitUsed_sort(self):
        queryResult=self.dlservice.queryDealerBenefitUsedOnMall(sort=self.UsedDealerBenefitInfo.sort,sellerId=self.UsedDealerBenefitInfo.sellerId,pageIndex=1,pageSize=10)
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
    # suite.addTest(queryDealerBenefitUsedOnMall("test_functions"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponEntityId"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponId_accurate"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponId_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponName_accurate"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponName_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponReceiveEndTime"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponReceiveStartTime"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponUseEndTime"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponUseFlg"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_couponUseStartTime"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_nullPara"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_onlyRequired"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_orderNo"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_orderStatus"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_payerName_accurate"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_payerName_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_sellerId"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_sellerName_accurate"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_sellerName_fuzzy"))
    suite.addTest(queryDealerBenefitUsedOnMall("test_queryDealerBenefitUsed_sort"))
    return suite
