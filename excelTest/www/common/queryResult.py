#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append(sys.path[0])

import unittest

class queryResult(unittest.TestCase):
    data={
            "status": 0,
            "msg":"",
            "data": {
                "result":[
                    {
                        "payerId" : "e0b68579f6904f059eb43743f50a5834",
                        "payerName" : "testzwq的终端店",
                        "sellerId" : "60984ad4c5844cf9b46eb86d551e323b",
                        "sellerName" : "testyuxi冒烟测试经销商",
                        "payNo" : "80609596710933",
                        "orderNo" : "20609596710932",
                        "orderStatus" : "C020",
                        "couponId" : "2433414104",
                        "couponEntityId" : "11243431100003",
                        "couponTypeId" : "01",
                        "couponName" : "zwq测试",
                        "promotionId" : "06112463897504",
                        "promotionName" : "测试推送卷831",
                        "promotionTypeId" : "06",
                        "couponAmt" : 1000000,
                        "discountAmt" : 44400,
                        "couponReceiveTime" : "2016-08-31 09:31:51",
                        "couponUseTime" : "2016-09-01 16:34:31",
                        "orderCreateTime" : "2016-09-01 16:34:31",
                        "orderConfirmTime" : "2016-09-01 16:34:31",
                        "logicDeleteFlg" : "0",
                        "couponUseFlg" : "1",
                        "payerAreaName" : "东海省-钓鱼岛-赤尾屿",
                        "sellerAreaName" : "东海省-钓鱼岛-赤尾屿"
                    },{
                        "payerId" : "e0b68579f6904f059eb43743f50a5834",
                        "payerName" : "testzwq的终端店",
                        "sellerId" : "e4d1e52da6a048449072a2a0cded29e7",
                        "sellerName" : "东海省茅台代理经销商",
                        "payNo" : "80609594140931",
                        "orderNo" : "20609594140930",
                        "orderStatus" : "C020",
                        "couponId" : "2433414104",
                        "couponEntityId" : "11243431100002",
                        "couponTypeId" : "01",
                        "couponName" : "zwq测试",
                        "promotionId" : "06112463897504",
                        "promotionName" : "测试推送卷831",
                        "promotionTypeId" : "06",
                        "couponAmt" : 1000000,
                        "discountAmt" : 200000,
                        "couponReceiveTime" : "2016-08-31 09:31:51",
                        "couponUseTime" : "2016-09-01 16:30:14",
                        "orderCreateTime" : "2016-09-01 16:30:14",
                        "orderConfirmTime" : "",
                        "logicDeleteFlg" : "0",
                        "couponUseFlg" : "1",
                        "payerAreaName" : "东海省-钓鱼岛-赤尾屿",
                        "sellerAreaName" : "东海省-钓鱼岛-赤尾屿"
                }],
                "total":100,
                "pageIndex":1,
                "pageSize":10
            }
        }

    def assertInTest(self):
        self.assertIn(self.data['data']['result'][0]['couponName'], 'wq测')


def suite():
     suite=unittest.TestSuite()
     suite.addTest(queryResult("assertInTest"))
     return suite


if __name__ == '__main__':
    #create_engine()
    runner = unittest.TextTestRunner()
    runner.run(queryResult.suite())
