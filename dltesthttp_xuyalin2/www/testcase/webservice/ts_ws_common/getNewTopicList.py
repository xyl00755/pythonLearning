#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import wsData

"""
LB01.首页：获取品类图标（经销商红包，优惠券）
http://127.0.0.1:8280/mallws/common/pic/getNewTopicList.json
{
	"token":"123"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                             // 0-成功 1-失败
		"topicList": [                                             // 主题列表
			{
				"topicType":"T01",                                 // 类型:T01-白酒，T02-葡萄酒，T03-啤酒，T04-其他饮品，T11-我的订单，T12-我的常购，T13-经销商红包，T14-优惠券
				"topicTitle":"白酒",                               // 标题
				"topicDesc":"标题描述",                            // 描述-预留字段
				"picUrl":"http://asset.danlu.com/upload/img/cate_icon/homepage_entranceitem_whitewine.png"           // 图片url
				"linkUrl":"http://coupon.danlu.com/m"                                                                // 链接地址:点击图标后跳转地址，如T13-经销商红包
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.GetTopicListResponse"
    }
}
"""
class getNewTopicList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    Param = wsData('Param')

    # S1.获取banner图片地址
    def test_getNewTopicList_get(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        TopicList = ws.getNewTopicList()
        self.assertEqual(TopicList.model['success'], '0')
        self.assertEqual(len(TopicList.model['topicList']),8)

    # S2.不带token获取banner图片地址
    def test_getNewTopicList_noToken(self):
        ws = webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        TopicList = ws.getNewTopicList(token='null')
        self.assertEqual(TopicList.code, 600)

    # S3.不存在的token获取banner图片地址
    def test_getNewTopicList_noExistToken(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        TopicList=ws.getNewTopicList(token='1234567890')
        self.assertEqual(TopicList.code,100)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getNewTopicList("test_getNewTopicList_get"))
    suite.addTest(getNewTopicList("test_getNewTopicList_noToken"))
    suite.addTest(getNewTopicList("test_getNewTopicList_noExistToken"))
    return suite