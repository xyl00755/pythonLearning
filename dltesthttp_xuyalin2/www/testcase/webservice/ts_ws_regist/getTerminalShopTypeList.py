#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0242.获取店铺类型列表
http://127.0.0.1:8280/mallws/regist/getTerminalShopTypeList.json
{

}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                          // 成功 0-成功
		"shopList": [
			{
				"codeId": "S011",                //店铺类型代码
				"codeValue": "烟酒专卖店"        //店铺类型内容
			}
		]
	},
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.ShopTypeListResponse"
    }
}

参数校验:
    // 不需验证
code说明:
    200-成功 400-非法的参数 500-服务器异常
"""

import unittest

from www.api.webservice import *

class getTerminalShopTypeList(unittest.TestCase):

    # S1.注册时获取店铺类型列表
    def test_getTShopType_list(self):
        ws = webservice()
        tmlShopList = ws.getTerminalShopTypeList()
        self.assertEqual(tmlShopList.code, 200)
        self.assertEqual(tmlShopList.model['success'], '0')
        self.assertEqual(tmlShopList.model['shopList'][0]['codeId'], 'S011')
        self.assertEqual(tmlShopList.model['shopList'][0]['codeValue'], '烟酒专卖店')
        self.assertEqual(tmlShopList.model['shopList'][1]['codeId'], 'S012')
        self.assertEqual(tmlShopList.model['shopList'][1]['codeValue'], '便利店')
        self.assertEqual(tmlShopList.model['shopList'][2]['codeId'], 'S013')
        self.assertEqual(tmlShopList.model['shopList'][2]['codeValue'], '餐饮店')
        self.assertEqual(tmlShopList.model['shopList'][3]['codeId'], 'S014')
        self.assertEqual(tmlShopList.model['shopList'][3]['codeValue'], '商业超市')
        self.assertEqual(tmlShopList.model['shopList'][4]['codeId'], 'S015')
        self.assertEqual(tmlShopList.model['shopList'][4]['codeValue'], '其它')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getTerminalShopTypeList("test_getTShopType_list"))
    return suite