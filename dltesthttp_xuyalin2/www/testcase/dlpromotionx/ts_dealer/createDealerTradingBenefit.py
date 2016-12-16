#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest,datetime,time
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *
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

class createDealerTradingBenefit(unittest.TestCase):
    BenefitActivityInfo = eData('AvailableCouponsBenfits')
    dlservice = dlpromotionx()
    actID = BenefitActivityInfo.benefitActivityId
    benefitId=BenefitActivityInfo.dealerBenefitId
    timeStamp = int(time.mktime((datetime.datetime.now() + datetime.timedelta(days=3)).timetuple()) * 1000)

    #领取优惠券
    def receiveBenefit(self,companyId,activityId):
        queryResult = self.dlservice.createDealerTrading(companyId=companyId, activityId=activityId)
        return queryResult

    #将入参指定的优惠券置于已使用状态
    def useBenefit(self,benefitActivityId,dealer_coupon_id,tmlCompanyId):
        #   dealer_coupon_entity_status varchar(2) comment '经销商红包、优惠卷实体状态 01–未使用;02-已使用;03-锁定;04-已过期',
        update('update dlpromotionx.dl_dealer_coupon_snapshot set dealer_coupon_entity_status=? where dealer_coupon_id=?', '02', dealer_coupon_id)
        deleteActivityKey(benefitActivityId=benefitActivityId,benefitId=dealer_coupon_id,tmlCompanyId=tmlCompanyId)


    #造前提数据
    def setUp(self):
        self.tearDown()

    #经销商优惠券领取成功
    def test_createDealerTradingBenefit_benefitSuccess(self):
        queryResult=self.receiveBenefit(self.BenefitActivityInfo.tmlCompanyId,activityId=self.actID)
        # print queryResult
        self.assertEqual(2, queryResult['status'])
        self.assertEqual(3, queryResult['data']['remainNum'])
        # self.assertEqual( '优惠券领取成功！请稍后在我的优惠券中进行查看！',queryResult['msg'])

    #经销商优惠券领取成功
    def test_createDealerTradingBenefit_benefitNotUsed(self):
        queryResult1=self.receiveBenefit(self.BenefitActivityInfo.tmlCompanyId,activityId=self.actID)
        queryResult=self.receiveBenefit(self.BenefitActivityInfo.tmlCompanyId,activityId=self.actID)
        self.assertEqual(8, queryResult['status'])
        #self.assertEqual( '优惠券领取成功！请稍后在我的优惠券中进行查看！',queryResult['msg'])

    #7：对不起，该券一人只能领三次，您已领取三次，无法再次领取
    def test_shareDealerTrading_overLimitNum(self):
        queryResult1 = self.receiveBenefit(companyId=self.BenefitActivityInfo.tmlCompanyId, activityId=self.actID)
        self.assertEqual(queryResult1['status'], 2)
        time.sleep(30)
        self.useBenefit(benefitActivityId= self.actID ,dealer_coupon_id=self.BenefitActivityInfo.dealerBenefitId,tmlCompanyId=self.BenefitActivityInfo.tmlCompanyId)


        queryResult2 = self.receiveBenefit(companyId=self.BenefitActivityInfo.tmlCompanyId, activityId=self.actID)
        self.assertEqual(queryResult2['status'], 2)
        time.sleep(30)
        self.useBenefit(benefitActivityId= self.actID ,dealer_coupon_id=self.BenefitActivityInfo.dealerBenefitId,tmlCompanyId=self.BenefitActivityInfo.tmlCompanyId)
        time.sleep(30)

        queryResult3 = self.receiveBenefit(companyId=self.BenefitActivityInfo.tmlCompanyId, activityId=self.actID)
        self.assertEqual(queryResult3['status'], 2)
        time.sleep(30)
        self.useBenefit(benefitActivityId= self.actID ,dealer_coupon_id=self.BenefitActivityInfo.dealerBenefitId,tmlCompanyId=self.BenefitActivityInfo.tmlCompanyId)
        time.sleep(30)

        queryResult4 = self.receiveBenefit(companyId=self.BenefitActivityInfo.tmlCompanyId, activityId=self.actID)
        self.assertEqual(queryResult4['status'], 7)
        time.sleep(30)

    def test_shareDealerTrading_cannotRepeat(self):
        queryResult1 = self.receiveBenefit(companyId=self.BenefitActivityInfo.tmlCompanyId2, activityId=self.actID)
        self.assertEqual(queryResult1['status'], 2)
        queryResult2 = self.receiveBenefit(companyId=self.BenefitActivityInfo.tmlCompanyId2, activityId=self.actID)
        self.assertEqual(queryResult2['status'], 8)

        time.sleep(30)

        pass


    #经销商优惠券领取失败，优惠券已领完
    def test_createDealerTradingBenefit_benefitOutOfStock(self):
        queryResult2 = self.receiveBenefit(self.BenefitActivityInfo.tmlCompanyId, activityId=self.BenefitActivityInfo.benefitOutOfStock)
        # print queryResult2
        self.assertEqual(9, queryResult2['status'])
        # self.assertEqual('很抱歉，该优惠券已全部领完！您可以尝试领取其它好券！',queryResult2['msg'] )

    # 用例执行完成后删除创建和领取表中的记录
    def tearDown(self):
        couponId = select_one('SELECT dealer_coupon_id from dlcoupon.dl_dealer_coupon '
                              'where dealer_coupon_name = (SELECT activity_name from dlpromotionx.dl_dealer_coupon_activity where activity_id =?)',
                              self.actID)
        # print couponId
        if self.actID != None:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',
                   self.BenefitActivityInfo.dealerBenefitId)  # 领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',
                   self.BenefitActivityInfo.dealerBenefitId)  # 领取记录
            # 恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',
                   0, 0, couponId['dealer_coupon_id'])
        deleteActivityKey(benefitActivityId=self.actID,benefitId=self.benefitId,tmlCompanyId=self.BenefitActivityInfo.tmlCompanyId)  #删除redis中的缓存

def suite():
    suite=unittest.TestSuite()
    suite.addTest(createDealerTradingBenefit("test_createDealerTradingBenefit_benefitSuccess"))
    suite.addTest(createDealerTradingBenefit("test_createDealerTradingBenefit_benefitNotUsed"))
    suite.addTest(createDealerTradingBenefit("test_shareDealerTrading_overLimitNum"))
    suite.addTest(createDealerTradingBenefit("test_createDealerTradingBenefit_benefitOutOfStock"))
    suite.addTest(createDealerTradingBenefit("test_shareDealerTrading_cannotRepeat"))
    return suite
