#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0243.获取终端店地区列表
http://127.0.0.1:8280/mallws/regist/getArea.json
{
    "search": "CHN"                               // 必填 "CHN"-获取省份列表 "CHNPXXX"-获取城市列表 "CHNPXXXCXXX"-获取区县列表
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                          // 成功 0-成功
		"areaList": [
					  {
						"areaCode": "CHNP001",                  //地区代码
						"areaName": "北京"                      //地区内容
					  }
					]
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.AreaResponse"
    }
}

参数校验:
    // 必须验证
	"terminalAreaProvinceCode"                  @NotNull，不为空字符串
    "terminalAreaCityCode"                      @NotNull，不为空字符串
    "terminalAreaDistrictCode"                  @NotNull，不为空字符串
code说明:
    200-成功 400-非法的参数 500-服务器异常
"""

import unittest

from www.api.webservice import *
from www.common.database import select_one,select_int

class getArea(unittest.TestCase):

    # S1.获取国家列表
    def test_getArea_nation(self):
        ws = webservice()
        nationList = ws.getArea('0')
        nationDb = select_one('select * from dlpublic.dl_area where area_parent_code = ?', '0')
        self.assertEqual(nationList.code, 200)
        self.assertEqual(nationList.model['success'], '0')
        self.assertEqual(nationList.model['areaList'][0]['areaCode'], nationDb.area_code)
        self.assertEqual(nationList.model['areaList'][0]['areaName'], nationDb.area_name)

    # S2.获取省份列表
    def test_getArea_province(self):
        ws = webservice()
        provinceList = ws.getArea('CHN')
        provinceNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHN')
        self.assertEqual(provinceList.code, 200)
        self.assertEqual(provinceList.model['success'], '0')
        self.assertEqual(len(provinceList.model['areaList']), provinceNum)

    # S3.获取市级列表
    def test_getArea_city(self):
        ws = webservice()
        cityList = ws.getArea('CHNP023')
        cityNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHNP023')
        self.assertEqual(cityList.code, 200)
        self.assertEqual(cityList.model['success'], '0')
        self.assertEqual(len(cityList.model['areaList']), cityNum)

    # S4.获取县级列表
    def test_getArea_county(self):
        ws = webservice()
        countyList = ws.getArea('CHNP023C237')
        countyNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHNP023C237')
        self.assertEqual(countyList.code, 200)
        self.assertEqual(countyList.model['success'], '0')
        self.assertEqual(len(countyList.model['areaList']), countyNum)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getArea("test_getArea_nation"))
    suite.addTest(getArea("test_getArea_province"))
    suite.addTest(getArea("test_getArea_city"))
    suite.addTest(getArea("test_getArea_county"))
    return suite