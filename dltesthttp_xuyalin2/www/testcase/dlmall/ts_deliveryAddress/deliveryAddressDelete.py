#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/deliveryAddress/deliveryAddressDelete.html

post
require: form
addressId:6cfc8e130d8e4f60a01a23c821d852f5

response: json string

 {
     "applyingDeliveryAddress" : "false",
     "viewResult" : ""
 }

"""


class deliveryAddressDelete(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserDeliveryAddressinfo = eData('DeliveryAddress')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?',self.UserDeliveryAddressinfo.company_id)

    def deliveryAddressInsert(self, areaCode=UserDeliveryAddressinfo.areaCode,
                              deliveryPerson=UserDeliveryAddressinfo.deliveryPerson):
        deliveryaddress = self.dlservice.deliveryAddressInsert(self.s, self.UserDeliveryAddressinfo.addressDetail,
                                                          self.UserDeliveryAddressinfo.zipcode,
                                                          deliveryPerson,
                                                          self.UserDeliveryAddressinfo.deliveryMobile,
                                                          self.UserDeliveryAddressinfo.deliveryTel,
                                                          self.UserDeliveryAddressinfo.isDefault,
                                                          areaCode)
        return deliveryaddress

    def deliveryAddressUpdate(self, areaCode=UserDeliveryAddressinfo.areaCode,
                              deliveryPerson=UserDeliveryAddressinfo.deliveryPerson):
        addresslist = self.dlservice.getAddressList(self.s)
        addressId = addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['addressId']
        updateaddress = self.dlservice.deliveryAddressUpdate(self.s, addressId, self.UserDeliveryAddressinfo.addressDetail,
                                                        self.UserDeliveryAddressinfo.zipcode,
                                                        deliveryPerson,
                                                        self.UserDeliveryAddressinfo.deliveryMobile,
                                                        self.UserDeliveryAddressinfo.deliveryTel,
                                                        self.UserDeliveryAddressinfo.isDefault,
                                                        areaCode)
        return updateaddress

    # 地区被改变后无法删除成功
    def test_deliveryAddressDelte_faild(self):
        self.deliveryAddressInsert()
        self.deliveryAddressUpdate('CHNP016C152D1425', self.UserDeliveryAddressinfo.deliveryPerson)
        addresslist = self.dlservice.getAddressList(self.s)
        addressdelete = self.dlservice.deliveryAddressDelete(self.s,
                                                        addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto'][
                                                            'addressId'])
        self.assertEqual(addressdelete['applyingDeliveryAddress'],True)

    # 删除成功
    def test_deliveryAddressDelete_sucess(self):
        self.deliveryAddressInsert()
        addresslist = self.dlservice.getAddressList(self.s)
        addressdelete = self.dlservice.deliveryAddressDelete(self.s,
                                                        addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto'][
                                                            'addressId'])
        self.assertEqual(addressdelete['applyingDeliveryAddress'], False)

    # 其他更改删除成功
    def test_deliveryAddressDelete_change(self):
        self.deliveryAddressInsert()
        self.deliveryAddressUpdate(self.UserDeliveryAddressinfo.areaCode, 'abc')
        addresslist = self.dlservice.getAddressList(self.s)
        addressdelete = self.dlservice.deliveryAddressDelete(self.s,
                                                        addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto'][
                                                            'addressId'])
        self.assertEqual(addressdelete['applyingDeliveryAddress'], False)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?', self.UserDeliveryAddressinfo.company_id)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(deliveryAddressDelete("test_deliveryAddressDelte_faild"))
    suite.addTest(deliveryAddressDelete("test_deliveryAddressDelete_sucess"))
    suite.addTest(deliveryAddressDelete("test_deliveryAddressDelete_change"))
    return suite
