#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0280.获取优惠劵列表
http://127.0.0.1:8280/mallws/coupon/getCouponList.json
{
	"token":"123",
	"companyId": "campany0101",                              // 企业Id
    "merchList": [                                           // 商品列表模型
       "67d4cb03595348cdacd61000bc96ba03",                   // 必须 商品id
	   "67d4cb03595348cdacd61000bc96ba04"
    ]
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "useablecouponList": [                                    // 可用优惠券列表
			{
				"couponId":"",                                    // 优惠券id
				"couponCode":"",                                  // 优惠券编号
				"couponName":"",                                  // 优惠券名称
				"kindsLimit":"",                                  // 品类限制"葡萄酒，白酒" 若全品类则返回""
				"couponStatus":"",                                // 优惠劵状态（01–未使用;02-已使用;03-锁定;04-已过期）
				"couponAmt":"",                                   // 优惠券金额
				"expireDay":"",                                   // 过期日期
				"timeLeft":""                                     // 剩余天数
			}
        ]
		"unUseablecouponList": [                                  // 不可用优惠券列表
			{
				"couponId":"",                                    // 优惠券id
				"couponCode":"",                                  // 优惠券编号
				"couponName":"",                                  // 优惠券名称
				"kindsLimit":"",                                  // 品类限制"葡萄酒，白酒" 若全品类则返回""
				"couponStatus":"",                                // 优惠劵状态（01–未使用;02-已使用;03-锁定;04-已过期）
				"couponAmt":"",                                   // 优惠券金额
				"expireDay":"",                                   // 过期日期
				"timeLeft":""                                     // 剩余天数
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.coupon.GetCouponListResponse"
    }
}
优惠劵实体状态(01–未使用;02-已使用;03-锁定;04-已过期)
"""
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData


class getCouponList(unittest.TestCase):
    UserShop = wsData('TmlShop')
    Merch1 = wsData('Merch1')

    #获取优惠券列表(可用红包和不可用红包都为空)
    def test_getCouponList_Null(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where issue_person = ? ','testapp',self.UserShop.companyId)
        merchList=[self.Merch1.goodsId]
        couponList = ws.getCouponList(companyId=self.UserShop.companyId,merchList=merchList)
        self.assertEquals(couponList.code,200)
        self.assertEquals(couponList.model['success'],'0')
        self.assertEquals(couponList.model['useablecouponList'], None)
        self.assertEquals(couponList.model['unUseablecouponList'],None)
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where issue_person = ? ',self.UserShop.companyId, 'testapp')


    #获取优惠券列表(可用红包不为空，不可用红包为空)
    def test_getCouponList_notUseNull(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where issue_person = ? ', 'testapp', self.UserShop.companyId)
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where coupon_entity_id = ? ',self.UserShop.companyId, '113155442300030')
        merchList = [self.Merch1.goodsId]
        couponList = ws.getCouponList(companyId=self.UserShop.companyId, merchList=merchList)
        self.assertEquals(couponList.code, 200)
        self.assertEquals(couponList.model['success'], '0')
        self.assertEquals(len(couponList.model['useablecouponList']),1)
        self.assertEquals(len(couponList.model['unUseablecouponList']), 0)
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where issue_person = ? ', self.UserShop.companyId, 'testapp')
    #获取优惠券列表（可用红包，不可用红包都存在）
    def test_getCouponList_All(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchList = [self.Merch1.goodsId]
        couponList = ws.getCouponList(companyId=self.UserShop.companyId, merchList=merchList)
        RstDB=select(
            'select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person=? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',
            self.UserShop.companyId, '01')
        RstDBunUseable=select(
            'select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person = ? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? and dlpromotionx.dl_promotionx_coupon_snapshot.category not like ? ',
            self.UserShop.companyId, '01','%C01L0101%')
        self.assertEquals(couponList.code, 200)
        self.assertEquals(couponList.model['success'], '0')
        self.assertEquals(len(couponList.model['useablecouponList']),len(RstDB)-len(RstDBunUseable))
        self.assertEquals(len(couponList.model['unUseablecouponList']), len(RstDBunUseable))
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where issue_person = ? ',self.UserShop.companyId, 'testapp')

    #商品ID为空，获取优惠券列表
    def test_getCouponList_IDNull(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchList = None
        couponList = ws.getCouponList(companyId=self.UserShop.companyId, merchList=merchList)
        self.assertEquals(couponList.code,200)
        self.assertEquals(couponList.model['success'], '0')
        self.assertEquals(couponList.model['useablecouponList'], None)
        self.assertEquals(couponList.model['unUseablecouponList'], None)


def tearDown(self):
        update('update dlpromotionx.dl_promotionx_coupon_issue_record set issue_person = ? where issue_person = ? ',self.UserShop.companyId, 'testapp')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCouponList('test_getCouponList_Null'))
    suite.addTest(getCouponList('test_getCouponList_notUseNull'))
    suite.addTest(getCouponList('test_getCouponList_IDNull'))
    suite.addTest(getCouponList('test_getCouponList_All'))
    return suite
