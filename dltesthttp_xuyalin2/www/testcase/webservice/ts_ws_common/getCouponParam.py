#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
0281.获取平台参数
http://127.0.0.1:8280/mallws/common/param/getCouponParam.json
{
   	"token":"123"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
		"payRatio": "0.5",               //最高支付比
		"maxTicketUseNum": "3"           //优惠劵最大使用张数
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.GetCouponParamResponse"
    }
}
"""

import unittest

from www.api.webservice import *
from www.common.excel import wsData


class getCouponParam(unittest.TestCase):

    UserShop = wsData('TmlShop')
    Param = wsData('Param')

    # S1.获取平台参数
    def test_getCouponParam_get(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        couponParam = ws.getCouponParam()
        self.assertEqual(couponParam.model['success'], '0')
        self.assertEqual(couponParam.model['payRatio'],self.Param.payRatio)
        self.assertEqual(couponParam.model['maxTicketUseNum'],self.Param.maxTicketUseNum)

    # S2.不带token获取平台参数——错误 #5429 已解决
    def test_getCouponParam_noToken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        couponParam = ws.getCouponParam(token='null')
        self.assertEqual(couponParam.code, 600)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCouponParam("test_getCouponParam_get"))
    suite.addTest(getCouponParam("test_getCouponParam_noToken"))
    return suite