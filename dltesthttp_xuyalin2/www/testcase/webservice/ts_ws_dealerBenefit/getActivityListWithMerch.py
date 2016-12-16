#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
LB05.商品详情：可领优惠券列表(与商品相关)
http://127.0.0.1:8280/mallws/dealerBenefit/getActivityListWithMerch.json
{
	"token":"123",
	"merchId":"67d4cb03595348cdacd61000bc96ba03"                   // 必须 商品ID
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                             // 0-成功 1-失败
		"activityList": [                                          // 优惠券活动列表
			{
				"activityId":"activity01",                         // 优惠券活动主健
				"activityStatus":"01",                             // 优惠券活动状态：01-可领取 02-已领取 03-已领完 04-已过期
				"couponAmt":"20000",                               // 优惠券金额：单位分
				"amtUseLimit":"满200可以使用",                     // 金额使用限制
				"dealerLimit":"湖北人人大",                        // 经销商使用限制
				"channelLimit":"烟酒专卖店",                       // 渠道使用限制
				"merchLimit":"白云边1919",                         // 商品使用限制
				"platformLimit":"web,app",                         // 平台使用限制
				"expireDate":"2016-09-18",                         // 过期日期
				"useDate":"2016-09-01"                             // 使用日期
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerBenefit.GetActivityListWithMerchResponse"
    }
}

"""
class getActivityListWithMerch(unittest.TestCase):
    UserShop=wsData('TmlShop')
    Merch=wsData('Merch1')
    coupon1=eData('AvailableCouponsBenfits')

    def setUp(self):
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch.goodsId)

    #正确获取商品详情页的可领优惠券列表
    def test_getActivityListWithMerch(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getActivity=ws.getActivityListWithMerch(merchId=self.Merch.goodsId)
        self.assertEqual(getActivity.model['success'],'0')
        self.assertSuccess(getActivity)

    #merchId为空
    def test_getActivityListWithMerch_null(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getActivity=ws.getActivityListWithMerch(merchId='')
        self.assertEqual(getActivity.model['success'],'1')
        self.assertEqual(getActivity.model['activityList'],None)

    #merchId不存在
    def test_getActivityListWithMerch_error(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getActivity=ws.getActivityListWithMerch(merchId='1234567890')
        self.assertEqual(getActivity.model['success'],'0')
        self.assertEqual(getActivity.model['activityList'],None)

    #商品已下架
    def test_getActivityListWithMerch_under(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','02',self.Merch.goodsId)
        getActivity=ws.getActivityListWithMerch(merchId=self.Merch.goodsId)
        self.assertEqual(getActivity.model['success'],'0')
        # self.assertEqual(getActivity.model['activityList'],None)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch.goodsId)

    #商品已锁定
    def test_getActivityListWithMerch_lock(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','03',self.Merch.goodsId)
        getActivity=ws.getActivityListWithMerch(merchId=self.Merch.goodsId)
        self.assertEqual(getActivity.model['success'],'0')
        # self.assertEqual(getActivity.model['activityList'],None)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch.goodsId)

    #商品已删除
    def test_getActivityListWithMerch_delete(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','99',self.Merch.goodsId)
        getActivity=ws.getActivityListWithMerch(merchId=self.Merch.goodsId)
        self.assertEqual(getActivity.model['success'],'0')
        # self.assertEqual(getActivity.model['activityList'],None)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch.goodsId)

    #无token值
    def test_getActivityListWithMerch_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getActivity=ws.getActivityListWithMerch(merchId=self.Merch.goodsId,token='null')
        self.assertEqual(getActivity.code,600)

    #验证返回数据的正确性
    def assertSuccess(self,res=None):
        if res.model['activityList'] is not None:
            coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',self.coupon1.dealerBenefitId)
            couponActivity=select_one('select * from dlpromotionx.dl_dealer_coupon_activity where activity_id=?',self.coupon1.benefitActivityId)
            self.assertEqual(res.model['activityList'][0]['activityId'],self.coupon1.benefitActivityId)
            self.assertEqual(res.model['activityList'][0]['activityStatus'],'01')
            self.assertEqual(res.model['activityList'][0]['couponAmt'],str(coupon.coupon_min_amt))
            self.assertEqual(res.model['activityList'][0]['amtUseLimit'],str(coupon.effective_amt))
            self.assertEqual(res.model['activityList'][0]['dealerLimit'],couponActivity.dealer_name)
            self.assertEqual(res.model['activityList'][0]['merchLimit'],couponActivity.goods_name)
            self.assertIn(res.model['activityList'][0]['expireDate'],str(couponActivity.uneffective_time))
            self.assertIn(res.model['activityList'][0]['useDate'],str(couponActivity.effective_time))


    def tearDown(self):
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch.goodsId)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch"))
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch_null"))
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch_error"))
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch_under"))
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch_lock"))
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch_delete"))
    suite.addTest(getActivityListWithMerch("test_getActivityListWithMerch_tokenNull"))
    return suite