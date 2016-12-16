#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *
from www.testcase.dlpromotionx.tool.createDealerActivityTool import *
import datetime

from www.operation.redisCache import *

"""
POST http://dlpromotionx.com/dealer/create_dealer_trading
 {
    "companyId": "0000d96033cd441c8a9fdee3f99a20dd",
    "activityId": "0210836632302",

  }
返回示例：
    {
    "status": 0,
    "msg": ”券已领取成功，可在‘我的优惠券’中进行查看“,
    "data": {
      "couponId": "2023642603",
      "couponAmt": "20",
    }
  }
"""



class createDealerTradingCoupon(unittest.TestCase):
    CouponActivityInfo = eData('AvailableCouponsBenfits')
    dlservice = dlpromotionx()
    actID = CouponActivityInfo.couponActivityId
    timeStamp = int(time.mktime((datetime.datetime.now() + datetime.timedelta(days=3)).timetuple()) * 1000)

    #领取红包
    def receiveCoupon(self,companyId,activityId):
        queryResult = self.dlservice.createDealerTrading(companyId=companyId, activityId=activityId)
        return queryResult

    #将入参指定的优惠券置于已使用状态
    def useBenefit(self,dealer_coupon_id):
        #   dealer_coupon_entity_status varchar(2) comment '经销商红包、优惠卷实体状态 01–未使用;02-已使用;03-锁定;04-已过期',
        update('update dlpromotionx.dl_dealer_coupon_snapshot set dealer_coupon_entity_status=? where dealer_coupon_id=?', '02', dealer_coupon_id)

    #恢复前提数据
    def setUp(self):
        self.tearDown()

    #经销商红包领取成功
    def test_createDealerTradingCoupon_couponSuccess(self):
        queryResult=self.receiveCoupon(self.CouponActivityInfo.tmlCompanyId2,activityId=self.actID)
        # print queryResult
        self.assertEqual( queryResult['status'],0)
        #self.assertEqual('经销商红包领取成功！请稍后在我的经销商红包中进行查看！',queryResult['msg'] )
        time.sleep(20)

    #7：对不起，该红包一人只能领三次，您已领取三次，无法再次领取！
    def test_shareDealerTrading_overLimitNum(self):
        queryResult1 = self.receiveCoupon(companyId=self.CouponActivityInfo.tmlCompanyId2, activityId=self.actID)
        self.assertEqual(queryResult1['status'], 0)
        time.sleep(20)
        # self.useBenefit(self.CouponActivityInfo.dealerCouponId)

        queryResult2 = self.receiveCoupon(companyId=self.CouponActivityInfo.tmlCompanyId2, activityId=self.actID)
        # print queryResult2
        self.assertEqual(queryResult2['status'], 0)
        time.sleep(20)
        # self.useBenefit(self.CouponActivityInfo.dealerCouponId)

        queryResult3 = self.receiveCoupon(companyId=self.CouponActivityInfo.tmlCompanyId2, activityId=self.actID)
        # print queryResult3
        self.assertEqual(queryResult3['status'], 0)
        time.sleep(20)
        # self.useBenefit(self.CouponActivityInfo.dealerCouponId)

        queryResult4 = self.receiveCoupon(companyId=self.CouponActivityInfo.tmlCompanyId2, activityId=self.actID)
        # print queryResult4
        self.assertEqual(queryResult4['status'], 7)
        time.sleep(20)


    #1.经销商红包领取失败，红包已领完
    def test_createDealerTradingCoupon_couponOutOfStock(self):
        update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',
               400, 4, self.CouponActivityInfo.dealerCouponId)
        queryResult = self.receiveCoupon(self.CouponActivityInfo.tmlCompanyId2, activityId=self.actID)
        self.assertEqual(queryResult['status'], 1)
        #self.assertEqual(queryResult2['msg'], '很抱歉，该经销商红包已全部领完！您可以尝试领取其他经销商红包！')


    #用例执行完成后删除领取表中的记录
    def tearDown(self):
        #self.dltool.deleteReceiveActivityBySQL()
        couponId=select_one('SELECT dealer_coupon_id from dlcoupon.dl_dealer_coupon '
                            'where dealer_coupon_name = (SELECT activity_name from dlpromotionx.dl_dealer_coupon_activity where activity_id =?)', self.actID)
        # print couponId
        if self.actID != None:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',couponId['dealer_coupon_id'])  #领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',couponId['dealer_coupon_id'])  #领取记录
            #恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?', 0, 0, couponId['dealer_coupon_id'])
        deleteActivityKey(couponActivityId=self.actID,tmlCompanyId=self.CouponActivityInfo.tmlCompanyId2)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(createDealerTradingCoupon("test_createDealerTradingCoupon_couponSuccess"))
    suite.addTest(createDealerTradingCoupon("test_shareDealerTrading_overLimitNum"))
    suite.addTest(createDealerTradingCoupon("test_createDealerTradingCoupon_couponOutOfStock"))

    return suite