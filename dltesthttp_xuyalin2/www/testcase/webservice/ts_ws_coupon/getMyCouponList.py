#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0283.获取优惠劵列表（个人中心：未使用，已过期，已使用）
http://127.0.0.1:8280/mallws/coupon/getMyCouponList.json
{
	"token":"123",
    "companyId": "campany0101",                                // 企业Id
	"couponStatus":"1",                                        // 优惠劵状态（01–未使用;02-已使用;03-锁定;04-已过期）
    "page":1,                                                  // 必须
    "rows":15                                                  // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                            // 0-成功 1-失败
		"couponList": [                                           // 可用优惠券列表
			{
				"couponId":"",                                    // 优惠券id
				"couponCode":"",                                  // 优惠券编号
				"couponName":"",                                  // 优惠券名称（丹露红包）
				"kindsLimit":"",                                  // 品类限制,"葡萄酒，白酒" 若全品类则返回""
				"couponStatus":"",                                // 优惠劵状态（01–未使用;02-已使用;03-锁定;04-已过期）
				"couponAmt":"",                                   // 优惠券金额
				"expireDay":"",                                   // 过期日期
				"useTime":"",                                     // 使用时间
				"timeLeft":"",                                    // 剩余天数
				"orderList" [
					"orderNo0001",
                    "orderNo0002"		                          // 订单号
                ]

			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.coupon.GetMyCouponListResponse"
    }
}
"""
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData



class getMyCouponList(unittest.TestCase):
    UserShop = wsData('TmlShop')
    Merch1 = wsData('Merch1')
    #获取未使用的优惠券数量（部分显示）
    def test_getMyCouponList_NotUsePart(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        getMyCouponListRst = ws.getMyCouponList(companyId=self.UserShop.companyId,couponStatus='01',page='1',rows='5')
        self.assertEquals(getMyCouponListRst.code, 200)
        self.assertEquals(getMyCouponListRst.model['success'], '0')
        self.assertEquals(len(getMyCouponListRst.model['couponList']), 5)

    #获取未使用的优惠券数量（全部显示）
    def test_getMyCouponList_NotUseAll(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        getMyCouponListRst = ws.getMyCouponList(companyId=self.UserShop.companyId, couponStatus='01', page='1', rows='15')
        self.assertEquals(getMyCouponListRst.code, 200)
        self.assertEquals(getMyCouponListRst.model['success'], '0')
        self.assertEquals(len(getMyCouponListRst.model['couponList']), 15)

    #获取已使用的优惠券数量
    def test_getMyCouponList_UseAll(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDB = select('select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person=? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',self.UserShop.companyId,'02')
        getMyCouponListRst = ws.getMyCouponList(companyId=self.UserShop.companyId, couponStatus='02', page='1',rows='10')
        self.assertEquals(getMyCouponListRst.code, 200)
        self.assertEquals(getMyCouponListRst.model['success'], '0')
        self.assertEquals(len(getMyCouponListRst.model['couponList']), len(RstDB))

    #获取锁定的优惠券数量
    def test_getMyCouponList_Locking(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDB = select(
            'select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person=? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',
            self.UserShop.companyId, '03')
        getMyCouponListRst = ws.getMyCouponList(companyId=self.UserShop.companyId, couponStatus='03', page='1',rows='10')
        self.assertEquals(getMyCouponListRst.code, 200)
        self.assertEquals(getMyCouponListRst.model['success'], '0')
        self.assertEquals(len(getMyCouponListRst.model['couponList']), len(RstDB))

    #获取已过期的优惠券数量
    def test_getMyCouponList_Overdue(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDB = select(
            'select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person=? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',
            self.UserShop.companyId, '04')
        getMyCouponListRst = ws.getMyCouponList(companyId=self.UserShop.companyId, couponStatus='04', page='1',rows='10')
        self.assertEquals(getMyCouponListRst.code, 200)
        self.assertEquals(getMyCouponListRst.model['success'], '0')
        self.assertEquals(len(getMyCouponListRst.model['couponList']), len(RstDB))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getMyCouponList('test_getMyCouponList_NotUsePart'))
    suite.addTest(getMyCouponList('test_getMyCouponList_NotUseAll'))
    suite.addTest(getMyCouponList('test_getMyCouponList_UseAll'))
    suite.addTest(getMyCouponList('test_getMyCouponList_Locking'))
    suite.addTest(getMyCouponList('test_getMyCouponList_Overdue'))
    return suite