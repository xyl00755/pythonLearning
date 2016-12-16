#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
类目接口预设
merch_07.获取类目列表
http://127.0.0.1:8280/mallws/merch/getAllCategory.json
{
    "token":"e422b788987047d1b9684bd8a1ec3e75"   //必须
}

{
    "code": 200,																						//100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
    "description": "执行成功!",
    "model": {
		"success": "0",
		"baseImgStr": "http://static.danlu.com/mobile/",												//类目图片前缀
		"categoryList":[
			{
				"categoryName": "白酒",																	//类目名称
				"categoryCode": "C01L0101",     														//类目编码
				"children": [{																			//二级类目下面的所有子类
					"categoryName": "茅台 ",
					"categoryCode": "C01L0101_01",
					"categoryUrl": "%E8%8C%85%E5%8F%B0.png""											//类目图片名	encode过
				}]
			}
		]
	}

    "metadata": {
        "type": 1,
        "clazz": ["cn.com.hd.mall.web.webservices.entity.response.merch.CategoryListResponse"]
    }
}
"""

import unittest
from www.common.excel import wsData
from www.api.webservice import webservice
from www.common.database import *


class getAllCategory(unittest.TestCase):

    UserShop = wsData('TmlShop')

    # S1.获取类目列表
    def test_getAllCategory_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allCategory = ws.getAllCategory()
        self.assertEqual(allCategory.model['success'], '0')
        self.assertEqual(allCategory.model['baseImgStr'], 'http://static.danlu.com/mobile/')
        self.assertAllCategory(allCategory=allCategory.model['categoryList'])


    # S2.无token获取类目列表
    def test_getAllCategory_noToken(self):
        ws = webservice()
        allCategory = ws.getAllCategory()
        self.assertEqual(allCategory.code, 600)

    def assertAllCategory(self, allCategory):
        levelOne = select('select * from danlu_cd_database.t_m_merchandise_left_menu_new where parent_id = ? or parent_id = ? order by sort', 0, 99)
        self.assertEqual(len(allCategory),len(levelOne)-12)
        for i in range(len(allCategory)):
            self.assertEqual(allCategory[i]['categoryName'], levelOne[i]['menu_name'])
            self.assertEqual(allCategory[i]['categoryCode'], levelOne[i]['menu_code'])
            levelTwo = select('select * from danlu_cd_database.t_m_merchandise_left_menu_new where parent_id = ? order by sort', levelOne[i]['id'])
            import urllib
            for j in range(len(allCategory[i]['children'])):
                self.assertEqual(allCategory[i]['children'][j]['categoryName'], levelTwo[j]['menu_name'])
                self.assertEqual(allCategory[i]['children'][j]['categoryCode'], levelTwo[j]['menu_code'])
                rspURL = allCategory[i]['children'][j]['categoryUrl']
                rspName = urllib.quote(str(levelTwo[j]['menu_name']).replace('/', '')+'.png')
                self.assertEqual(rspURL, rspName)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getAllCategory("test_getAllCategory_all"))
    suite.addTest(getAllCategory("test_getAllCategory_noToken"))
    return suite
