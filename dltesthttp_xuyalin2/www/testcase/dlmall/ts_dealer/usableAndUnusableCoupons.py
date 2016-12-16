#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/dealer/usableAndUnusableCoupons.html

post
require: json string
[
    {
        "dealerId": "5482720f5503463aa930a3e373d3efd6",
        "goodsTotalAmt": "1000"
    }
]

response: json string

{
    "status": 0,
    "msg": "",
    "data": {
        "5482720f5503463aa930a3e373d3efd6": {
            "usableDealerCoupons": [
                {
                    "dealerCouponEntityId": "asa",
                    "dealerCouponEntityStatus": "01",
                    "dealerCouponId": "a123",
                    "dealerCouponName": "优惠券1",
                    "dealerCouponType": "10",
                    "dealerName": "河北人人大",
                    "dealerId": "abc",
                    "dealerCouponImgUrl": "http://www.baidu.com/img.jpg",
                    "dealerCouponAmount": 213,
                    "effectiveTime": "12321321212",
                    "uneffectiveTime": "12312312312",
                    "availableChannel": "S011,S012",
                    "goodsId": "1232",
                    "goodsName": "国窖1753 500mL",
                    "areaLimit": "code1,code2",
                    "platformLimit": "WEB",
                    "effectiveAmount": 154,
                    "orderNo": "bcd",
                    "activityId": "abc",
                    "goodsFlag": true,
                    "effectivityStatus": "01"
                }
            ],
            "unUsableDealerCoupons": [
                {
                    "dealerCouponEntityId": "asa",
                    "dealerCouponEntityStatus": "01",
                    "dealerCouponId": "a123",
                    "dealerCouponName": "优惠券1",
                    "dealerCouponType": "10",
                    "dealerName": "河北人人大",
                    "dealerId": "abc",
                    "dealerCouponImgUrl": "http://www.baidu.com/img.jpg",
                    "dealerCouponAmount": 213,
                    "effectiveTime": "12321321212",
                    "uneffectiveTime": "12312312312",
                    "availableChannel": "S011,S012",
                    "goodsId": "1232",
                    "goodsName": "国窖1753 500mL",
                    "areaLimit": "code1,code2",
                    "platformLimit": "WEB",
                    "effectiveAmount": 154,
                    "orderNo": "bcd",
                    "activityId": "abc",
                    "goodsFlag": true,
                    "effectivityStatus": "01"
                }
            ]
        }
    }
}

"""
class usableAndUnusableCoupons(unittest.TestCase):
    dealerCouponsInfo=eData('dealerCouponsInfo')
    dlservice = dlmall()

    def login(self,username,userpassword):
        s = self.dlservice.login(username,userpassword)
        return s

    #经销商没有发放红包，检查返回数组个数
    def test_noCoupon_dealer(self):
        s = self.longin(self.dealerCouponsInfo.username1,self.dealerCouponsInfo.password1)
        dealers=[
            {'dealerId':self.dealerCouponsInfo.dealerId1,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt1}
        ]
        getdealercoupons= self.dlservice.usableAndUnusableCoupons(s,dealers)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId1]['usableDealerCoupons']),0)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId1]['unUsableDealerCoupons']),0)

    #经销商发放三个红包，用户没有领用，检查返回数组个数
    def test_coupons_dealerNotUse(self):
        s = self.longin(self.dealerCouponsInfo.username2,self.dealerCouponsInfo.password2)
        dealers=[
            {'dealerId':self.dealerCouponsInfo.dealerId2,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt2}
        ]
        getdealercoupons= self.dlservice.usableAndUnusableCoupons(s,dealers)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId2]['usableDealerCoupons']),0)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId2]['unUsableDealerCoupons']),0)


    #经销商发放三个红包，用户领用了两个，检查返回数组个数
    def test_coupons_dealerUse(self):
        s = self.longin(self.dealerCouponsInfo.username3,self.dealerCouponsInfo.password3)
        dealers=[
            {'dealerId':self.dealerCouponsInfo.dealerId3,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt3}
        ]
        getdealercoupons= self.dlservice.usableAndUnusableCoupons(s,dealers)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId3]['usableDealerCoupons']),2)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId3]['unUsableDealerCoupons']),0)

    #用户购买了两个不同经销商的商品，一个经销商发放三个红包用户领用了两个，一个经销商没有发放红包，检查返回数组个数
    def test_coupons_twoDealers(self):
        s = self.longin(self.dealerCouponsInfo.username4,self.dealerCouponsInfo.password4)
        dealers=[
            {'dealerId':self.dealerCouponsInfo.dealerId4,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt4},
            {'dealerId':self.dealerCouponsInfo.dealerId5,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt5}
        ]
        getdealercoupons= self.dlservice.usableAndUnusableCoupons(s,dealers)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId5]['usableDealerCoupons']),2)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId4]['usableDealerCoupons']),0)

    #经销商发放了三个红包，用户领用了两个红包，两个红包都有效,检查所有红包已领取状态
    def test_coupons_usable(self):
        s = self.longin(self.dealerCouponsInfo.username3,self.dealerCouponsInfo.password3)
        dealers=[
            {'dealerId':self.dealerCouponsInfo.dealerId3,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt3}
        ]
        getdealercoupons= self.dlservice.usableAndUnusableCoupons(s,dealers)
        for i in range(2):
            self.assertEqual(getdealercoupons['data'][self.dealerCouponsInfo.dealerId6]['usableDealerCoupons'][i]['dealerCouponEntityStatus'],'01')

    #发了六个红包的经销商(一个红包有效五个红包无效，无效分别为1 超过使用金额限制 2 不同平台 3 没有到有效期开始时间 4 过了有效期结束时间 5 更改售卖权）
    def test_coupons_usableandunusablecoupons(self):
        s = self.longin(self.dealerCouponsInfo.username5,self.dealerCouponsInfo.password5)
        dealers=[
            {
            'dealerId':self.dealerCouponsInfo.dealerId6,
            'goodsTotalAmt':self.dealerCouponsInfo.goodsTotalAmt6
            }
        ]
        getdealercoupons= self.dlservice.usableAndUnusableCoupons(s,dealers)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId6]['usableDealerCoupons']),1)
        self.assertEqual(len(getdealercoupons['data'][self.dealerCouponsInfo.dealerId6]['unUsableDealerCoupons']),5)
















