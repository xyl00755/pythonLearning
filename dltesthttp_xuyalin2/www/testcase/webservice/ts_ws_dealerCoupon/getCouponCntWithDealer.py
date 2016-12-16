#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import wsData

"""
WQ04.提交订单页获取经销商可使用红包数量
http://127.0.0.1:8280/mallws/dealerCoupon/getCouponCntWithDealer.json
{
	"token":"123",
										    // 必须 经销商ID列表
	"dealerParam":[
		{
			"dealerId":"123",				// 必须 经销商ID
			"totalAmt":"15000"				// 必须 订单中该经销商下所有商品总额(扣除满减满赠后) 单位：分
		},
		{
			"dealerId":"123",
			"totalAmt":"15000"
		}
	]
}

{
	"code": 200,
    "description": "执行成功!",
	"model": {
        "success": "0",                         // 0-成功 1-失败
		"unUsedCntList":[{
		 "dealerId":"123",
		 "unUsedCnt":"2"
		}]                                      // 可用红包数量
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.GetCouponCntWithDealerResponse"
    }

}
"""

class getCouponCntWithDealer(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop1=wsData('DealMager')
    UserShop2=wsData('DealMager2')

    #正确获取经销商可使用红包数量
    def test_getCouponCntWithDealerOne(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCntWithDealer(dealerId=[self.UserShop1.companyId],totalAmt=['15000'])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertNotEqual(getCoupon.model['unUsedCntList'][0]['unUsedCnt'],'')

    #正确获取两个经销商可使用红包数量
    def test_getCouponCntWithDealerTwo(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCntWithDealer(dealerId=[self.UserShop1.companyId,self.UserShop2.companyId],totalAmt=['15000','15000'])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertNotEqual(getCoupon.model['unUsedCntList'][0]['unUsedCnt'],'')
        self.assertNotEqual(getCoupon.model['unUsedCntList'][1]['unUsedCnt'],'')

    #获取不存在的经销商可使用红包数量
    def test_getCouponCntWithDealer_error(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCntWithDealer(dealerId=['1234567890'],totalAmt=['15000'])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['unUsedCntList'][0]['unUsedCnt'],'0')

    #经销商id为空
    def test_getCouponCntWithDealer_null(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getCouponCntWithDealer(dealerId=[''],totalAmt=['15000'])
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['unUsedCntList'],None)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCouponCntWithDealer("test_getCouponCntWithDealerOne"))
    suite.addTest(getCouponCntWithDealer("test_getCouponCntWithDealerTwo"))
    suite.addTest(getCouponCntWithDealer("test_getCouponCntWithDealer_error"))
    suite.addTest(getCouponCntWithDealer("test_getCouponCntWithDealer_null"))
    return suite