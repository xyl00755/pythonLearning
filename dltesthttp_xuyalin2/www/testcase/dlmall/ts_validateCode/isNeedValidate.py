#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/vilidateCode/isNeedValidate.html

post
require: data form
couponList:[{"couponId":"114512879800028","couponAmt":600,"couponUseAmt":600}]

response: json string

 {"flag":0}

"""

class isNeedValidate(unittest.TestCase):
    UserShop = wsData('TmlShop')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    # 多个红包需要验证
    def test_needValidate(self):
        needvalidate= self.dlservice.isNeedValidate(self.s,'123',40000,300,3)
        self.assertEqual(needvalidate['flag'],1)


    #多个红包不需要验证

    def test_noNeedValidate(self):
        needvalidate= self.dlservice.isNeedValidate(self.s,'123',400,300,2)
        self.assertEqual(needvalidate['flag'],0)

    #1个红包需要验证

    def test_needValidate_oneCoupou(self):
        needvalidate= self.dlservice.isNeedValidate(self.s,'123',100000,300,1)
        self.assertEqual(needvalidate['flag'],1)

    #1个红包不需要验证

    def test_noNeedValidate_oneCoupou(self):
        needvalidate= self.dlservice.isNeedValidate(self.s,'123',800,300,1)
        self.assertEqual(needvalidate['flag'],0)





def suite():
    suite=unittest.TestSuite()
    suite.addTest(isNeedValidate("test_needValidate"))
    suite.addTest(isNeedValidate("test_noNeedValidate"))
    suite.addTest(isNeedValidate("test_needValidate_oneCoupou"))
    suite.addTest(isNeedValidate("test_noNeedValidate_oneCoupou"))
    return suite















