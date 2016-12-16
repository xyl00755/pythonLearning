#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

"""
PUT /dealer/coupon
    {
            'activityType':activityType,
            'dealerCouponIdOrName':dealerCouponIdOrName,
            'activityName':activityName,
            'effectiveTimeBegin':effectiveTimeBegin,
            'effectiveTimeEnd':effectiveTimeEnd,
            'uneffectiveTimeBegin':uneffectiveTimeBegin,
            'uneffectiveTimeEnd':uneffectiveTimeEnd,
            'gmtCreateBegin':gmtCreateBegin,
            'gmtCreateEnd':gmtCreateEnd,
            'dealerName':dealerName,
            'goodsName':goodsName,
            'status':status,
            'sort':sort,
            'pageIndex':pageIndex,
            'pageSize':pageSize
        }
"""

class queryDealerActivity(unittest.TestCase):

    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    dealerInfo = wsData('DealMager')
    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()


    #根据红包名称或者红包id查询到唯一的一个红包,dealerCouponType=10
    def test_queryCoupon_dealerCouponIdOrName(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,dealerCouponIdOrName=self.ReceiveCouponInfo.dealerCouponIdOrName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']),1)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据有效期起始时间查询红包,dealerCouponType=10
    def test_queryCoupon_effectiveTime(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,effectiveTimeBegin=self.ReceiveCouponInfo.effectiveTimeBegin,effectiveTimeEnd=self.ReceiveCouponInfo.effectiveTimeEnd)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据有效结束时间查询红包，dealerCouponType=10
    def test_queryCoupon_uneffectiveTime(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,uneffectiveTimeBegin=self.ReceiveCouponInfo.uneffectiveTimeBegin,uneffectiveTimeEnd=self.ReceiveCouponInfo.uneffectiveTimeEnd)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

     #根据创建时间查询红包,dealerCouponType=10
    def test_queryCoupon_createTime(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,gmtCreateBegin=int(round(time.time())*1000-1000000),gmtCreateEnd=int(round(time.time())*1000)+1000000)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据使用店铺查询红包,dealerCouponType=10
    def test_queryCoupon_dealerName(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,dealerName=self.ReceiveCouponInfo.dealerName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据红包状态查询红包,dealerCouponType=10，创建送红包活动默认的状态为2，未启用
    def test_queryCoupon_status(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,status='2')
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')



    #根据名称或者优惠券id查询到唯一的一个优惠券,dealerCouponType=11
    def test_queryBenefit_dealerCouponName(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,dealerCouponIdOrName=self.ReceiveBenefitInfo.dealerCouponIdOrName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']),1)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据有效期起始时间查询优惠券,dealerCouponType=11
    def test_queryBenefit_effectiveTime(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,effectiveTimeBegin=self.ReceiveBenefitInfo.effectiveTimeBegin,effectiveTimeEnd=self.ReceiveBenefitInfo.effectiveTimeEnd)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据有效结束时间查询优惠券，dealerCouponType=11
    def test_queryBenefit_uneffectiveTime(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,uneffectiveTimeBegin=self.ReceiveBenefitInfo.uneffectiveTimeBegin,uneffectiveTimeEnd=self.ReceiveBenefitInfo.uneffectiveTimeEnd)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

     #根据创建时间查询优惠券,dealerCouponType=11
    def test_queryBenefit_createTime(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,gmtCreateBegin=int(round(time.time())*1000-1000000),gmtCreateEnd=int(round(time.time())*1000)+1000000)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据使用店铺查询优惠券,dealerCouponType=11
    def test_queryBenefit_dealerName(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,dealerName=self.ReceiveBenefitInfo.dealerName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据使用限制查询优惠券,dealerCouponType=11
    def test_queryBenefit_goodsName(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,goodsName=self.ReceiveBenefitInfo.goodsName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据红包状态查询优惠券,dealerCouponType=11
    def test_queryBenefit_status(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,status='2')
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')



    #根据名称或红包id查询的红包不存在,dealerCouponType=10
    def test_queryCoupon_dealerCouponNameNotExist(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,dealerCouponIdOrName=u'测试不存在的经销商活动名称')
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)
        self.assertNotExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据有效期起始时间查询红包不存在,dealerCouponType=10,2016-10-02 17:00:00----2016-10-03 17:00:00
    def test_queryCoupon_effectiveTimeNotExist(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,effectiveTimeBegin='1475398800000',effectiveTimeEnd='1475485200000')
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertNotExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据有效结束时间查询红包不存在，dealerCouponType=10
    def test_queryCoupon_uneffectiveTimeNotExist(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,uneffectiveTimeBegin='1475398800000',uneffectiveTimeEnd='1475485200000')
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertNotExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

     #根据创建时间查询红包不存在,dealerCouponType=10
    def test_queryCoupon_createTimeNotExsit(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,gmtCreateBegin=int(round(time.time())*1000+1000000),gmtCreateEnd=int(round(time.time())*1000+2000000))
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertNotExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据使用店铺查询红包不存在,dealerCouponType=10
    def test_queryCoupon_dealerNameNotExist(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,dealerName=self.dealerInfo.fullName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertNotExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据红包状态查询红包不存在,dealerCouponType=10
    def test_queryCoupon_statusNotExist(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,status=self.ReceiveCouponInfo.status)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertNotExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')



    #根据名称或者优惠券id查询的优惠券不存在,dealerCouponType=11
    def test_queryBenefit_dealerCouponNameNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,dealerCouponIdOrName=u'测试不存在的经销商活动名称')
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']), 0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据有效期起始时间查询的优惠券不存在,dealerCouponType=11
    def test_queryBenefit_effectiveTimeNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,effectiveTimeBegin='1475398800000',effectiveTimeEnd='1475485200000')
        self.assertEqual(queryBenefitResult['status'],0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据有效结束时间查询的优惠券不存在，dealerCouponType=11
    def test_queryBenefit_uneffectiveTimeNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,uneffectiveTimeBegin='1475398800000',uneffectiveTimeEnd='1475485200000')
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

     #根据创建时间查询的优惠券不存在,dealerCouponType=11
    def test_queryBenefit_createTimeNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,gmtCreateBegin=int(round(time.time())*1000+1000000),gmtCreateEnd=int(round(time.time())*1000+2000000))
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据使用店铺查询的优惠券不存在,dealerCouponType=11
    def test_queryBenefit_dealerNameNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,dealerName=self.dealerInfo.fullName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    #根据使用限制查询的优惠券不存在,dealerCouponType=11
    def test_queryBenefit_goodsIdNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,goodsName=u'不选在的goodName')
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送红包活动gch')

    #根据红包状态查询的优惠券不存在,dealerCouponType=11
    def test_queryBenefit_statusNotExist(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,status=self.ReceiveBenefitInfo.status)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertNotExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')



    #根据红包名称进行模糊查询,dealerCouponType=10
    def test_queryCoupon_fuzzy(self):
        self.dltool.createReceiveCouponActivity()
        queryCouponResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveCouponInfo.activityType,dealerCouponIdOrName=u'gch')
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],u'接口测试送红包活动gch')

    #根据优惠券名称进行模糊查询,dealerCouponType=11
    def test_queryBenefit_fuzzy(self):
        self.dltool.createReceiveBenifitActivity()
        queryBenefitResult = self.dlservice.queryDealerActivity(activityType=self.ReceiveBenefitInfo.activityType,dealerCouponIdOrName=u'gch')
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],u'接口测试送优惠券活动gch')

    def assertExist(self,queryResult,expectResult):
        dealerCoupons = []
        for item in queryResult:
            dealerCoupons.append(item['dealerCouponDto']['dealerCouponName'])
        self.assertEqual(expectResult in dealerCoupons,True)

    def assertNotExist(self,queryResult,expectResult):
        dealerCoupons = []
        for item in queryResult:
            dealerCoupons.append(item['dealerCouponDto']['dealerCouponName'])
        self.assertEqual(expectResult in dealerCoupons,False)


    def tearDown(self):
        self.dltool.deleteReceiveActivityBySQL()


def suite():
    suite=unittest.TestSuite()
    suite.addTest(queryDealerActivity("test_queryCoupon_createTime"))
    suite.addTest(queryDealerActivity("test_queryCoupon_createTimeNotExsit"))
    suite.addTest(queryDealerActivity("test_queryCoupon_dealerCouponIdOrName"))
    suite.addTest(queryDealerActivity("test_queryCoupon_dealerCouponNameNotExist"))
    suite.addTest(queryDealerActivity("test_queryCoupon_dealerName"))
    suite.addTest(queryDealerActivity("test_queryCoupon_dealerNameNotExist"))
    suite.addTest(queryDealerActivity("test_queryCoupon_effectiveTime"))
    suite.addTest(queryDealerActivity("test_queryCoupon_effectiveTimeNotExist"))
    suite.addTest(queryDealerActivity("test_queryCoupon_status"))
    suite.addTest(queryDealerActivity("test_queryCoupon_statusNotExist"))
    suite.addTest(queryDealerActivity("test_queryCoupon_uneffectiveTime"))
    suite.addTest(queryDealerActivity("test_queryCoupon_uneffectiveTimeNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_createTime"))
    suite.addTest(queryDealerActivity("test_queryBenefit_createTimeNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_dealerCouponName"))
    suite.addTest(queryDealerActivity("test_queryBenefit_dealerCouponNameNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_dealerName"))
    suite.addTest(queryDealerActivity("test_queryBenefit_dealerNameNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_effectiveTime"))
    suite.addTest(queryDealerActivity("test_queryBenefit_effectiveTimeNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_goodsIdNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_goodsName"))
    suite.addTest(queryDealerActivity("test_queryBenefit_status"))
    suite.addTest(queryDealerActivity("test_queryBenefit_statusNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_uneffectiveTime"))
    suite.addTest(queryDealerActivity("test_queryBenefit_uneffectiveTimeNotExist"))
    suite.addTest(queryDealerActivity("test_queryBenefit_fuzzy"))
    suite.addTest(queryDealerActivity("test_queryCoupon_fuzzy"))
    return suite



