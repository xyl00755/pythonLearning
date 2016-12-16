#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
0286.获取Banner图片地址
http://127.0.0.1:8280/mallws/common/pic/getBannerList.json
{
	"token":"123"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                              // 0-成功 1-失败
		"bannerList": [                                             // Banner列表
			{
				"bannerType":"B01",                                 // 类型:B01-顶部banner B02-中部banner
				"bannerTitle":"红包活动",                           // 标题-预留字段
				"bannerDesc":"图片描述",                            // 描述-预留字段
				"picUrl":"123"                                      // 图片url
				"linkUrl":""                                        // 链接地址
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.GetBannerListResponse"
    }
}
"""

import unittest

from www.api.webservice import *
from www.common.excel import wsData


class getBannerList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    Param = wsData('Param')

    # S1.获取banner图片地址
    def test_getBannerList_get(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        bannerList = ws.getBannerList()
        self.assertEqual(bannerList.model['success'], '0')

    # S2.不带token获取banner图片地址
    def test_getBannerList_noToken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        bannerList = ws.getBannerList(token='null')
        self.assertEqual(bannerList.code, 600)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getBannerList("test_getBannerList_get"))
    suite.addTest(getBannerList("test_getBannerList_noToken"))
    return suite