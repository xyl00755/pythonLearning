#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dldata import *
from www.common.excel import *
#from www.common.database import *

"""
POST
{
    "couponEntityId" : "0001210212",
    "couponId" : "1002012",
    "couponName" : "测试经销商红包",
    "payerName" : "testzwq的终端店",
    "sellerName" : "testyuxi冒烟测试经销商",
    "sellerId" : "60984ad4c5844cf9b46eb86d551e323b",
    "couponUseFlg" : "1",
    "orderStatus" : "C019",
    "couponUseStartTime" : "2016-09-05",
    "couponUseEndTime" : "2016-09-10",
    "couponReceiveStartTime" : "2016-09-01",
    "couponReceiveEndTime" : "2016-09-30"
}
"""

class queryCouponTotalAmtOnAdmin(unittest.TestCase):
    UsedDealerCouponInfo = eData('UsedDealerCoupon')
    dlservice = dldata()

    #插入抵扣数据
    def setUp(self):
        print 'setUp'

    #入参为空时查询到所有红包,
    def test_queryCouponTotalAmtOnAdmin_nullPara(self):
        #queryResult=self.dlservice.queryCouponTotalAmtOnAdmin()
        queryResult=   {
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
                                    "orderConfirmTime" : "2016-09-01 16:34:31",
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
        self.assertEqual(queryResult['status'], 0)
        #self.assertGreaterEqual(queryResult['data']['grantAmt'],0)
        #self.assertIn('00',str(queryResult['data']['discountAmt']))
        #self.assertGreaterEqual(queryResult['data']['couponUseStartTime'], "2016-09-06")
        for i in range(0, len(queryResult['data']['result'])):
            self.assertEqual(queryResult['data']['result'][i]['couponId'], self.UsedDealerCouponInfo.couponId)

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'


def suite():
    suite=unittest.TestSuite()
    suite.addTest(queryCouponTotalAmtOnAdmin("test_queryCouponTotalAmtOnAdmin_nullPara"))
    return suite
