#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import wsData

"""
WQ02.获取我的经销商优惠劵/红包 数量
http://127.0.0.1:8280/mallws/dealerCoupon/getCouponCnt.json
{
	"token":"123",
	"dealerCouponType":"1"										 // 必须 类型 11-经销商优惠券 10-经销商红包
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                           // 0-成功 1-失败
		"unUsedCnt":"20",                                        // 未使用张数
		"usedCnt":"10",                                          // 已使用张数
	    "expireCnt":"5"                                          // 已过期张数
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.GetCouponCntResponse"
    }
}
"""

class getCouponCnt(unittest.TestCase):
    UserShop=wsData('TmlShop')

    #正确获取我的经销商优惠券数量
    def test_getCouponCnt11(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCnt(dealerCouponType='11')
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertNotEqual(getCoupon.model['unUsedCnt'],'')
        self.assertNotEqual(getCoupon.model['usedCnt'],'')
        self.assertNotEqual(getCoupon.model['expireCnt'],'')

    #正确获取我的经销商红包数量
    def test_getCouponCnt10(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCnt(dealerCouponType='10')
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertNotEqual(getCoupon.model['unUsedCnt'],'')
        self.assertNotEqual(getCoupon.model['usedCnt'],'')
        self.assertNotEqual(getCoupon.model['expireCnt'],'')

    #dealerCouponType为空
    def test_getCouponCnt_couponTypeNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCnt(dealerCouponType='')
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['unUsedCnt'],'0')
        self.assertEqual(getCoupon.model['usedCnt'],'0')
        self.assertEqual(getCoupon.model['expireCnt'],'0')

    #dealerCouponType不存在
    def test_getCouponCnt_couponTypeError(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCnt(dealerCouponType='123')
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['unUsedCnt'],'0')
        self.assertEqual(getCoupon.model['usedCnt'],'0')
        self.assertEqual(getCoupon.model['expireCnt'],'0')

    #token为空
    def test_getCouponCnt_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCnt(dealerCouponType='10',token='null')
        self.assertEqual(getCoupon.code,600)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCouponCnt("test_getCouponCnt11"))
    suite.addTest(getCouponCnt("test_getCouponCnt10"))
    suite.addTest(getCouponCnt("test_getCouponCnt_couponTypeNull"))
    suite.addTest(getCouponCnt("test_getCouponCnt_couponTypeError"))
    suite.addTest(getCouponCnt("test_getCouponCnt_tokenNull"))
    return suite