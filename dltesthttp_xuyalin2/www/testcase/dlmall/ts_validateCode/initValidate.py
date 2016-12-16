#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/vilidateCode/init.html

get

response: json string

{"phoneNo":"17608011804","couponAmt":5}

"""

class initValidate(unittest.TestCase):
    UserShop = wsData('TmlShop')
    validateCodeInfo=eData('validateCode')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)


    #返回值一致
    def test_initValidate(self):
        initvalidate=self.dlservice.initValidate(self.s)
        self.assertEqual(initvalidate['phoneNo'],self.validateCodeInfo.phoneNo)
        self.assertEqual(initvalidate['couponAmt'],int(self.validateCodeInfo.coupon_amount))



def suite():
    suite=unittest.TestSuite()
    suite.addTest(initValidate("test_initValidate"))
    return suite
