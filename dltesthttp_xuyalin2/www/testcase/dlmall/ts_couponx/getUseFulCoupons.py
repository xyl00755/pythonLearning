#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/couponx/getUseFulCoupons.html

request:
get
http://123.57.244.205:9003/couponx/getUseFulCoupons.html?goodsId=f4bccbbd84e44f9ba839e082970dccca%2C9c02bcf9737d499a8a72a3514730b425%2C24df3ab5b628496aa0fdded6c4230fec%2C2e78061ea75b26638ef38d1b0c848cbb%2Cbc54482ad9a44f3d95b63d9876bc3100%2C&t=1474440394741
response:json string
{
    "status": 0,
    "data": {
        "unUseFulCoupons": [
            {
                "id": null,
                "couponEntityId": "114512879800028",
                "couponName": "6元优惠券验证",
                "couponAmt": 600,
                "couponEntityStatus": "01",
                "effectiveTime": "2016-09-21",
                "uneffectiveTime": "2016-10-21",
                "category": "白酒",
                "expireTime": null,
                "useTime": null,
                "records": null
            }
        ],
        "useFulCoupons": [
            {
                "id": null,
                "couponEntityId": "114512879800028",
                "couponName": "6元优惠券验证",
                "couponAmt": 600,
                "couponEntityStatus": "01",
                "effectiveTime": "2016-09-21",
                "uneffectiveTime": "2016-10-21",
                "category": "白酒",
                "expireTime": null,
                "useTime": null,
                "records": null
            }
        ]
    },
    "msg": ""
}
"""

class getUseFulCoupons(unittest.TestCase):
    UserShop = eData('WebManager')
    danluCouponsInfo=eData('DanluCoupons')
    dlservice = dlmall()
    s = dlservice.login(UserShop.buyer_username,UserShop.buyer_password)

    #四种红包1 过期时间最长  2 两个过期时间一样但是一个金额大一个金额小 3 过期时间最短 检查返回值排序
    def test_Coupons_sort(self):
        data =[self.danluConponsInfo.goodsId1,self.danluConponsInfo.goodsId2,self.danluConponsInfo.goodsId3,self.danluConponsInfo.goodsId4]
        a =','
        a.join(data)
        couponlist= self.dlservice.getUseFulCoupons(s,data)
        self.assertEqual(couponlist['data']['UseFulCoupons'][0]['couponEntityId'],self.danluCouponsInfo.couponEntityId4)
        self.assertEqual(couponlist['data']['UseFulCoupons'][1]['couponEntityId'],self.danluCouponsInfo.couponEntityId3)
        self.assertEqual(couponlist['data']['UseFulCoupons'][2]['couponEntityId'],self.danluCouponsInfo.couponEntityId2)
        self.assertEqual(couponlist['data']['UseFulCoupons'][3]['couponEntityId'],self.danluCouponsInfo.couponEntityId1)





