#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

"""
POST /dealer/verifyName
 {
    'dealerCouponType':dealerCouponType,
    'dealerCouponName':dealerCouponName,
     'flag':flag,
    'activityId':activityId
}
{
  "status": 0,
  "data": {
    "flag" : true
  },
  "msg": "重复"
}
"""

class verifyName(unittest.TestCase):

    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    PushCouponInfo = eData('PushCoupon')
    PushBenefitInfo = eData('PushBenefit')
    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()

    #新增的判重成功，红包名称重复，flag=0表示是新增的判重
    def test_verifyAddName_couponNameRepeat(self):
        self.dltool.createReceiveCouponActivity()
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName,dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],True)

    #新增的判重成功，红包名称不重复
    def test_verifyAddName_couponNameNotRepeat(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName,dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #新增的判重成功，红包名称不重复，存在同名称的优惠券
    def test_verifyAddName_sameNameWithBenefit(self):
        self.dltool.createReceiveBenifitActivity(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName,dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=0)
        self.dltool.deleteReceiveActivityBySQL(dealerCouponType=self.ReceiveBenefitInfo.dealerCouponType,activityType=self.ReceiveBenefitInfo.activityType)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #修改的判重成功，红包名称与自身名称一致，不重复,flag=1表示是修改的判重
    def test_verifyModifyName_couponNameSelfConsistency(self):
        self.dltool.createReceiveCouponActivity()
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName,dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=1,activityId=activityId['activity_id'])
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #修改的判重成功，红包名称重复
    def test_verifyModifyName_couponNameRepeat(self):
        self.dltool.createReceiveCouponActivity()
        self.dltool.createReceiveCouponActivity(dealerCouponName=u'接口测试送红包活动2')
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=u'接口测试送红包活动2',dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=1,activityId=activityId['activity_id'])
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName=u'接口测试送红包活动2')
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],True)

    #修改的判重成功，红包名称不重复
    def test_verifyModifyName_couponNameNotRepeat(self):
        self.dltool.createReceiveCouponActivity()
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=u'接口测试送红包活动2',dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=1,activityId=activityId['activity_id'])
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)



    #新增的判重成功，优惠券名称重复，flag=0表示是新增的判重
    def test_verifyAddName_benefitNameRepeat(self):
        self.dltool.createReceiveBenifitActivity()
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveBenefitInfo.dealerCouponName,dealerCouponType = self.ReceiveBenefitInfo.dealerCouponType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],True)

    #新增的判重成功，优惠券名称不重复
    def test_verifyAddName_benefitNameNotRepeat(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveBenefitInfo.dealerCouponName,dealerCouponType = self.ReceiveBenefitInfo.dealerCouponType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #新增的判重成功，优惠券名称不重复，存在同名称的红包
    def test_verifyAddName_sameNameWithCoupon(self):
        self.dltool.createReceiveCouponActivity(dealerCouponName=self.ReceiveBenefitInfo.dealerCouponName)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveBenefitInfo.dealerCouponName,dealerCouponType = self.ReceiveBenefitInfo.dealerCouponType,flag=0)
        self.dltool.deleteReceiveActivityBySQL(dealerCouponType=self.ReceiveBenefitInfo.dealerCouponType,activityType=self.ReceiveCouponInfo.activityType)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #修改的判重成功，优惠券名称与自身名称一致，不重复,flag=1表示是修改的判重
    def test_verifyModifyName_benefitNameSelfConsistency(self):
        self.dltool.createReceiveBenifitActivity()
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveBenefitInfo.dealerCouponName,dealerCouponType = self.ReceiveBenefitInfo.dealerCouponType,flag=1,activityId=activityId['activity_id'])
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #修改的判重成功，优惠券名称重复
    def test_verifyModifyName_benefitNameRepeat(self):
        self.dltool.createReceiveBenifitActivity()
        self.dltool.createReceiveBenifitActivity(dealerCouponName=u'接口测试送优惠券活动2',effectiveTime='1576028800000',uneffectiveTime='1576979199000',goodsId='43411',goodsName='测试商品',areaLimit='code3',availableChannel='S013')
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=u'接口测试送优惠券活动2',dealerCouponType = self.ReceiveBenefitInfo.dealerCouponType,flag=1,activityId=activityId['activity_id'])
        self.dltool.deleteReceiveActivityBySQL(dealerCouponName2=u'接口测试送优惠券活动2')
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],True)

    #修改的判重成功，优惠券名称不重复
    def test_verifyModifyName_benefitNameNotRepeat(self):
        self.dltool.createReceiveBenifitActivity()
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=u'接口测试送红包活动2',dealerCouponType = self.ReceiveBenefitInfo.dealerCouponType,flag=1,activityId=activityId['activity_id'])
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)




    #新增的判重成功，推送红包名称重复，flag=0表示是新增的判重
    def test_verifyAddName_pushCouponNameRepeat(self):
        self.dltool.createPushCouponActivity()
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.PushCouponInfo.activityName,dealerCouponType = self.PushCouponInfo.activityType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],True)

    #新增的判重成功，推送红包名称不重复
    def test_verifyAddName_pushCouponNameNotRepeat(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.PushCouponInfo.activityName,dealerCouponType = self.PushCouponInfo.activityType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #新增的判重成功，推送红包名称不重复，存在同名称的推送优惠券
    def test_verifyAddName_sameNameWithPushBenefit(self):
        self.dltool.createPushBenefitActivity(activityName=self.PushCouponInfo.activityName)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.PushCouponInfo.activityName,dealerCouponType = self.PushCouponInfo.activityType,flag=0)
        self.dltool.deletePushActivityBySQL(activityName2=self.PushCouponInfo.activityName,activityType2=self.PushBenefitInfo.activityType)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)


    #新增的判重成功，推送优惠券名称重复，flag=0表示是新增的判重
    def test_verifyAddName_benefitCouponNameRepeat(self):
        self.dltool.createPushBenefitActivity()
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.PushBenefitInfo.activityName,dealerCouponType = self.PushBenefitInfo.activityType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],True)

    #新增的判重成功，推送优惠券名称不重复
    def test_verifyAddName_benefitCouponNameNotRepeat(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.PushBenefitInfo.activityName,dealerCouponType = self.PushBenefitInfo.activityType,flag=0)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)

    #新增的判重成功，推送优惠券名称不重复，存在同名称的推送红包
    def test_verifyAddName_sameNameWithCoupon(self):
        self.dltool.createPushCouponActivity(activityName=self.PushBenefitInfo.activityName)
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.PushBenefitInfo.activityName,dealerCouponType = self.PushBenefitInfo.activityType,flag=0)
        self.dltool.deletePushActivityBySQL(activityName=self.PushBenefitInfo.activityName,activityType=self.PushCouponInfo.activityType)
        self.assertEqual(verifyNameResult['status'], 0)
        self.assertEqual(verifyNameResult['data']['flag'],False)


    #修改的判重失败，修改的判重时没有传递activityId
    def test_verifyModifyName_activityIdNull(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName,dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=1)
        self.assertEqual(verifyNameResult['status'], -1)

    #判重失败，红包名称为空
    def test_verifyName_couponNameNull(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponType = self.ReceiveCouponInfo.dealerCouponType,flag=0)
        self.assertEqual(verifyNameResult['status'], -1)

    #判重失败，红包类型为空
    def test_verifyName_couponTypeNull(self):
        verifyNameResult = self.dlservice.verifyName(dealerCouponName=self.ReceiveCouponInfo.dealerCouponName,flag=0)
        self.assertEqual(verifyNameResult['status'], -1)

    def tearDown(self):
        self.dltool.deleteReceiveActivityBySQL()
        self.dltool.deletePushActivityBySQL()

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'

def suite():
    suite=unittest.TestSuite()
    # suite.addTest(verifyName("test_functions"))
    suite.addTest(verifyName("test_verifyAddName_benefitCouponNameNotRepeat"))
    suite.addTest(verifyName("test_verifyAddName_benefitCouponNameRepeat"))
    suite.addTest(verifyName("test_verifyAddName_benefitNameNotRepeat"))
    suite.addTest(verifyName("test_verifyAddName_benefitNameRepeat"))
    suite.addTest(verifyName("test_verifyAddName_couponNameNotRepeat"))
    suite.addTest(verifyName("test_verifyAddName_couponNameRepeat"))
    suite.addTest(verifyName("test_verifyAddName_pushCouponNameNotRepeat"))
    suite.addTest(verifyName("test_verifyAddName_pushCouponNameRepeat"))
    suite.addTest(verifyName("test_verifyAddName_sameNameWithBenefit"))
    suite.addTest(verifyName("test_verifyAddName_sameNameWithCoupon"))
    suite.addTest(verifyName("test_verifyAddName_sameNameWithPushBenefit"))
    suite.addTest(verifyName("test_verifyModifyName_activityIdNull"))
    suite.addTest(verifyName("test_verifyModifyName_benefitNameNotRepeat"))
    suite.addTest(verifyName("test_verifyModifyName_benefitNameRepeat"))
    suite.addTest(verifyName("test_verifyModifyName_benefitNameSelfConsistency"))
    suite.addTest(verifyName("test_verifyModifyName_couponNameNotRepeat"))
    suite.addTest(verifyName("test_verifyModifyName_couponNameRepeat"))
    suite.addTest(verifyName("test_verifyModifyName_couponNameSelfConsistency"))
    suite.addTest(verifyName("test_verifyName_couponNameNull"))
    suite.addTest(verifyName("test_verifyName_couponTypeNull"))
    return suite

