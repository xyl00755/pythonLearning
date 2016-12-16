#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from www.common.database import *
from www.common.excel import *
from www.api.webservice import *
from www.operation.redisCache import *


"""
LB03.领券中心、抢经销商红包：领取优惠券、抢经销商红包
http://127.0.0.1:8280/mallws/dealerCoupon/achieveCoupon.json
{
	"token":"123",
    "activityId":"activity01"                                      // 必须 优惠券活动主健
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                             // （待定）0-成功 1-失败 2-已领完
		"couponId": "c01010546"                                    // 优惠券/红包id
		"couponAmt":"15000"										   // 优惠券/红包金额
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.AchieveCouponResponse"
    }
}
"""
class achieveGiftMoney(unittest.TestCase):
    UserCoupon = eData('TmlShop3') #登录帐号
    CouponLst4 = eData('CouponLst4') #经销商优惠卷
    GiftMoney1 = eData('GiftMoney1') #经销商红包
    gmActivity = CouponLst4.activityId

    #查询优惠卷数量是否能够领取
    def setUp(self):
        self.tearDown()

    #领取1张经销商优惠卷
    def test_getCoupon_dealer(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        achieveCoupon = ws.achieveCoupon(self.GiftMoney1.activityId)
        self.test_assertEqual_parameter(achieveCoupon,self.GiftMoney1)


    #领取经销商优惠卷without token
    def test_useCouponList_withoutToken(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        achieveCoupon = ws.achieveCoupon(self.CouponLst4.activityIdWhiteWine,token = 'null')
        self.assertEqual(achieveCoupon.code,600)
        flag = False
        if achieveCoupon.model is None:
          flag = True
          self.assertEqual(flag,True,'the response is wrong')

    #领取经销商红包without token
    def test_useGiftMoney_withoutToken(self):
        ws = webservice()
        ws.login(self.UserCoupon.username, self.UserCoupon.password)
        achieveCoupon = ws.achieveCoupon(self.GiftMoney1.activityId,token = 'null')
        self.assertEqual(achieveCoupon.code,600)
        flag = False
        if achieveCoupon.model is None:
            flag = True
            self.assertEqual(flag, True, 'the response is wrong')

    #领取已经领完的优惠卷活动
    def test_useCouponList_Null(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        update('update dlcoupon.dl_coupon_detail SET package_amount = ?,package_grant_amount = ? where coupon_id = ?','9999','9999',self.CouponLst4.couponId)
        achieveCoupon = ws.achieveCoupon(self.CouponLst4.activityId)
        self.assertEqual(achieveCoupon.code,200)
        flag = False
        if achieveCoupon.model['success'] == 2:
            if achieveCoupon.model['couponId'] is None:
                if achieveCoupon.model['couponAmt'] is None:
                    if achieveCoupon.model['leftTimes'] is None:
                      flag = True
                      self.assertEqual(flag,True,'the response is wrong')


    #领取经销商优惠卷并验证领取后优惠卷的数量
    def test_useCouponList_getFree(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        achieveCoupon = ws.achieveCoupon(activityId=self.coupon4.activityId)
        print('after  800 seconds,it will check the number of coupon which has been achieved')
        time.sleep(30)
        coupon = select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',self.coupon1.dealerBenefitId)
        self.assertEqual(coupon.package_grant_amount, 1)
        self.assertEqual(achieveCoupon.model['success'], '0')
        self.assertEqual(achieveCoupon.model['couponId'], self.coupon4.couponId)
        self.assertEqual(achieveCoupon.model['couponAmt'], '99900')
        self.assertEqual(achieveCoupon.model['leftTimes'], '3')

    #领取经销商红包并验证领取后的数量
    def test_useGiftMoney_getFree(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        achieveCoupon = ws.achieveCoupon(activityId=self.GiftMoney1.activityId)
        print('after  800 seconds,it will check the number of coupon which has been achieved')
        time.sleep(30)
        coupon = select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?', self.GiftMoney1.couponId)
        self.assertEqual(coupon.package_grant_amount, 1)
        self.assertEqual(achieveCoupon.model['success'], '0')
        self.assertEqual(achieveCoupon.model['couponId'], self.GiftMoney1.couponId)
        self.assertEqual(achieveCoupon.model['couponAmt'], '99900')
        self.assertEqual(achieveCoupon.model['leftTimes'], '3')

    #重复领取经销商优惠卷
    def test_useCouponMoney_getRepition(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        for i in range(0,2):
            achieveCoupon = ws.achieveCoupon(self.CouponLst4.activityId)
        self.assertEqual(achieveCoupon.code,200)
        flag = False
        if achieveCoupon.model['success'] == '2':
            if achieveCoupon.model['couponId'] == 'Null':
                if achieveCoupon.model['couponAmt'] == 'Null':
                     flag = True
                     self.assertEqual(flag,True,self.CouponLst4.CouponId + ' '+'has being get already')

    #重复领取经销商红包
    def test_useGiftMoney_getRepition(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        for k in range(0,2):
            achieveCoupon = ws.achieveCoupon(self.GiftMoney1.activityId)
        self.assertEqual(achieveCoupon.code,200)
        flag = False
        if achieveCoupon.model['success'] == '0':
            if achieveCoupon.model['couponId'] == self.GiftMoney1.couponId:
                if achieveCoupon.model['couponAmt'] == self.GiftMoney1.couponAmt:
                    flag = True
                    self.assertEqual(flag,True,self.GiftMoney1.activityId + ' '+'has being get already')

    #领取未启用的经销商优惠卷
    def test_useGiftMoney_notEnable(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        achieveCoupon = ws.achieveCoupon(self.CouponLst4.activityId01)
        self.assertEqual(achieveCoupon.code,200)
        flag = False
        if achieveCoupon.model['success'] == '2':
            if achieveCoupon.model['couponId'] == 'Null':
                if achieveCoupon.model['couponAmt'] == 'Null':
                    flag = True
                    self.assertEqual(flag,True,self.CouponLst4.activityId01 + 'has been get wrong')

    #领取不允许的终端店类型的优惠卷
    def test_useCouponMoney_byanotherUserformate(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        achieveCoupon = ws.achieveCoupon(self.CouponLst4.acitivityId02)
        self.assertEqual(achieveCoupon.code,200)
        flag = False
        if achieveCoupon.model['success'] == '2':
            if achieveCoupon.model['couponId'] == 'Null':
                if achieveCoupon.model['couponAmt'] == 'Null':
                    flag = True
                    self.assertEqual(flag,True,self.CouponLst4.acitivityId02 +'has been get wrong')

    #领取不在对分发地域里面的优惠卷
    def test_assertEqual_notInTheSection(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        achieveCoupon = ws.achieveCoupon(self.CouponLst4.activityId03)
        self.assertEqual(achieveCoupon.code,200)
        flag = False
        if achieveCoupon.model['success'] == '2':
            if achieveCoupon.model['couponId'] == 'Null':
                if achieveCoupon.model['couponAmt'] == 'Null':
                    flag = True
                    self.assertEqual(flag,True,self.CouponLst4.activityId03 + 'has been get wrong')

    #校验response body的字段类型
    def test_assertEqual_parameter(self):
         ws = webservice()
         ws.login(self.UserCoupon.username,self.UserCoupon.password)
         achieveCoupon = ws.achieveCoupon(self.GiftMoney1.activityId)
         self.assertEqual(achieveCoupon.code,200)

    def test_assertRsp_body(self,rsp,giftMoney,success = '0'):
        self.assertEqual(rsp.model['success'],success)
        flag = False
        if rsp.model['couponId'] == giftMoney.couponId:
            if rsp.model['couponAmt'] == giftMoney.couponAmt:
                flag = True
        self.assertEqual(flag,True,'the response formate is wrong ')

    # 用例执行完成后删除领取表中的记录
    def deleteSql(self, couponType=None):
        if couponType == 11:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',
               self.coupon1.dealerBenefitId)  # 领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',
               self.coupon1.dealerBenefitId)  # 领取记录
        # 恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?', 0,
               0, self.coupon1.dealerBenefitId)
            deleteActivityKey(benefitActivityId=self.coupon4.activityId, benefitId=self.coupon4.activityId,
                          tmlCompanyId=self.coupon4.activityId)  # 删除redis中的缓存
        else:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',
               self.coupon1.dealerCouponId)  # 领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',
               self.coupon1.dealerCouponId)  # 领取记录
        # 恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?', 0,
               0, self.coupon4.activityId)
            deleteActivityKey(couponActivityId=self.coupon1.couponActivityId, tmlCompanyId=self.coupon4.activityId)  # 删除redis中的缓存


    def tearDown(self):
        self.deleteSql(couponType=11)  # 11代表经销商优惠券
        self.deleteSql(couponType=10)  # 10代表经销商红包



def  suite():
    suite = unittest.TestSuite()
    suite.addTest(achieveGiftMoney("test_getCoupon_dealer"))
    suite.addTest(achieveGiftMoney("test_useCouponList_withoutToken"))
    suite.addTest(achieveGiftMoney("test_useGiftMoney_withoutToken"))
    suite.addTest(achieveGiftMoney("test_useCouponList_Null"))
    suite.addTest(achieveGiftMoney("test_useCouponList_getFree"))
    suite.addTest(achieveGiftMoney("test_useGiftMoney_getFree"))
    suite.addTest(achieveGiftMoney("test_useCouponMoney_getRepition"))
    suite.addTest(achieveGiftMoney("test_useGiftMoney_getRepition"))
    suite.addTest(achieveGiftMoney("test_useGiftMoney_notEnable"))
    suite.addTest(achieveGiftMoney("test_useCouponMoney_byanotherUserformate"))
    suite.addTest(achieveGiftMoney("test_assertEqual_notInTheSection"))
    suite.addTest(achieveGiftMoney("test_assertEqual_parameter"))
    return suite
