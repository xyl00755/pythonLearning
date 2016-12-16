#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

"""
PUT http://127.0.0.1:8280/dealer/coupon/{activityId}

{
    'activityId':activityId,
    'logicDeleteFlag':logicDeleteFlag,
}

{
      "status": 0,
      "data": {
        "flag":true
      },
      "msg": "删除成功"
}
"""

class deleteDealerActivity(unittest.TestCase):

    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()

    #逻辑删除红包领取活动成功
    def test_deleteReceiveCoupon_success(self):
        createReceiveCouponResult=self.dltool.createReceiveCouponActivity()
        if createReceiveCouponResult['status'] == 0:
            activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
            deleteReceiveCouponResult = self.dlservice.deleteDealerActivity(activityId['activity_id'])
            self.assertEqual(deleteReceiveCouponResult['status'], 0)
            self.assertEqual(deleteReceiveCouponResult['data']['flag'],True)
            self.assertEqual(self.getLogicDeleteFlagFromDlpromotionx(activityType=self.ReceiveCouponInfo.activityType),'1')
            self.assertEqual(self.getLogicDeleteFlagFromDlcoupon(activityType=self.ReceiveCouponInfo.activityType),'1')
        else:
            print '创建红包领取活动失败，无法进行删除操作。'
            self.assertEqual(createReceiveCouponResult['status'], 0)

    #活动启动过不能删除,status=3为启动中
    def test_deleteReceiveCoupon_isStarted(self):
        self.dltool.createReceiveCouponActivity()
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        self.dlservice.modifyDealerActivity(activityId=activityId['activity_id'],status=3)
        deleteReceiveCouponResult = self.dlservice.deleteDealerActivity(activityId['activity_id'])
        self.assertEqual(deleteReceiveCouponResult['status'], 0)
        self.assertEqual(deleteReceiveCouponResult['data']['flag'],False)
        self.assertEqual(deleteReceiveCouponResult['msg'],u'优惠券已经启用过不能删除。')
        self.assertEqual(self.getLogicDeleteFlagFromDlpromotionx(activityType=self.ReceiveCouponInfo.activityType),'0')
        self.assertEqual(self.getLogicDeleteFlagFromDlcoupon(activityType=self.ReceiveCouponInfo.activityType),'0')


    #逻辑删除优惠券领取活动成功
    def test_deleteReceiveBenefit_success(self):
        createReceiveBenefitResult=self.dltool.createReceiveBenifitActivity()
        if createReceiveBenefitResult['status'] == 0:
            activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
            deleteReceiveBenefitResult = self.dlservice.deleteDealerActivity(activityId['activity_id'])
            self.assertEqual(deleteReceiveBenefitResult['status'], 0)
            self.assertEqual(deleteReceiveBenefitResult['data']['flag'],True)
            self.assertEqual(self.getLogicDeleteFlagFromDlpromotionx(activityType=self.ReceiveBenefitInfo.activityType),'1')
            self.assertEqual(self.getLogicDeleteFlagFromDlcoupon(activityType=self.ReceiveBenefitInfo.activityType),'1')
        else:
            self.assertEqual(createReceiveBenefitResult['status'], 0)
            print '创建优惠券领取活动失败，无法进行删除操作。'

     #活动启动过不能删除,status=3为启动中
    def test_deleteReceiveBenefit_isStarted(self):
        self.dltool.createReceiveBenifitActivity()
        activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?',self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        self.dlservice.modifyDealerActivity(activityId=activityId['activity_id'],status=3)
        deleteReceiveBenefitResult = self.dlservice.deleteDealerActivity(activityId['activity_id'])
        self.assertEqual(deleteReceiveBenefitResult['status'], 0)
        self.assertEqual(deleteReceiveBenefitResult['data']['flag'],False)
        self.assertEqual(deleteReceiveBenefitResult['msg'],u'优惠券已经启用过不能删除。')
        self.assertEqual(self.getLogicDeleteFlagFromDlpromotionx(activityType=self.ReceiveBenefitInfo.activityType),'0')
        self.assertEqual(self.getLogicDeleteFlagFromDlcoupon(activityType=self.ReceiveBenefitInfo.activityType),'0')

    #需要删除的活动activityId为空
    def test_deleteDealerActivity_activityNameNull(self):
        deleteDealerActivityResult = self.dlservice.deleteDealerActivity()
        self.assertEqual(deleteDealerActivityResult['status'],-1)
        self.assertEqual(deleteDealerActivityResult['msg'],u'修改/删除/优惠券/红包失败.')


    #获取用例执行后表dlpromotionx.dl_dealer_coupon_activity中logic_delete_flag值
    def getLogicDeleteFlagFromDlpromotionx(self,activityType):
        if activityType==self.ReceiveCouponInfo.activityType :
            logicDeleteFlag = select_one('select logic_delete_flag from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        elif activityType==self.ReceiveBenefitInfo.activityType:
            logicDeleteFlag = select_one('select logic_delete_flag from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        return logicDeleteFlag['logic_delete_flag']

    #获取用例执行后表dlcoupon.logic_delete_flag中logic_delete_flag值
    def getLogicDeleteFlagFromDlcoupon(self,activityType):
        if activityType==self.ReceiveCouponInfo.activityType :
            logicDeleteFlag = select_one('select logic_delete_flag from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.dealerCouponType)
        elif activityType==self.ReceiveBenefitInfo.activityType:
            logicDeleteFlag = select_one('select logic_delete_flag from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.dealerCouponType)
        return logicDeleteFlag['logic_delete_flag']

    def tearDown(self):
        self.dltool.deleteReceiveActivityBySQL()

def suite():
    suite=unittest.TestSuite()
    suite.addTest(deleteDealerActivity("test_deleteReceiveCoupon_success"))
    suite.addTest(deleteDealerActivity("test_deleteReceiveBenefit_success"))
    suite.addTest(deleteDealerActivity("test_deleteReceiveCoupon_isStarted"))
    suite.addTest(deleteDealerActivity("test_deleteReceiveBenefit_isStarted"))
    suite.addTest(deleteDealerActivity("test_deleteDealerActivity_activityNameNull"))
    return suite