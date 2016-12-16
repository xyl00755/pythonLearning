#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/vilidateCode/validateImgCode.html

post
require: data form
imgCode:5277

response: json string

true

"""

class validateImgCode(unittest.TestCase):
    UserShop = wsData('TmlShop')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def test_validateImgCode(self):
        validateimagecode= self.dlservice.validateImgCode(self.s,1111)
        self.assertEqual(validateimagecode,False)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(validateImgCode("test_validateImgCode"))
    return suite

