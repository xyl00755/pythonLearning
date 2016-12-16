#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *
from www.operation.redisCache import *

"""
WQ03.提交订单页获取商品优惠券
http://127.0.0.1:8280/mallws/dealerBenefit/getCouponWithMerch.json
{
	"token":"123",
	"merchIdList":[												 // 必须 商品id
		"67d4cb03595348cdacd61000bc96ba03",
		"67d4cb03595348cdacd61000bc96ba03"
	]
}

{
	"code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
		"couponModelList":[{
			"merchId":"67d4cb03595348cdacd61000bc96ba03",			 // 商品id
			"flag":"true",											 // 是否有优惠券 true-有;false-没有
			"coupon":{
				"couponCode":"",                                         // 优惠券编号
				"couponName":"",                                         // 优惠券名称
				"couponAmt":"2000",                                      // 优惠券金额(满100减20)
				"amtLimit":"10000"									     // 使用限制金额
			}
		}]
	},
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerBenefit.GetCouponWithMerchResponse"
    }
}
"""

class getCouponWithMerch(unittest.TestCase):
    UserShop = wsData('TmlShop')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    coupon1 = eData('AvailableCouponsBenfits')

    def setUp(self):
        self.tearDown()

    #正确获取一个商品优惠券
    def test_getCouponWithMerch_one(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        ws.achieveCoupon(activityId=self.coupon1.benefitActivityId)
        time.sleep(30)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertCouponModelList(coup=getCoupon)

    #正确获取两个商品优惠券
    def test_getCouponWithMerch_two(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        ws.achieveCoupon(activityId=self.coupon1.benefitActivityId)
        time.sleep(30)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId,self.Merch2.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertCouponModelList(coup=getCoupon)

    #商品id为空
    def test_getCouponWithMerch_goodsNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponWithMerch(merchIdList=[])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponModelList'],[])

    #商品已下架
    def test_getCouponWithMerch_goodsUnder(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','02',self.Merch1.goodsId)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponModelList'][0]['merchId'],self.Merch1.goodsId)
        self.assertEqual(getCoupon.model['couponModelList'][0]['flag'],'false')
        self.assertEqual(getCoupon.model['couponModelList'][0]['coupon'],None)

    #商品已锁定
    def test_getCouponWithMerch_goodsLock(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','03',self.Merch1.goodsId)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponModelList'][0]['merchId'],self.Merch1.goodsId)
        self.assertEqual(getCoupon.model['couponModelList'][0]['flag'],'false')
        self.assertEqual(getCoupon.model['couponModelList'][0]['coupon'],None)

    #商品已删除
    def test_getCouponWithMerch_goodsDelet(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','99',self.Merch1.goodsId)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponModelList'][0]['merchId'],self.Merch1.goodsId)
        self.assertEqual(getCoupon.model['couponModelList'][0]['flag'],'false')
        self.assertEqual(getCoupon.model['couponModelList'][0]['coupon'],None)

    #商品无价格
    def test_getCouponWithMerch_goodsNoPrice(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set price_retail=? where goods_id=?','0',self.Merch1.goodsId)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponModelList'][0]['merchId'],self.Merch1.goodsId)
        self.assertEqual(getCoupon.model['couponModelList'][0]['flag'],'false')
        self.assertEqual(getCoupon.model['couponModelList'][0]['coupon'],None)

    #商品无库存
    def test_getCouponWithMerch_goodsNoInventory(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set on_hand_inventory=? where goods_id=?','0',self.Merch1.goodsId)
        getCoupon=ws.getCouponWithMerch(merchIdList=[self.Merch1.goodsId])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponModelList'][0]['merchId'],self.Merch1.goodsId)
        self.assertEqual(getCoupon.model['couponModelList'][0]['flag'],'false')
        self.assertEqual(getCoupon.model['couponModelList'][0]['coupon'],None)

    def assertCouponModelList(self,coup):
        couponLen=len(coup.model['couponModelList'])
        for i in range(couponLen):
            getFlag=coup.model['couponModelList'][i]['flag']
            if getFlag=='true':
                couponList=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id=? and issue_person=?',self.coupon1.benefitActivityId,self.coupon1.tmlCompanyId)
                couponEntityId=couponList.dealer_coupon_entity_id
                couponEntity=select_one('select * from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id=?',couponEntityId)
                coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',self.coupon1.dealerBenefitId)
                self.assertEqual(coup.model['couponModelList'][i]['coupon']['couponCode'],couponEntityId)
                self.assertEqual(coup.model['couponModelList'][i]['coupon']['couponName'],couponEntity.dealer_coupon_name)
                self.assertEqual(coup.model['couponModelList'][i]['coupon']['couponAmt'],str(coupon.coupon_min_amt))
                self.assertEqual(coup.model['couponModelList'][i]['coupon']['amtLimit'],str(couponEntity.effective_amount))
            else:
                self.assertEqual(coup.model['couponModelList'][i]['coupon'],None)


    def tearDown(self):
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch1.goodsId)
        update('update dlmerchandise.dl_goods set price_retail=? where goods_id=?','36000',self.Merch1.goodsId)
        update('update dlmerchandise.dl_goods set on_hand_inventory=? where goods_id=?','999',self.Merch1.goodsId)
        update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',self.coupon1.dealerBenefitId)  # 领取实体快照
        update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',self.coupon1.dealerBenefitId)  # 领取记录
        # 恢复库存
        update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',0,0,self.coupon1.dealerBenefitId)
        deleteActivityKey(benefitActivityId=self.coupon1.benefitActivityId,benefitId=self.coupon1.dealerBenefitId,tmlCompanyId=self.coupon1.tmlCompanyId)  #删除redis中的缓存

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_one"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_two"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_goodsNull"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_goodsUnder"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_goodsLock"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_goodsDelet"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_goodsNoPrice"))
    suite.addTest(getCouponWithMerch("test_getCouponWithMerch_goodsNoInventory"))
    return suite

