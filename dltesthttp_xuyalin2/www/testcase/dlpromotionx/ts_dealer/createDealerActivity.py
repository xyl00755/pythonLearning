#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

"""
http://127.0.0.1:8280/dealer/activity

{
    "dealerCouponDto":{
        "dealerCouponName":"lulu酒业送券活动",
        "dealerCouponType":"11",
        "dealerName":"lulu酒业",
        "dealerId":"7d8f02016bc141efb9d4c2a67d4bedff",
        "totalNum":100,
        "totalAmount":10000,
        "effectiveTime":"1474861112",
        "uneffectiveTime":"1474861112",
        "availableChannel":"S012,S014",
        "goodsId":"cac55daa5a0d41bc9e1d1dc6da3962e6",
        "goodsName":"茅台 500ml",
        "areaLimit":"code1,code2",
        "platformLimit":"WEB,APP",
        "createPersonName":"system",
        "createPerson":"7d8f02016bc141efb9d4c2a67d4bedff",
        "dealerCouponAmounts":[
            {
                "couponMinAmt":100,
                "effectiveAmt":10,
                "couponPriority":1,
                "packageAmount":2,
                "packageAmt":200
            },
            {
                "couponMinAmt":100,
                "effectiveAmt":10,
                "couponPriority":1,
                "packageAmount":2,
                "packageAmt":200
            }
        ]
    },
    "activityType":"10",
    "issueWay":0,
    "autoEnable":"1474861112",
    "autoDisable":"1474861112",
    "approvalAutoEnable":1,
    "releaseCompletionDisable":0,
    "limitNum":2,
    "showWay":"0,1,2",
    "getWay":"0,1",
    "createPersonName":"system",
    "createPerson":"7d8f02016bc141efb9d4c2a67d4bedff",
    "notice":"01,02"
}

{
    "status": 0,
    "data": {
        "flag" : true
    },
    "msg": "提示信息"
}
"""

class createDealerActivity(unittest.TestCase):

    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()

    #成功创建红包领取活动，activityType=10
    def test_createReceiveCoupon_success(self):
        createReceiveCouponResult = self.dltool.createReceiveCouponActivity()
        self.assertEqual(createReceiveCouponResult['status'], 0)
        self.assertEqual(createReceiveCouponResult['data']['flag'],True)

    #创建红包活动的名称重复
    def test_createReceiveCoupon_activityNameRepeat(self):
        self.dltool.createReceiveCouponActivity()
        createReceiveCouponResult = self.dltool.createReceiveCouponActivity()
        self.assertEqual(createReceiveCouponResult['status'], -1)
        self.assertEqual(createReceiveCouponResult['data']['flag'],False)


    #创建领取优惠券领取活动成功,activityType=11
    def test_createReceiveBenefit_success(self):
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity()
        self.assertEqual(createReceiveBenefitResult['status'], 0)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],True)

    #创建领取优惠券活动，活动名称重复
    def test_createReceiveBenefit_activityNameRepeat(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity()
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #时间左重叠，2016-11-01 18:00:00 -- 2016-11-02 18:00:00；2016-10-31 18:00:00 -- 2016-11-01 18:00:00
    def test_createReceiveBenefit_timeLeftOverlap(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1477908000000',uneffectiveTime='1477994400000')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #时间重叠，2016-11-01 18:00:00 -- 2016-11-02 18:00:00；2016-11-01 19:00:00 -- 2016-11-02 17:00:00
    def test_createReceiveBenefit_timeOverlap(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1477998000000',uneffectiveTime='1478077200000')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #时间右重叠，2016-11-01 18:00:00 -- 2016-11-02 18:00:00；2016-11-02 18:00:00 -- 2016-11-03 18:00:00
    def test_createReceiveBenefit_timeRightOverlap(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1478080800000',uneffectiveTime='1478167200000')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

     #时间包含，2016-11-01 18:00:00 -- 2016-11-02 18:00:00；2016-10-30 18:00:00 -- 2016-11-03 18:00:00
    def test_createReceiveBenefit_timeIncluded(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1477908000000',uneffectiveTime='1478167200000')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #areaLimit，存在省的优惠券，重复创建市级别的优惠券
    def test_createReceiveBenefit_areaLimitIncluded1(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',areaLimit='CHNP035C001')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #areaLimit,存在市的优惠券，重复创建省级别的优惠券
    def test_createReceiveBenefit_areaLimitIncluded2(self):
        self.dltool.createReceiveBenifitActivity(areaLimit='CHNP035C001')
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',areaLimit='CHNP035')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #arealimit不同
    def test_createReceiveBenefit_arealimitDifferent(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',areaLimit='CHNP034')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], 0)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],True)

    #availableChannel不同
    def test_createReceiveBenefit_availableChannelDifferent(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',availableChannel='S014')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], 0)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],True)

    #goodsId不同
    def test_createReceiveBenefit_goodsIdDifferent(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',goodsId='54564gsdfg4564656')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], 0)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],True)

    #有效时间不同
    def test_createReceiveBenefit_timeDifferent(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1478167200000',uneffectiveTime='1478253600000')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], 0)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],True)

    #重复创建优惠券
    def test_createReceiveBenefit_repeat(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #包含11.01、goods、S011、CHNP035。2016-10-31 18:00:00 -- 2016-11-02 10:00:00
    def test_createReceiveBenefit_repeat1(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1477908000000',uneffectiveTime='1478052000000',availableChannel='S011,S014',areaLimit='CHNP034,CHNP035')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #包含11.01、goods、S013、CHNP035。2016-10-31 18:00:00 -- 2016-11-02 10:00:00
    def test_createReceiveBenefit_repeat2(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1477908000000',uneffectiveTime='1478052000000',availableChannel='S013,S014',areaLimit='CHNP034,CHNP035')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #包含11.02、goods、S011、CHNP035。2016-11-02 10:00:00 -- 2016-11-03 10:00:00
    def test_createReceiveBenefit_repeat3(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1478052000000',uneffectiveTime='1478138400000',availableChannel='S011,S014',areaLimit='CHNP034,CHNP035')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #包含11.02、goods、S013、CHNP035。2016-11-02 10:00:00 -- 2016-11-03 10:00:00
    def test_createReceiveBenefit_repeat4(self):
        self.dltool.createReceiveBenifitActivity()
        createReceiveBenefitResult =self.dltool.createReceiveBenifitActivity(dealerCouponName='接口测试送优惠券活动gch2',effectiveTime='1478052000000',uneffectiveTime='1478138400000',availableChannel='S013,S014',areaLimit='CHNP034,CHNP035')
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2='接口测试送优惠券活动gch2')
        self.assertEqual(createReceiveBenefitResult['status'], -1)
        self.assertEqual(createReceiveBenefitResult['data']['flag'],False)

    #创建红包领取活动时候活动类型不存在
    def test_createReceiveActivity_activityTypeNotExist(self):
        createReceiveCouponResult=self.dltool.createReceiveCouponActivity(activityType='15')
        self.assertEqual(createReceiveCouponResult['status'], -1)
        self.assertEqual(createReceiveCouponResult['data']['flag'],False)

    #用例执行完成后清理数据库
    def tearDown(self):
        self.dltool.deleteReceiveActivityBySQL()

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'


def suite():
    suite=unittest.TestSuite()
    suite.addTest(createDealerActivity("test_createReceiveActivity_activityTypeNotExist"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_activityNameRepeat"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_areaLimitIncluded1"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_areaLimitIncluded2"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_arealimitDifferent"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_availableChannelDifferent"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_goodsIdDifferent"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_repeat"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_success"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_timeDifferent"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_timeIncluded"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_timeLeftOverlap"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_timeOverlap"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_timeRightOverlap"))
    suite.addTest(createDealerActivity("test_createReceiveCoupon_activityNameRepeat"))
    suite.addTest(createDealerActivity("test_createReceiveCoupon_success"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_repeat1"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_repeat2"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_repeat3"))
    suite.addTest(createDealerActivity("test_createReceiveBenefit_repeat4"))
    return suite