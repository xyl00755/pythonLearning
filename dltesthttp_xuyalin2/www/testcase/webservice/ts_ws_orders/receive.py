#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0182.订单收货
http://127.0.0.1:8280/mallws/orders/oper/receive.json
{
    "token":"123",                      // 必须
    "paymentNo":"paymentNo",            // 必须 大订单号
    "orderNo":"123123",                 // 必须 订单号
    "payType":"123"                     // 必须 支付类型
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                      // 0-成功 1-订单状态发生变化收货失败 2-收货失败
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest


class receive(unittest.TestCase):

    pass


def suite():
    suite = unittest.TestSuite()
    return suite