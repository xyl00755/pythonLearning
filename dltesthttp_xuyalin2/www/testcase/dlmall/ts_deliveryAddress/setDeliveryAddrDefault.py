#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/deliveryAddress/setDeliveryAddrDefault.html

post
require: json string
{"addressId":"6cfc8e130d8e4f60a01a23c821d852f5"}

response: json string

  {
     "resultView" : "",
     "success" : "GO_INTO_EFFECT"
 }

"""
class setDeliveryAddrDefault(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserDeliveryAddressinfo = eData('DeliveryAddress')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?',
               self.UserDeliveryAddressinfo.company_id)

    def deliveryAddressInsert(self,isDefault=UserDeliveryAddressinfo.isDefault):
        self.dlservice.deliveryAddressInsert(self.s, self.UserDeliveryAddressinfo.addressDetail,
                                             self.UserDeliveryAddressinfo.zipcode,
                                             self.UserDeliveryAddressinfo.deliveryPerson,
                                             self.UserDeliveryAddressinfo.deliveryMobile,
                                             self.UserDeliveryAddressinfo.deliveryTel,
                                             isDefault,
                                             self.UserDeliveryAddressinfo.areaCode,)
    #已经是默认地址再设置为默认地址
    def test_setDeliveryAdrDefault(self):
        self.deliveryAddressInsert()
        addresslist= self.dlservice.getAddressList(self.s)
        deliveryaddressdefalut= self.dlservice.setDeliveryAddrDefault(self.s,addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['addressId'])
        self.assertEqual(deliveryaddressdefalut['status'],0)

    #把非默认地址设置为默认地址
    def test_setDeliveryAdrDefault_notdefault(self):
        self.deliveryAddressInsert(0)
        addresslist= self.dlservice.getAddressList(self.s)
        deliveryaddressdefalut= self.dlservice.setDeliveryAddrDefault(self.s,addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['addressId'])
        self.assertEqual(deliveryaddressdefalut['status'],0)

    #不存在的地址不能成功设置为默认地址
    def test_setDeliveryAdrDefault_setDefaultFail(self):
        self.deliveryAddressInsert()
        addresslist= self.dlservice.getAddressList(self.s)
        deliveryaddressdefalut= self.dlservice.setDeliveryAddrDefault(self.s,'a0d29b5ad64445')
        self.assertEqual(deliveryaddressdefalut['status'],1)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?', self.UserDeliveryAddressinfo.company_id)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(setDeliveryAddrDefault("test_setDeliveryAdrDefault"))
    suite.addTest(setDeliveryAddrDefault("test_setDeliveryAdrDefault_notdefault"))
    suite.addTest(setDeliveryAddrDefault("test_setDeliveryAdrDefault_setDefaultFail"))
    return suite