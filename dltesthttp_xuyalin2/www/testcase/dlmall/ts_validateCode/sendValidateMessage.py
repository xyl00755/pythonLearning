#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/vilidateCode/sendMessage.html

post
require: data form
phoneNo:17608011804

response: json string

"""

class sendValidateMessage(unittest.TestCase):
    UserShop = wsData('TmlShop')
    validateCodeInfo=eData('validateCode')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def test_sendValidateMessage(self):
        validatemessage=self.dlservice.sendValidateMessage(self.s,self.validateCodeInfo.phoneNo)
        self.assertEqual(validatemessage,200)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(sendValidateMessage("test_sendValidateMessage"))
    return suite



