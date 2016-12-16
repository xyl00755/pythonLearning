#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
http://127.0.0.1:8280/mallws/common/area/getAreaListStandAlone.json
{
    "token":"26a4f98c2c894011bf12d81ea1a2e72f",         // 必须
    "provinceCode":"P003",                              // 可选
    "cityCode":"C006"                                   // 可选
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "topList": [
            {
                "code": "D0093",
                "name": "邯山区",
                "childList": null
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.AreaListResponse"
    }
}

参数校验:
    // 不做
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
param说明:
    provinceCode/cityCode为可选参数
    1.全不传 返回省份列表
    2.只传provinceCode 返回省份下的所有市列表
    3.传cityCode 返回市下的所有区列表
"""

import unittest

from www.api.webservice import *
from www.common.database import select_int
from www.common.excel import wsData


class getAreaListStandAlone(unittest.TestCase):

    UserShop = wsData('TmlShop')

    # S1.获取所有区域列表
    def test_getAreaListStandAlone_province(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListStandAlone()
        self.assertEqual(areaList.model['success'], '0')
        provinceNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHN')
        self.assertEqual(len(areaList.model['topList']),provinceNum)

    # S2.获取四川省区域列表
    def test_getAreaListStandAlone_city(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListStandAlone(provinceCode='P023')
        self.assertEqual(areaList.model['success'], '0')
        cityNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHNP023')
        self.assertEqual(len(areaList.model['topList']), cityNum)



    # S3.获取县级列表
    def test_getAreaListStandAlone_county(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListStandAlone(provinceCode='P023',cityCode='C238')
        self.assertEqual(areaList.model['success'], '0')
        countryNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHNP023C238')
        self.assertEqual(len(areaList.model['topList']), countryNum)


    # S4.当市不属于省时获取列表——当前是不属于省则获取该省列表

    # S5.未带token时返回600
    def test_getAreaListStandAlone_notoken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListStandAlone(token='null')
        self.assertEqual(areaList.code, 600)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getAreaListStandAlone("test_getAreaListStandAlone_province"))
    suite.addTest(getAreaListStandAlone("test_getAreaListStandAlone_city"))
    suite.addTest(getAreaListStandAlone("test_getAreaListStandAlone_county"))
    suite.addTest(getAreaListStandAlone("test_getAreaListStandAlone_notoken"))
    return suite