#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/deliveryAddress/deliveryAddressInsert.html

post
require: form

addressDetail:反正就是丹露啦
zipcode:
deliveryPerson:wgh
deliveryMobile:13111111111
deliveryTel:
isDefault:0
areaCode:CHNP035C345D2998


response: json string

{"result":true}

"""


class deliveryAddressInsert(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserDeliveryAddressinfo = eData('DeliveryAddress')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?', self.UserDeliveryAddressinfo.company_id)

    def deliveryaddressInsert(self,isDefault=UserDeliveryAddressinfo.isDefault,deliveryPerson=UserDeliveryAddressinfo.deliveryPerson):
        deliveryaddress = self.dlservice.deliveryAddressInsert(self.s, self.UserDeliveryAddressinfo.addressDetail,
                                                          self.UserDeliveryAddressinfo.zipcode,
                                                          deliveryPerson,
                                                          self.UserDeliveryAddressinfo.deliveryMobile,
                                                          self.UserDeliveryAddressinfo.deliveryTel,
                                                          isDefault,
                                                          self.UserDeliveryAddressinfo.areaCode)
        return deliveryaddress

    # 正常插入所有需要填入的内容，设为默认地址
    def test_deliveryAddressInsert(self):
        deliveryaddress = self.deliveryaddressInsert()
        self.assertEqual(deliveryaddress['result'], True)

    # 插入同样的地址，设为默认地址
    def test_deliveryAddressInsert_same(self):
        for i in range(2):
            deliveryaddress = self.deliveryaddressInsert()
        self.assertEqual(deliveryaddress['result'], True)

    # 插入同样的地址，非默认
    def test_deliveryAddressInsert_notdefault(self):
        deliveryaddress = self.deliveryaddressInsert('0',self.UserDeliveryAddressinfo.deliveryPerson)
        self.assertEqual(deliveryaddress['result'], True)


    # 必填项(收货人、所在地区、街道地址、联系手机）收货人为空
    def test_deliveryAddressInsert_nullName(self):
        deliveryaddress= self.deliveryaddressInsert(self.UserDeliveryAddressinfo.isDefault,None)
        self.assertEqual(deliveryaddress['result'], False)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?', self.UserDeliveryAddressinfo.company_id)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(deliveryAddressInsert("test_deliveryAddressInsert"))
    suite.addTest(deliveryAddressInsert("test_deliveryAddressInsert_same"))
    suite.addTest(deliveryAddressInsert("test_deliveryAddressInsert_notdefault"))
    suite.addTest(deliveryAddressInsert("test_deliveryAddressInsert_nullName"))
    return suite
