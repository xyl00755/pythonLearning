#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import *

"""
0214.收货地址列表
http://127.0.0.1:8880/mallws/mydl/deliverAddress/getDeliverAddressList.json
{
    "token":"19ff0bb9e96846979163df1bd02ccf53"                        // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                               // 成功 0-成功
        "deliverAddressModelList": [                                  // 收货地址列表
            {
                "addressId": "1aefb9a18c5a4f0089b67903c5d5bd2a",        // 收货地址id
                "customerId": "76fc5f07fcef421a9cd4b9cb17ca1f27",       // 用户id
                "areaProvinceCode": "P014",                             // 省id
                "areaProvinceName": "辽宁",                             // 省名
                "areaCityCode": "C124",                                 // 市id
                "areaCityName": "大连",                                 // 市名
                "areaDistrictCode": "D1179",                            // 区id
                "areaDistrictName": "高新区",                           // 区名
                "addressDetail": "dd",                                  // 详细地址
                "zipCode": "",                                          // 邮编
                "deliverPerson": "xt",                                  // 收货人
                "deliverMobile": "13390006677",                         // 联系电话
                "deliverTel": "",                                       // 固定电话
                "isDefault": "1"                                        // 是否默认 0-默认 1-非默认
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.deliveraddr.DeliverAddressListReponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class getDeliverAddressList(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')


    # S1.有收货地址时获取收货地址列表
    def test_getDeliverAddressList(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getDeliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(getDeliverAddressList.model['success'],'0')
        self.assertGetDeliverAddressSuccess(deliverAddressList=getDeliverAddressList)

    # S2.无收货地址时获取收货地址列表
    def test_getDeliverAddress_null(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getDeliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(getDeliverAddressList.model['success'],'0')
        self.assertEqual(getDeliverAddressList.model['deliverAddressModelList'],[])

    # S3.无token时，获取收货地址列表
    def test_getDeliverAddress_noToken(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getDeliverAddressList=ws.getDeliverAddressList(token='null')
        self.assertEqual(getDeliverAddressList.model,None)
        self.assertEqual(getDeliverAddressList.code,600)

    # S4.token错误，获取收货地址列表
    def test_getDeliverAddress_tokenError(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getDeliverAddressList=ws.getDeliverAddressList(token='123456789')
        self.assertEqual(getDeliverAddressList.model,None)
        self.assertEqual(getDeliverAddressList.code,100)


    # 验证获取收货地址列表正确
    def assertGetDeliverAddressSuccess(self,deliverAddressList=None):
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['addressId'],self.UserShop1.addressId)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['areaProvinceCode'],self.UserShop1.areaProvinceCode)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['areaCityCode'],self.UserShop1.areaCityCode)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['areaDistrictCode'],self.UserShop1.areaDistrictCode)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['addressDetail'],self.UserShop1.deliverAddress)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['zipCode'],self.UserShop1.zipCode)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['deliverPerson'],self.UserShop1.deliverPerson)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['deliverTel'],self.UserShop1.deliverTel)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['deliverMobile'],self.UserShop1.deliverMobile)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['isDefault'],self.UserShop1.isDefault)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(getDeliverAddressList("test_getDeliverAddressList"))
    suite.addTest(getDeliverAddressList("test_getDeliverAddress_null"))
    suite.addTest(getDeliverAddressList("test_getDeliverAddress_noToken"))
    suite.addTest(getDeliverAddressList("test_getDeliverAddress_tokenError"))
    return suite