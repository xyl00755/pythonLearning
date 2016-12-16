#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *
from www.operation.redisCache import *

"""

WQ05.提交订单页获取经销商红包列表（包括：可用红包，不可用红包）
http://127.0.0.1:8280/mallws/dealerCoupon/getCouponListWithDealer.json
{
	"token":"123",
	"dealerId":"123"										      // 必须 经销商ID
	"totalAmt":"15000"											  // 必须 订单中该经销商下所有商品总额(扣除满减满赠后)单位：分
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "useableCouponList": [                                    // 可用经销商红包列表
			{
				"couponCode":"10006230",                          // 优惠券/红包编号
				"orderNo":"1011",								  // 使用订单编号(已使用的经销商优惠券/红包特有)
				"couponName":"**优惠券",                          // 优惠券/红包名称
				"couponStatus":"01",                              // 优惠劵/红包状态（01–未使用;02-已使用;03-已过期）
				"couponAmt":"20000",                              // 优惠券/红包金额
				"timeLeft":"12",							      // 剩余天数
				"expireDate":"2016-09-18",                        // 过期日期
				"useDate":"2016-09-01",                           // 使用日期
                "amtUseLimit":"满200可以使用",                    // 金额使用限制
				"dealerLimit":"湖北人人大",                       // 经销商使用限制
				"channelLimit":"烟酒专卖店",                      // 渠道使用限制
				"merchLimit":"白云边1919",                        // 商品使用限制
				"platformLimit":"web,app",                        // 平台使用限制
			}
        ]
		"unUseableCouponList": [                                  // 不可用经销商红包列表
			{
				"couponCode":"10006230",                          // 优惠券/红包编号
				"orderNo":"1011",								  // 使用订单编号(已使用的经销商优惠券/红包特有)
				"couponName":"**优惠券",                          // 优惠券/红包名称
				"couponStatus":"01",                              // 优惠劵/红包状态（01–未使用;02-已使用;03-已过期）
				"couponAmt":"20000",                              // 优惠券/红包金额
				"timeLeft":"12",							      // 剩余天数
				"expireDate":"2016-09-18",                        // 过期日期
				"useDate":"2016-09-01",                           // 使用日期
                "amtUseLimit":"满200可以使用",                    // 金额使用限制
				"dealerLimit":"湖北人人大",                       // 经销商使用限制
				"channelLimit":"烟酒专卖店",                      // 渠道使用限制
				"merchLimit":"白云边1919",                        // 商品使用限制
				"platformLimit":"web,app",                        // 平台使用限制
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.GetCouponListWithDealerResponse"
    }
}
"""

class getCouponListWithDealer(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('DealMager')
    coupon1=eData('AvailableCouponsBenfits')

    def setUp(self):
        self.tearDown()

    #正确获取经销商可用红包列表
    def test_getCouponListWithDealer_useful(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        achieve=ws.achieveCoupon(activityId=self.coupon1.couponActivityId)
        time.sleep(30)
        getCouponList=ws.getCouponListWithDealer(dealerId=self.UserShop2.companyId,totalAmt='15')
        self.assertEqual(getCouponList.model['success'],'0')
        self.assertSuccess(res=getCouponList)

    #正确获取不可用红包列表
    def test_getCouponListWithDealer_unUserful(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        achieve=ws.achieveCoupon(activityId=self.coupon1.couponActivityId)
        time.sleep(30)
        getCouponList=ws.getCouponListWithDealer(dealerId=self.UserShop2.companyId,totalAmt='-123')
        self.assertEqual(getCouponList.model['success'],'0')
        self.assertEqual(getCouponList.model['useableCouponList'],None)
        self.assertNotEqual(getCouponList.model['unUseableCouponList'],None)
        self.assertEqual(len(getCouponList.model['unUseableCouponList']),1)

    #dealerId不存在
    def test_getCouponListWithDealer_dealerIdError(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCouponList=ws.getCouponListWithDealer(dealerId='1234567890',totalAmt='15000')
        self.assertEqual(getCouponList.model['success'],'0')
        self.assertEqual(getCouponList.model['useableCouponList'],None)
        self.assertEqual(getCouponList.model['unUseableCouponList'],None)

    #dealerId为空
    def test_getCouponListWithDealer_dealerIdNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCouponList=ws.getCouponListWithDealer(dealerId='',totalAmt='15000')
        self.assertEqual(getCouponList.model['success'],'0')
        self.assertEqual(getCouponList.model['useableCouponList'],None)
        self.assertEqual(getCouponList.model['unUseableCouponList'],None)

    #totalAmt为空
    def test_getCouponListWithDealer_totalAmtNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCouponList=ws.getCouponListWithDealer(dealerId=self.UserShop2.companyId,totalAmt='')
        self.assertEqual(getCouponList.model['success'],'1')
        self.assertEqual(getCouponList.model['useableCouponList'],None)
        self.assertEqual(getCouponList.model['unUseableCouponList'],None)

    #totalAmt为0
    def test_getCouponListWithDealer_totalAmtZero(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCouponList=ws.getCouponListWithDealer(dealerId=self.UserShop2.companyId,totalAmt='0')
        self.assertEqual(getCouponList.model['success'],'0')
        self.assertEqual(getCouponList.model['useableCouponList'],None)
        self.assertEqual(getCouponList.model['unUseableCouponList'],None)

    def assertSuccess(self,res):
        couponList=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id=? and issue_person=?',self.coupon1.couponActivityId,self.coupon1.tmlCompanyId2)
        couponEntityId=couponList.dealer_coupon_entity_id
        couponEntity=select_one('select * from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id=?',couponEntityId)
        coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',self.coupon1.dealerCouponId)
        for i in range(len(res.model['useableCouponList'])):
            if res.model['useableCouponList'][i]['couponCode']==couponEntityId:
                self.assertEqual(res.model['useableCouponList'][i]['couponName'],couponEntity.dealer_coupon_name)
                self.assertEqual(res.model['useableCouponList'][i]['couponStatus'],couponEntity.dealer_coupon_entity_status)
                self.assertEqual(res.model['useableCouponList'][i]['couponAmt'],str(coupon.coupon_min_amt))
                self.assertIn(res.model['useableCouponList'][i]['expireDate'],str(couponEntity.uneffective_time))
                self.assertIn(res.model['useableCouponList'][i]['useDate'],str(couponEntity.effective_time))
                self.assertEqual(res.model['useableCouponList'][i]['amtUseLimit'],str(couponEntity.effective_amount))
                self.assertEqual(res.model['useableCouponList'][i]['dealerLimit'],couponEntity.dealer_name)
                self.assertEqual(res.model['useableCouponList'][i]['channelLimit'],'烟酒专卖店')
                self.assertEqual(res.model['useableCouponList'][i]['merchLimit'],None)
                self.assertEqual(res.model['useableCouponList'][i]['platformLimit'],'WEB;APP可用')

    def tearDown(self):
        update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',self.coupon1.dealerCouponId)  # 领取实体快照
        update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',self.coupon1.dealerCouponId)  # 领取记录
        # 恢复库存
        update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',0,0,self.coupon1.dealerCouponId)
        deleteActivityKey(couponActivityId=self.coupon1.couponActivityId,tmlCompanyId=self.coupon1.tmlCompanyId2)  #删除redis中的缓存

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCouponListWithDealer("test_getCouponListWithDealer_useful"))
    suite.addTest(getCouponListWithDealer("test_getCouponListWithDealer_unUserful"))
    suite.addTest(getCouponListWithDealer("test_getCouponListWithDealer_dealerIdError"))
    suite.addTest(getCouponListWithDealer("test_getCouponListWithDealer_dealerIdNull"))
    suite.addTest(getCouponListWithDealer("test_getCouponListWithDealer_totalAmtNull"))
    suite.addTest(getCouponListWithDealer("test_getCouponListWithDealer_totalAmtZero"))

    return suite