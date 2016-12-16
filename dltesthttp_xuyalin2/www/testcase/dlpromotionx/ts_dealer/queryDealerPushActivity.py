#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *
from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

"""
POST /dealer/pushcoupon
{
    'activityName':activityName,
    'gmtCreateBegin':gmtCreateBegin,
    'gmtCreateEnd':gmtCreateEnd,
     'createPersonName':createPersonName
}
"""

class queryDealerPushActivity(unittest.TestCase):

    PushCouponInfo = eData('PushCoupon')
    PushBenefitInfo = eData('PushBenefit')
    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()


    #所有参数都为空，获取所有数据
    def test_queryPushCoupon(self):
        queryCouponResult = self.dlservice.queryDealerPushActivity()
        self.assertEqual(queryCouponResult['status'], 0)

    #根据活动名称查询红包推送活动，查询成功，获得一条活动数据
    def test_queryPushCoupon_activityName(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(activityName=self.PushCouponInfo.activityName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 1)
        self.assertExist(queryCouponResult['data']['result'],self.PushCouponInfo.activityName)

    #根据活动名称查询红包推送活动，查询成功，没有相关活动数据
    def test_queryPushCoupon_activityNameNotExist(self):
        queryCouponResult = self.dlservice.queryDealerPushActivity(activityName=self.PushCouponInfo.activityName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)

    #根据创建时间查询红包推送活动,查询成功，获得一条活动数据
    def test_queryPushCoupon_gmtCreate(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],self.PushCouponInfo.activityName)

    #根据创建时间查询红包推送活动,查询成功，没有相关数据
    def test_queryPushCoupon_gmtCreateNotExist(self):
        queryCouponResult = self.dlservice.queryDealerPushActivity(gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)

    #根据创建活动人查询红包推送活动,查询成功，获得一条活动数据
    def test_queryPushCoupon_createPersonName(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(createPersonName=self.PushCouponInfo.createPersonName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],self.PushCouponInfo.activityName)

    #根据创建活动人查询红包推送活动,查询成功，没有相关数据
    def test_queryPushCoupon_createPersonNameNotExist(self):
        queryCouponResult = self.dlservice.queryDealerPushActivity(createPersonName=self.PushCouponInfo.createPersonName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)

    #根据活动名称、创建时间、创建人联合查询红包推送活动，查询成功，获得一条数据
    def test_queryPushCoupon_unionQuery(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(activityName=self.PushCouponInfo.activityName,gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000,createPersonName=self.PushCouponInfo.createPersonName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertExist(queryCouponResult['data']['result'],self.PushCouponInfo.activityName)

    #根据活动名称、创建时间、创建人联合查询红包推送活动，活动名称不存在，查询成功，没有相关数据
    def test_queryPushCoupon_unionQueryActivityNameNotExist(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(activityName=u'测试不存在的活动名称',gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000,createPersonName=self.PushCouponInfo.createPersonName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)

    #根据活动名称、创建时间、创建人联合查询红包推送活动，创建时间不匹配，查询成功，没有相关数据
    def test_queryPushCoupon_unionQueryCreateTimeNotExist(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(activityName=self.PushCouponInfo.activityName,gmtCreateBegin=int(round(time.time())*1000)+1000000,gmtCreateEnd=int(round(time.time())*1000)+2000000,createPersonName=self.PushCouponInfo.createPersonName)
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)

    #根据活动名称、创建时间、创建人联合查询红包推送活动，创建人不存在，查询成功，没有相关数据
    def test_queryPushCoupon_unionQueryCreatePersonNotExist(self):
        self.dltool.createPushCouponActivity()
        queryCouponResult = self.dlservice.queryDealerPushActivity(activityName=self.PushCouponInfo.activityName,gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000,createPersonName=u'测试不存在的创建人')
        self.assertEqual(queryCouponResult['status'], 0)
        self.assertEqual(len(queryCouponResult['data']['result']), 0)




    #根据活动名称查询优惠券推送活动，查询成功，获得一条数据
    def test_queryPushBenefit_activityName(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(activityName=self.PushBenefitInfo.activityName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],self.PushBenefitInfo.activityName)

     #根据活动名称查询优惠券推送活动，查询成功，没有相关数据
    def test_queryPushBenefit_activityNameNotExist(self):
        queryBenefitResult = self.dlservice.queryDealerPushActivity(activityName=self.PushBenefitInfo.activityName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']), 0)

    #根据创建时间查询优惠券推送活动,查询成功，获得一条数据
    def test_queryPushBenefit_gmtCreate(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],self.PushBenefitInfo.activityName)

    #根据创建时间查询优惠券推送活动，查询成功，没有相关数据
    def test_queryPushBenefit_gmtCreateNotExist(self):
        queryBenefitResult = self.dlservice.queryDealerPushActivity(gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']),0)

    #根据创建活动人查询优惠券推送活动，擦汗寻成功，获得一条数据
    def test_queryPushBenefit_createPersonName(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(createPersonName=self.PushBenefitInfo.createPersonName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],self.PushBenefitInfo.activityName)

    #根据创建活动人查询优惠券推送活动，查询成功，没有相关数据
    def test_queryPushBenefit_createPersonNameNotExist(self):
        queryBenefitResult = self.dlservice.queryDealerPushActivity(createPersonName=self.PushBenefitInfo.createPersonName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertNotExist(queryBenefitResult['data']['result'],self.PushBenefitInfo.activityName)

    #根据活动名称、创建时间、创建人联合查询优惠券推送活动，查询成功，获得一条数据
    def test_queryPushBenefit_unionQuery(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(activityName=self.PushBenefitInfo.activityName,gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000,createPersonName=self.PushBenefitInfo.createPersonName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertExist(queryBenefitResult['data']['result'],self.PushBenefitInfo.activityName)

    #根据活动名称、创建时间、创建人联合查询优惠券推送活动，活动名称不存在，查询成功，没有相关数据
    def test_queryPushBenefit_unionQueryActivityNameNotExist(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(activityName=u'测试不存在的活动名称',gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000,createPersonName=self.PushBenefitInfo.createPersonName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']), 0)

    #根据活动名称、创建时间、创建人联合查询优惠券推送活动，创建时间不匹配，查询成功，没有相关数据
    def test_queryPushBenefit_unionQueryCreateTimeNotExist(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(activityName=self.PushBenefitInfo.activityName,gmtCreateBegin=int(round(time.time())*1000)+1000000,gmtCreateEnd=int(round(time.time())*1000)+2000000,createPersonName=self.PushBenefitInfo.createPersonName)
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']), 0)

    #根据活动名称、创建时间、创建人联合查询优惠券推送活动，创建人不存在，查询成功，没有相关数据
    def test_queryPushBenefit_unionQueryCreatePersonNotExist(self):
        self.dltool.createPushBenefitActivity()
        queryBenefitResult = self.dlservice.queryDealerPushActivity(activityName=self.PushBenefitInfo.activityName,gmtCreateBegin=int(round(time.time())*1000)-1000000,gmtCreateEnd=int(round(time.time())*1000)+1000000,createPersonName=u'测试不存在的创建人')
        self.assertEqual(queryBenefitResult['status'], 0)
        self.assertEqual(len(queryBenefitResult['data']['result']), 0)


    def assertExist(self,queryResult,expectResult):
        dealerCoupons = []
        for item in queryResult:
            dealerCoupons.append(str(item['activityName'].encode("utf-8")))
        self.assertEqual(expectResult in dealerCoupons,True)

    def assertNotExist(self,queryResult,expectResult):
        dealerCoupons = []
        for item in queryResult:
            dealerCoupons.append(str(item['activityName'].encode("utf-8")))
        self.assertEqual(expectResult in dealerCoupons,False)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'


    def tearDown(self):
        self.dltool.deletePushActivityBySQL()


def suite():
    suite=unittest.TestSuite()
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_activityName"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_activityNameNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_createPersonName"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_createPersonNameNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_gmtCreate"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_gmtCreateNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_unionQuery"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_unionQueryActivityNameNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_unionQueryCreatePersonNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushBenefit_unionQueryCreateTimeNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_activityName"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_activityNameNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_createPersonName"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_createPersonNameNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_gmtCreate"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_gmtCreateNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_unionQuery"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_unionQueryActivityNameNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_unionQueryCreatePersonNotExist"))
    suite.addTest(queryDealerPushActivity("test_queryPushCoupon_unionQueryCreateTimeNotExist"))
    return suite



