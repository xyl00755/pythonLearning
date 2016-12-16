#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/deliveryAddress/deliveryAddressUpdate.html

post
require: form
addressId:a0d29b5ad6444521b8b9b5f6f5da7a97
addressDetail:丹露道
zipcode:
deliveryPerson:wgh
deliveryMobile:13111111111
deliveryTel:
isDefault:0
areaCode:CHNP035C345D2998

response: json string

  {
     "resultView" : "",
     "success" : "GO_INTO_EFFECT"
 }

"""


class deliveryAddressUpdate(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserDeliveryAddressinfo = eData('DeliveryAddress')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?',
               self.UserDeliveryAddressinfo.company_id)

    def deliveryAddressInsert(self):
        self.dlservice.deliveryAddressInsert(self.s, self.UserDeliveryAddressinfo.addressDetail,
                                             self.UserDeliveryAddressinfo.zipcode,
                                             self.UserDeliveryAddressinfo.deliveryPerson,
                                             self.UserDeliveryAddressinfo.deliveryMobile,
                                             self.UserDeliveryAddressinfo.deliveryTel,
                                             self.UserDeliveryAddressinfo.isDefault,
                                             self.UserDeliveryAddressinfo.areaCode
                                             )

    def deliveryAddressUpdate(self, addressId='a0d29b5ad64445', areaCode=UserDeliveryAddressinfo.areaCode,
                              deliveryPerson=UserDeliveryAddressinfo.deliveryPerson):
        updateaddress = self.dlservice.deliveryAddressUpdate(self.s, addressId, self.UserDeliveryAddressinfo.addressDetail,
                                                             self.UserDeliveryAddressinfo.zipcode,
                                                             deliveryPerson,
                                                             self.UserDeliveryAddressinfo.deliveryMobile,
                                                             self.UserDeliveryAddressinfo.deliveryTel,
                                                             self.UserDeliveryAddressinfo.isDefault,
                                                             areaCode)
        return updateaddress

    def tearDown(self):
        update('delete from dlpromotionx.dl_dealer_coupon_activity where company_id = ?',
               self.UserDeliveryAddressinfo.company_id)

    # 修改成功及时生效
    def test_deliveryAddressUpdate_updateSuccess(self):
        self.deliveryAddressInsert()
        addresslist = self.dlservice.getAddressList(self.s)
        addressId = addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['addressId']
        updateaddress = self.deliveryAddressUpdate(addressId, self.UserDeliveryAddressinfo.areaCode, 'abc')
        self.assertEqual(updateaddress['success'], 'GO_INTO_EFFECT')

    # 修改成功等待审核

    def test_deliveryAddressUpdate_approve(self):
        self.deliveryAddressInsert()
        addresslist = self.dlservice.getAddressList(self.s)
        addressId = addresslist['deliveryAddressWrappers'][0]['deliveryAddressDto']['addressId']
        updateaddress = self.deliveryAddressUpdate(addressId, 'CHNP016C152D1425', self.UserDeliveryAddressinfo.deliveryPerson)
        self.assertEqual(updateaddress['success'], 'WAIT_4_EXAM')
        self.assertEqual(updateaddress['hasModifyDeliveryAddressApplying'], True)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?', self.UserDeliveryAddressinfo.company_id)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(deliveryAddressUpdate("test_deliveryAddressUpdate_updateSuccess"))
    suite.addTest(deliveryAddressUpdate("test_deliveryAddressUpdate_approve"))
    return suite
