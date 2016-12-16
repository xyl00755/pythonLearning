#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
url:
http://127.0.0.1:8280/common/getCity.html
request:
response:
{
    "result":[
        {
            "cityCode":"CHNP035C345",
            "provinceCode":"CHNP035",
            "cityName":"钓鱼岛",
            "areaCode":null,
            "logicDeleteFlg":null
        }
    ],
    "success":true
}

"""


class getCity(unittest.TestCase):

    UserShop=wsData('DealMager')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    #用例执行前的操作
    #def setUp(self):

    #获取东海省的市级城市数量
    def test_getCityOfDonghai(self):
        getCityInfo = self.dlservice.getCity(self.s,"CHNP035")
        self.assertEqual(len(getCityInfo['result']),1)

    #获取四川省的市级城市数量
    def test_getCityOfSichuan(self):
        getCityInfo = self.dlservice.getCity(self.s,"CHNP023")
        self.assertEqual(len(getCityInfo['result']),21)

    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getCity("test_getCityOfDonghai"))
    suite.addTest(getCity("test_getCityOfSichuan"))
    return suite