#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
0230.获取所有区域列表
http://127.0.0.1:8280/mallws/common/area/getAllAreaList.json
{
    "token":"9a9ce53d88be4609af8d51112b4893f5"                      // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "topList": [
            {
                "code": "P001",
                "name": "北京",
                "childList": [
                    {
                        "code": "C001",
                        "name": "北京市",
                        "childList": [
                            {
                                "code": "D0001",
                                "name": "东城区",
                                "childList": null
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.AreaListResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import *
from www.common.database import select_int
from www.common.excel import wsData


class getAllAreaList(unittest.TestCase):

    UserShop = wsData('TmlShop')

    # S1.获取所有区域列表
    def test_getAllAreaList_all(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAllAreaList()
        self.assertEqual(areaList.model['success'], '0')
        provinceNum = select_int('select count(*) from dlpublic.dl_area where area_parent_code = ?', 'CHN')
        self.assertEqual(len(areaList.model['topList']),provinceNum)


    # S2.无token时获取区域列表
    def test_getAllAreaList_noToken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        areaList = ws.getAllAreaList(token='null')
        self.assertEqual(areaList.code, 600)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(getAllAreaList("test_getAllAreaList_all"))
    suite.addTest(getAllAreaList("test_getAllAreaList_noToken"))
    return suite