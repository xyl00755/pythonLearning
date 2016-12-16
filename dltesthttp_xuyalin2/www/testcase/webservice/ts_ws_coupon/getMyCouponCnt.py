#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0284.获取优惠劵列表张数
http://127.0.0.1:8280/mallws/coupon/getMyCouponCnt.json
{
	"token":"123",
    "companyId": "campany0101",                                // 企业Id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                        // 0-成功 1-失败
		"unUsedCnt":"20",                                     // 未使用张数
		"usedCnt":"10",                                       // 已使用张数
	    "expireCnt":"5"                                       // 已过期张数
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.coupon.GetMyCouponCntResponse"
    }
}
"""
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData


class getMyCouponCnt(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    #获取优惠券列表张数
    def test_getMyCouponCnt_All(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        getMyCouponCntRst = ws.getMyCouponCnt(companyId=self.UserShop.companyId)
        RstDBunUsedCnt = select('select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person = ? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',self.UserShop.companyId,'01')
        RstDBsedCnt = select(
            'select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person=? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',
            self.UserShop.companyId,'02')
        RstDBexpireCnt = select(
            'select * from dlpromotionx.dl_promotionx_coupon_issue_record inner join dlpromotionx.dl_promotionx_coupon_snapshot on dlpromotionx.dl_promotionx_coupon_issue_record.coupon_entity_id = dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_id and dlpromotionx.dl_promotionx_coupon_issue_record.issue_person=? and dlpromotionx.dl_promotionx_coupon_snapshot.coupon_entity_status= ? ',
            self.UserShop.companyId,'04')
        self.assertEquals(getMyCouponCntRst.code, 200)
        self.assertEquals(getMyCouponCntRst.model['success'], '0')
        self.assertEquals(getMyCouponCntRst.model['unUsedCnt'],str(len(RstDBunUsedCnt)))
        self.assertEquals(getMyCouponCntRst.model['usedCnt'], str(len(RstDBsedCnt)))
        self.assertEquals(getMyCouponCntRst.model['expireCnt'], str(len(RstDBexpireCnt)))
    #获取不存在的用户优惠券列表(Bug:#6019)
    def test_getMyCouponCnt_NullUser(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        getMyCouponCntRst = ws.getMyCouponCnt(companyId='123456789')
        self.assertEquals(getMyCouponCntRst.code, 200)
        self.assertEquals(getMyCouponCntRst.model['success'], '0')
    #获取其他账户的优惠券列表
    def test_getMyCouponCnt_OtherUser(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        getMyCouponCntRst = ws.getMyCouponCnt(companyId=self.UserShop2.companyId)
        self.assertEquals(getMyCouponCntRst.code, 200)
        self.assertEquals(getMyCouponCntRst.model['success'], '0')
        self.assertEquals(getMyCouponCntRst.model['usedCnt'], '0')
        self.assertEquals(getMyCouponCntRst.model['expireCnt'], '0')
def suite():
    suite = unittest.TestSuite()
    suite.addTest(getMyCouponCnt('test_getMyCouponCnt_All'))
    suite.addTest(getMyCouponCnt('test_getMyCouponCnt_NullUser'))
    suite.addTest(getMyCouponCnt('test_getMyCouponCnt_OtherUser'))
    return suite
