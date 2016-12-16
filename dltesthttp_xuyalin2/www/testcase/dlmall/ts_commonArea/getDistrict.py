#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
url:
http://127.0.0.1:8280/common/getDistrict.html
request:
response:
{
    "result":[
        {
            "districtCode":"CHNP035C345D2998",
            "cityCode":"CHNP035C345",
            "districtName":"赤尾屿",
            "postCode":null,
            "logicDeleteFlg":null
        },
        {
            "districtCode":"CHNP035C345D2999",
            "cityCode":"CHNP035C345",
            "districtName":"乐山呼叫中心岛",
            "postCode":null,
            "logicDeleteFlg":null
        },
        {
            "districtCode":"CHNP035C345D3001",
            "cityCode":"CHNP035C345",
            "districtName":"黄岩岛",
            "postCode":null,
            "logicDeleteFlg":null
        }
    ],
    "success":true
}
"""

class getDistrict(unittest.TestCase):

    UserShop=wsData('DealMager')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username,UserShop.password)

    #UserShop=eData('DealMager')

    #用例执行前的操作
    #def setUp(self):

    #获取东海省-钓鱼岛下的区县级城市数量
    def test_getDistrict(self):
        getDistrictInfo = self.dlservice.getCity(self.s,"CHNP035C345")
        self.assertEqual(len(getDistrictInfo['result']),3)

    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getDistrict("test_getDistrict"))
    return suite