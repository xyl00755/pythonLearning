#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

class createDealerPushActivity(unittest.TestCase):

    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    PushCouponInfo = eData('PushCoupon')
    PushBenefitInfo = eData('PushBenefit')

    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()

    #成功创建红包推送 activityType='12' couponTypeId='10'
    def test_createPushCoupon_success(self):
        self.dltool.createReceiveCouponActivity()
        coupondealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.dealerCouponType)
        createPushCouponResult=self.dltool.createPushCouponActivity(couponId=coupondealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushCouponResult['status'], 0)
        self.assertEqual(createPushCouponResult['data']['flag'],True)
        self.assertPushResult(pushList=[self.PushCouponInfo.pushList1,self.PushCouponInfo.pushList2],expectStatus=0)

    #创建重名的红包推送活动失败
    def test_createPushCoupon_repeat(self):
        self.dltool.createReceiveCouponActivity()
        coupondealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.dealerCouponType)
        self.dltool.createPushCouponActivity(couponId=coupondealerCouponId['dealer_coupon_id'])
        createPushCouponResult=self.dltool.createPushCouponActivity(couponId=coupondealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushCouponResult['status'], -1)
        self.assertEqual(createPushCouponResult['data']['flag'],False)

    #推送的红包并非当前经销商的红包
    def test_createPushCoupon_couponNotMatch(self):
        self.dltool.createReceiveCouponActivity(dealerId='802412e1f4d54f6a858757545394dca1',dealerName=u'测试自动化配送商01')
        coupondealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.dealerCouponType)
        createPushCouponResult=self.dltool.createPushCouponActivity(couponId=coupondealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushCouponResult['status'], -1)
        self.assertEqual(createPushCouponResult['data']['flag'],False)

    #推送名单中的一个终端店与红包的可用渠道availableChannel不匹配
    def test_createPushCoupon_availableChannelNotMatch(self):
        self.dltool.createReceiveCouponActivity(availableChannel="S011,S013")
        coupondealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.dealerCouponType)
        createPushCouponResult=self.dltool.createPushCouponActivity(couponId=coupondealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushCouponResult['status'], 0)
        self.assertEqual(createPushCouponResult['data']['flag'],True)
        self.assertPushResult(pushList=[self.PushCouponInfo.pushList1,self.PushCouponInfo.pushList2],expectStatus=6)

    #推送名单中终端店地域与红包可用地域不匹配
    def test_createPushCoupon_areaNotMatch(self):
        self.dltool.createReceiveCouponActivity(areaLimit="CHNP034")
        coupondealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.dealerCouponType)
        createPushCouponResult=self.dltool.createPushCouponActivity(couponId=coupondealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushCouponResult['status'], 0)
        self.assertEqual(createPushCouponResult['data']['flag'],True)
        self.assertPushResult(pushList=[self.PushCouponInfo.pushList1,self.PushCouponInfo.pushList2],expectStatus=7)



    #成功创建优惠券推送 activityType='13' couponTypeId='11'
    def test_createPushBenefit_success(self):
        self.dltool.createReceiveBenifitActivity()
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        createPushBenefitResult=self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushBenefitResult['status'], 0)
        self.assertEqual(createPushBenefitResult['data']['flag'],True)
        self.assertPushResult(activityName=self.PushBenefitInfo.activityName,activityType=self.PushBenefitInfo.activityType,pushList=[self.PushCouponInfo.pushList1,self.PushCouponInfo.pushList2],expectStatus=0)

    #创建重名的优惠券推送活动失败
    def test_createPushBenefit_repeat(self):
        self.dltool.createReceiveBenifitActivity()
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        createPushBenefitResult=self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushBenefitResult['status'], -1)
        self.assertEqual(createPushBenefitResult['data']['flag'],False)

    #推送优惠券，用户已存在相同的优惠券，且状态为未使用
    def test_createPushBenefit_benefitAlreadyExist(self):
        self.dltool.createReceiveBenifitActivity()
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        createPushBenefitResult=self.dltool.createPushBenefitActivity(activityName='接口测试优惠券推送活动2',couponId=benefitdealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushBenefitResult['status'], 0)
        self.assertEqual(createPushBenefitResult['data']['flag'],True)
        self.assertPushResult(activityName=u'接口测试优惠券推送活动2',activityType=self.PushBenefitInfo.activityType,pushList=[self.PushBenefitInfo.pushList1,self.PushBenefitInfo.pushList2],expectStatus=1)
        self.dltool.deletePushActivityBySQL(activityName2='接口测试优惠券推送活动2')

    #推送优惠券，推送名单中的一个终端店与优惠券的可用渠道availableChannel不匹配
    def test_createPushBenefit_availableChannelNotMatch(self):
        self.dltool.createReceiveBenifitActivity(availableChannel="S011,S013")
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        createPushBenefitResult=self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushBenefitResult['status'], 0)
        self.assertEqual(createPushBenefitResult['data']['flag'],True)
        self.assertPushResult(activityName=self.PushBenefitInfo.activityName,activityType=self.PushBenefitInfo.activityType,pushList=[self.PushBenefitInfo.pushList1,self.PushBenefitInfo.pushList2],expectStatus=6)

    #推送优惠券，推送名单中终端店地域与优惠券可用地域不匹配
    def test_createPushBenefit_areaNotMatch(self):
        self.dltool.createReceiveBenifitActivity(areaLimit="CHNP034")
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        createPushBenefitResult=self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushBenefitResult['status'], 0)
        self.assertEqual(createPushBenefitResult['data']['flag'],True)
        self.assertPushResult(activityName=self.PushBenefitInfo.activityName,activityType=self.PushBenefitInfo.activityType,pushList=[self.PushBenefitInfo.pushList1,self.PushBenefitInfo.pushList2],expectStatus=7)

    #推送优惠券，推送名单中终端店无该优惠券商品的售卖权
    def test_createPushBenefit_sellRightNotMatch(self):
        self.dltool.createReceiveBenifitActivity(goodsId="13c139794d8b441bae348fbc3bde7594")
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        createPushBenefitResult=self.dltool.createPushBenefitActivity(couponId=benefitdealerCouponId['dealer_coupon_id'])
        self.assertEqual(createPushBenefitResult['status'], 0)
        self.assertEqual(createPushBenefitResult['data']['flag'],True)
        self.assertPushResult(activityName=self.PushBenefitInfo.activityName,activityType=self.PushBenefitInfo.activityType,pushList=[self.PushBenefitInfo.pushList1,self.PushBenefitInfo.pushList2],expectStatus=3)

    #创建推送活动时候活动类型不存在
    def test_createPushActivity_activityTypeNotExist(self):
        createPushBenefitResult=self.dltool.createPushBenefitActivity(activityType='15')
        self.assertEqual(createPushBenefitResult['status'], -1)
        self.assertEqual(createPushBenefitResult['data']['flag'],False)


    #验证推送活动状态的方法，0:消息发送成功，1：已经领用了该优惠券不再发放，2：推送发券消息失败，3：用户与优惠券类型不匹配，4：减库存失败，5：活动减库存成功',
    def assertPushResult(self,activityName=PushCouponInfo.activityName,activityType=PushCouponInfo.activityType,pushList=PushCouponInfo.pushList1,expectStatus=None):
        statusArr = []
        for pushItem in pushList:
            activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?',activityName,activityType)
            status = select('select status from dlpromotionx.dl_dealer_push_name_list where activity_id = ? and company_id = ?',activityId['activity_id'],pushItem)
            for item in status:
                statusArr.append(item['status'])
        self.assertEqual(expectStatus in statusArr,True)

    #将要推送的红包或者优惠券id不存在
    def test_createPushActivity_couponIdNotExist(self):
        createPushCouponResult=self.dltool.createPushCouponActivity(couponId='123456789')
        self.assertEqual(createPushCouponResult['status'], -1)
        self.assertEqual(createPushCouponResult['data']['flag'],False)


    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'

    def tearDown(self):
        self.dltool.deletePushActivityBySQL()
        self.dltool.deleteReceiveActivityBySQL()

def suite():
    suite=unittest.TestSuite()
    suite.addTest(createDealerPushActivity("test_createPushActivity_activityTypeNotExist"))
    suite.addTest(createDealerPushActivity("test_createPushActivity_couponIdNotExist"))
    suite.addTest(createDealerPushActivity("test_createPushBenefit_areaNotMatch"))
    suite.addTest(createDealerPushActivity("test_createPushBenefit_availableChannelNotMatch"))
    suite.addTest(createDealerPushActivity("test_createPushBenefit_benefitAlreadyExist"))
    suite.addTest(createDealerPushActivity("test_createPushBenefit_repeat"))
    suite.addTest(createDealerPushActivity("test_createPushBenefit_sellRightNotMatch"))
    suite.addTest(createDealerPushActivity("test_createPushBenefit_success"))
    suite.addTest(createDealerPushActivity("test_createPushCoupon_areaNotMatch"))
    suite.addTest(createDealerPushActivity("test_createPushCoupon_availableChannelNotMatch"))
    suite.addTest(createDealerPushActivity("test_createPushCoupon_couponNotMatch"))
    suite.addTest(createDealerPushActivity("test_createPushCoupon_repeat"))
    suite.addTest(createDealerPushActivity("test_createPushCoupon_success"))
    return suite