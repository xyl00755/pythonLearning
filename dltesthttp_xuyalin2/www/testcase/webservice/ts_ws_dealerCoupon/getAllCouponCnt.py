#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import wsData

"""
WQ08.我的丹露页获取丹露红包、经销商红包、经销商优惠券数量
http://127.0.0.1:8280/mallws/dealerCoupon/getAllCouponCnt.json
{
	"token":"123"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                          // 0-成功 1-失败
		"danluCouponCnt":"20",                                  // 丹露红包张数
		"dealerCouponCnt":"10",                                 // 经销商红包张数
	    "dealerBenefitCnt":"5"                                  // 经销商优惠券张数
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.GetAllCouponCntResponse"
    }
}
"""
class getAllCouponCnt(unittest.TestCase):
    UserShop=wsData('TmlShop')

    #正确获取丹露页红包及优惠券数量
    def test_getAllCouponCnt(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getAllCouponCnt()
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertNotEqual(getCoupon.model['danluCouponCnt'],'')
        self.assertNotEqual(getCoupon.model['dealerCouponCnt'],'')
        self.assertNotEqual(getCoupon.model['dealerBenefitCnt'],'')

    #token为空
    def test_getAllCouponCnt_noToken(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getAllCouponCnt(token='null')
        self.assertEqual(getCoupon.code,600)

    #不存在的token
    def test_getAllCouponCnt_noExistToken(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getAllCouponCnt(token='1234567890')
        self.assertEqual(getCoupon.code,100)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getAllCouponCnt("test_getAllCouponCnt"))
    suite.addTest(getAllCouponCnt("test_getAllCouponCnt_noToken"))
    suite.addTest(getAllCouponCnt("test_getAllCouponCnt_noExistToken"))
    return suite