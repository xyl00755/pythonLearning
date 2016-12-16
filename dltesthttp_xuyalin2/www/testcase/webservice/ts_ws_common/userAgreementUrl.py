#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
0254.获取用户协议URL
http://127.0.0.1:8280/mallws/common/url/userAgreementUrl.json
{
	// 请求不需要参数
}

{
	"code": "200",
	"description": "执行成功!",
	"model": {
		"success": "0",                      									  // 0-成功 1-失败
		"userAgreementUrl": "http://www.danlu.com/registerEasy/agreement.html"    // 用户协议URL
	},
	"metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.common.UserAgreementResponse"
    }

}

参数校验:
		无
code说明:
    200-成功 400-非法的参数 500-服务器异常
"""

import unittest

from www.api.webservice import *
from www.common.excel import wsData


class userAgreementUrl(unittest.TestCase):

    agreeurl = wsData('Param')

    # S1.获取用户注册协议URL
    def test_userAgreementUrl_get(self):
        ws = webservice()
        agreeUrl = ws.userAgreementUrl()
        self.assertEqual(agreeUrl.model['success'],'0')
        self.assertEqual(agreeUrl.model['userAgreementUrl'], self.agreeurl.agreementUrl)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(userAgreementUrl("test_userAgreementUrl_get"))
    return suite