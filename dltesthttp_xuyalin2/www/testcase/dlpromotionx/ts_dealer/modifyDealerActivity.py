#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.testcase.dlpromotionx.tool.createDealerActivityTool import *

"""
PUT /dealer/coupon/{activityId}
 {
    'activityId':activityId,
    'autoEnable':autoEnable,
    'autoDisable':autoDisable,
    'status':status
 }
{
    "status": 0,
    "data": {},
    "msg": ""
}
"""

class modifyDealerActivity(unittest.TestCase):
    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    dlservice = dlpromotionx()
    dltool = createDealerActivityTool()

    def setUp(self):
        self.tearDown()

    #更新红包状态为启用，成功。更改启用状态时必须传入启动停用时间
    def test_modifyReceiveCoupon_status(self):
        activityId=self.createDealerActivity(activityType=self.ReceiveCouponInfo.activityType)
        modifyResult = self.dlservice.modifyDealerActivity(activityId=activityId,status=self.ReceiveCouponInfo.status,autoEnable=self.ReceiveCouponInfo.autoEnable,autoDisable=self.ReceiveCouponInfo.autoDisable)
        couponActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        autoEnable = select_one('select auto_enable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        autoDisable = select_one('select auto_disable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        self.assertEqual(self.timeStrtoTimeStamp(str(autoEnable['auto_enable'])),self.ReceiveCouponInfo.autoEnable)
        self.assertEqual(self.timeStrtoTimeStamp(str(autoDisable['auto_disable'])),self.ReceiveCouponInfo.autoDisable)
        status = select_one('select status from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        self.assertEqual(modifyResult['status'],0)
        self.assertEqual(modifyResult['msg'],u'修改成功')
        self.assertEqual(status['status'],int(self.ReceiveCouponInfo.status))

    #更新红包状态为启用，不传自动启用时间和停用时间
    def test_modifyReceiveCoupon_statusNoTime(self):
        activityId=self.createDealerActivity(activityType=self.ReceiveCouponInfo.activityType)
        modifyResult = self.dlservice.modifyDealerActivity(activityId=activityId,status=self.ReceiveCouponInfo.status,autoEnable=None,autoDisable=None)
        couponActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        autoEnable = select_one('select auto_enable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        autoDisable = select_one('select auto_disable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        self.assertEqual(autoEnable['auto_enable'],None)
        self.assertEqual(autoDisable['auto_disable'],None)
        status = select_one('select status from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        self.assertEqual(modifyResult['status'],0)
        self.assertEqual(modifyResult['msg'],u'修改成功')
        self.assertEqual(status['status'],int(self.ReceiveCouponInfo.status))

    #修改红包启用和停用时间
    def test_modifyReceiveCoupon_time(self):
        activityId=self.createDealerActivity(activityType=self.ReceiveCouponInfo.activityType)
        modifyResult = self.dlservice.modifyDealerActivity(activityId=activityId,autoEnable=self.ReceiveCouponInfo.autoEnable1,autoDisable=self.ReceiveCouponInfo.autoDisable1)
        couponActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        autoEnable = select_one('select auto_enable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        autoDisable = select_one('select auto_disable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        self.assertEqual(self.timeStrtoTimeStamp(str(autoEnable['auto_enable'])),self.ReceiveCouponInfo.autoEnable1)
        self.assertEqual(self.timeStrtoTimeStamp(str(autoDisable['auto_disable'])),self.ReceiveCouponInfo.autoDisable1)
        self.assertEqual(modifyResult['status'],0)
        self.assertEqual(modifyResult['msg'],u'修改成功')

    #活动id不存在
    def test_modifyReceiveCoupon_couponIdNotExist(self):
        modifyResult = self.dlservice.modifyDealerActivity(activityId='343141411413243',autoEnable=self.ReceiveCouponInfo.autoEnable,autoDisable=self.ReceiveCouponInfo.autoDisable,status=self.ReceiveCouponInfo.status)
        self.assertEqual(modifyResult['status'], -1)
        self.assertEqual(modifyResult['msg'],u'修改/删除/优惠券/红包失败.')


    #更新优惠券状态为启用，成功
    def test_modifyReceiveBenefit_status(self):
        activityId=self.createDealerActivity(activityType=self.ReceiveBenefitInfo.activityType)
        modifyResult = self.dlservice.modifyDealerActivity(activityId=activityId,status=self.ReceiveBenefitInfo.status)
        benifitActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        status = select_one('select status from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', benifitActivityId['activity_id'])
        self.assertEqual(status['status'],int(self.ReceiveBenefitInfo.status))
        self.assertEqual(modifyResult['status'],0)
        self.assertEqual(modifyResult['msg'],u'修改成功')

    #修改优惠券启用和停用时间
    def test_modifyReceiveBenefit_time(self):
        activityId=self.createDealerActivity(activityType=self.ReceiveBenefitInfo.activityType)
        modifyResult = self.dlservice.modifyDealerActivity(activityId=activityId,autoEnable=self.ReceiveBenefitInfo.autoEnable1,autoDisable=self.ReceiveBenefitInfo.autoDisable1)
        couponActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        autoEnable = select_one('select auto_enable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        autoDisable = select_one('select auto_disable from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?', couponActivityId['activity_id'])
        self.assertEqual(self.timeStrtoTimeStamp(str(autoEnable['auto_enable'])),self.ReceiveBenefitInfo.autoEnable1)
        self.assertEqual(self.timeStrtoTimeStamp(str(autoDisable['auto_disable'])),self.ReceiveBenefitInfo.autoDisable1)
        self.assertEqual(modifyResult['status'],0)
        self.assertEqual(modifyResult['msg'],u'修改成功')

    #将时间格式''转化为时间戳
    def timeStrtoTimeStamp(self,timeStr):
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray)*1000)
        return str(timeStamp)


    def createDealerActivity(self,activityType):
        #创建领取红包的活动
        if activityType == '10':
            self.dltool.createReceiveCouponActivity()
            activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveCouponInfo.dealerCouponName,self.ReceiveCouponInfo.activityType)
        elif activityType == '11':
            self.dltool.createReceiveBenifitActivity()
            activityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', self.ReceiveBenefitInfo.dealerCouponName,self.ReceiveBenefitInfo.activityType)
        return activityId['activity_id']


    #用例执行完成后清理数据库
    def tearDown(self):
        self.dltool.deleteReceiveActivityBySQL()

def suite():
    suite=unittest.TestSuite()
    suite.addTest(modifyDealerActivity("test_modifyReceiveCoupon_status"))
    suite.addTest(modifyDealerActivity("test_modifyReceiveCoupon_time"))
    suite.addTest(modifyDealerActivity("test_modifyReceiveCoupon_couponIdNotExist"))
    suite.addTest(modifyDealerActivity("test_modifyReceiveBenefit_status"))
    suite.addTest(modifyDealerActivity("test_modifyReceiveBenefit_time"))
    suite.addTest(modifyDealerActivity("test_modifyReceiveCoupon_statusNoTime"))
    return suite