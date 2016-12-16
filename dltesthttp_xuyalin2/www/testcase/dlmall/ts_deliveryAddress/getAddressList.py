#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/deliveryAddress/getAddressList.html

post
require:

response: json string
{
    "deliveryAddressWrappers": [
        {
            "deliveryAddressDto": {
                "addressId": "a0d29b5ad6444521b8b9b5f6f5da7a97",
                "companyId": "618c5c025cec4893bf3d711ad6635251",
                "areaCode": "CHNP035C345D2998",
                "addressDetail": "丹露县",
                "zipcode": "123456",
                "deliveryPerson": "wgh",
                "deliveryMobile": "13856789101",
                "deliveryTel": "",
                "isDefault": "1",
                "applyId": null,
                "createdTimestamp": 1464915551000,
                "createdPerson": "wangguohao",
                "updatedTimestamp": 1464915551000,
                "updatedPerson": "wangguohao"
            },
            "name": "东海省 -钓鱼岛 -赤尾屿",
            "provinceCode": "CHNP035",
            "cityCode": "CHNP035C345",
            "districtCode": "CHNP035C345D2998"
        }
    ]
"""


class getAddressList(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserDeliveryAddressinfo = eData('DeliveryAddress')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?',
               self.UserDeliveryAddressinfo.company_id)

    def getAddressList(self):
        for i in range(3):
            self.dlservice.deliveryAddressInsert(self.s, self.UserDeliveryAddressinfo.addressDetail,
                                        self.UserDeliveryAddressinfo.zipcode,
                                        self.UserDeliveryAddressinfo.deliveryPerson,
                                        self.UserDeliveryAddressinfo.deliveryMobile,
                                        self.UserDeliveryAddressinfo.deliveryTel,
                                        self.UserDeliveryAddressinfo.isDefault,
                                        self.UserDeliveryAddressinfo.areaCode)
        addresslist= self.dlservice.getAddressList(self.s)
        return addresslist


    # 插入三个地址，判断长度
    def test_getAddressList_len(self):
        addresslist= self.getAddressList()
        self.assertEqual(len(addresslist['deliveryAddressWrappers']),3)

    #判断返回值的名字和填入的是否一致
    def test_getAddressList_name(self):
        addresslist= self.getAddressList()
        self.assertEqual(addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['deliveryPerson'].encode('utf-8'),u'刘亿莎'.encode('utf-8'))

    #判断所有列表是否只有一个默认地址
    def test_getAddressList_defautaddress(self):
        addresslist= self.getAddressList()
        count = 0
        for i in range(3):
            if ('1' ==addresslist['deliveryAddressWrappers'][i]['deliveryAddressDto']['isDefault']):
                count+=1
        self.assertEqual(count,1)

    # 删除一个地址，判断长度
    def test_getAddressList_delete_len(self):
        addresslist= self.getAddressList()
        self.dlservice.deliveryAddressDelete(self.s,addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['addressId'])
        addresslist = self.dlservice.getAddressList(self.s)
        self.assertEqual(len(addresslist['deliveryAddressWrappers']), 2)


    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?',
               self.UserDeliveryAddressinfo.company_id)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getAddressList("test_getAddressList_len"))
    suite.addTest(getAddressList("test_getAddressList_name"))
    suite.addTest(getAddressList("test_getAddressList_defautaddress"))
    suite.addTest(getAddressList("test_getAddressList_delete_len"))
    return suite
