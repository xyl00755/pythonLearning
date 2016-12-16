#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
common_pic_06.获取主题列表（品类及其他）
http://127.0.0.1:8280/mallws/common/pic/getTopicList_V2.json
{
	"token":"123"	//必选
}

{
    "code": 200,												   //100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
    "description": "执行成功!",
    "model": {
        "success": "0"                                             // 0-成功 1-失败
		"topicList": [                                             // 主题列表
			{
				"topicType":"T01",                                 // 类型:T01-白酒，T02-葡萄酒，T03-饮料，T04-副食，T11-我的订单，T12-我的红包，T13-我的常购，T14-抽奖抢红包
				"topicTitle":"酒类",                               // 标题
				"topicDesc":"标题描述",                            // 描述-预留字段
				"picUrl":"123"                                     // 图片url
				"linkUrl":""                                       // 链接地址-预留字段
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.GetTopicListResponse"
    }
}
"""

import unittest
from www.common.excel import wsData
from www.api.webservice import webservice
from www.common.database import *


class getTopicList_V2(unittest.TestCase):

    UserShop = wsData('TmlShop')
    Param = wsData('Param')

    # S1.获取banner图片地址
    def test_getTopicList_get(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        TopicList = ws.getTopicList_V2()
        self.assertEqual(TopicList.model['success'], '0')
        self.assertEqual(len(TopicList.model['topicList']), 8)
        for i in range(len(TopicList.model['topicList'])):
            self.assertIsNotNone(TopicList.model['topicList'][i]['topicTitle'])
            self.assertIsNotNone(TopicList.model['topicList'][i]['picUrl'])

    # S2.不带token获取banner图片地址
    def test_getTopicList_noToken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        TopicList = ws.getTopicList_V2(token='null')
        self.assertEqual(TopicList.code, 600)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getTopicList_V2("test_getTopicList_get"))
    suite.addTest(getTopicList_V2("test_getTopicList_noToken"))
    return suite
