#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import wsData

"""

WQ07.获取经销商红包相关参数
http://127.0.0.1:8280/mallws/common/param/getDealerCouponParam.json
{
   	"token":"123",
	"dealerIdList":["123","321"]								// 必须 经销商ID(列表)
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
		"paramList":[{
		"dealerId":"",											// 经销商ID
		"dealerPayRatio": 3000									// 经销商红包最高支付比(New)(int类型)
		},{
		"dealerId":"",
		"dealerPayRatio": 4000
		}
		]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.GetDealerCouponParamResponse"
    }
}
参数说明：
	经销商最高支付比(dealerPayRatio)为整数类型，支付比对应的百分百计算公式：百分比 = 支付比 / 10000 如：30% = 3000 / 10000;

"""

class getDealerCouponParam(unittest.TestCase):
    UserShop=wsData('DealMager')
    Param=wsData('Param')

    #正确获取经销商红包参数设置
    def test_getDealerCouponParam(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getParam=ws.getDealerCouponParam(dealerIdList=[self.UserShop.companyId])
        self.assertEqual(getParam.model['success'],'0')
        self.assertEqual(str(getParam.model['paramList'][0]['dealerPayRatio']),self.Param.dealerPayRatio)

    #dealerId为空
    def test_getDealerCouponParam_null(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getParam=ws.getDealerCouponParam(dealerIdList=[''])
        self.assertEqual(getParam.model['success'],'0')
        self.assertEqual(getParam.model['paramList'],[])

    #dealerId不存在
    def test_getDealerCouponParam_error(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getParam=ws.getDealerCouponParam(dealerIdList=['1234567890'])
        self.assertEqual(getParam.model['success'],'0')
        self.assertEqual(getParam.model['paramList'][0]['dealerPayRatio'],3000)
        self.assertEqual(getParam.model['paramList'][0]['dealerId'],'1234567890')

    #token为空
    def test_getDealerCouponParam_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getParam=ws.getDealerCouponParam(dealerIdList=[self.UserShop.companyId],token='null')
        self.assertEqual(getParam.code,600)

    #token不存在
    def test_getDealerCouponParam_tokenErrorl(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getParam=ws.getDealerCouponParam(dealerIdList=[self.UserShop.companyId],token='1234567890')
        self.assertEqual(getParam.code,100)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getDealerCouponParam("test_getDealerCouponParam"))
    suite.addTest(getDealerCouponParam("test_getDealerCouponParam_null"))
    suite.addTest(getDealerCouponParam("test_getDealerCouponParam_error"))
    suite.addTest(getDealerCouponParam("test_getDealerCouponParam_tokenNull"))
    suite.addTest(getDealerCouponParam("test_getDealerCouponParam_tokenErrorl"))
    return suite
