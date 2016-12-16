#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
0231.选择获取区域列表
http://127.0.0.1:8280/mallws/common/area/getAreaListByCondition.json
{
    "token":"9a9ce53d88be4609af8d51112b4893f5",                     // 必须
    "provinceCode":"P011",                                          // 可选 见详细
    "cityCode": "C088"                                              // 可选 见详细
}

{
    // 结构同上一个(http://127.0.0.1:8280/mallws/common/area/getAllAreaList.json)接口
}

参数校验:
    // 不做
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
param说明:
    provinceCode/cityCode为可选参数  可以 全不传/只传provinceCode/全传 (不可只传cityCode) (如果全传 必须保证市属于省)
    1.全不传 返回所有省份列表 第一个省份对应的所有市列表 第一个省份的第一个市对应的所有区列表
    2.只传provinceCode 返回所有省份列表 选择的省份的所有市列表 选择的省份的第一个市对应的所有区列表
    3.全传 返回所有省份列表 选择的省份的所有市列表 选择的省份的选择的市的所有区列表
"""

import unittest

from www.api.webservice import *
from www.common.database import select_int
from www.common.excel import wsData


class getAreaListByCondition(unittest.TestCase):

    UserShop = wsData('TmlShop')

    # S1.获取所有区域列表
    def test_getAreaListByCondition_province(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListByCondition()
        self.assertEqual(areaList.model['success'], '0')
        provinceNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHN')
        self.assertEqual(len(areaList.model['topList']),provinceNum)

    # S2.获取四川省区域列表
    def test_getAreaListByCondition_city(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListByCondition(provinceCode='P023')
        self.assertEqual(areaList.model['success'], '0')
        cityNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHNP023')
        flag = False
        for i in range(0, len(areaList.model['topList'])):
            if areaList.model['topList'][i]['code'] == 'P023' :
                self.assertEqual(len(areaList.model['topList'][i]['childList']), cityNum)
                flag = True
        self.assertEqual(flag, True, '未找到相应的省份')


    # S3.获取县级列表
    def test_getAreaListByCondition_county(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListByCondition(provinceCode='P023',cityCode='C238')
        self.assertEqual(areaList.model['success'], '0')
        countryNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHNP023C238')
        flag = False
        for i in range(0, len(areaList.model['topList'])):
            if areaList.model['topList'][i]['code'] == 'P023':
                for j in range(0, len(areaList.model['topList'][i]['childList'])):
                    if areaList.model['topList'][i]['childList'][j]['code'] == 'C238':
                        self.assertEqual(len(areaList.model['topList'][i]['childList'][j]['childList']), countryNum)
                        flag = True
        self.assertEqual(flag, True, '未找到相应的省市')

    # S4.当市不属于省时获取列表——当前是不属于省则获取该省列表

    # S5.未带token时返回600
    def test_getAreaListByCondition_notoken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAreaListByCondition(token='null')
        self.assertEqual(areaList.code, 600)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(getAreaListByCondition("test_getAreaListByCondition_province"))
    suite.addTest(getAreaListByCondition("test_getAreaListByCondition_city"))
    suite.addTest(getAreaListByCondition("test_getAreaListByCondition_county"))
    suite.addTest(getAreaListByCondition("test_getAreaListByCondition_notoken"))
    return suite