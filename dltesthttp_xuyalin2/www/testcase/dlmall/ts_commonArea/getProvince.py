#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
url:
http://127.0.0.1:8280/common/getProvince.html
request:
response:
{
    "result":[
        {
            "provinceCode":"CHNP001",
            "provinceName":"北京",
            "sorted":null,
            "logicDeleteFlg":null
        },
        {
            "provinceCode":"CHNP002",
            "provinceName":"天津",
            "sorted":null,
            "logicDeleteFlg":null
        }
    ],
    "success":true
}

"""

class getProvince(unittest.TestCase):

    UserShop=wsData('DealMager')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    #用例执行前的操作
    #def setUp(self):

    #获取省份个数
    def test_getProvince(self):
        getProvinceInfo = self.dlservice.getProvince(self.s)
        self.assertEqual(len(getProvinceInfo['result']),35)

    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getProvince("test_getProvince"))
    return suite