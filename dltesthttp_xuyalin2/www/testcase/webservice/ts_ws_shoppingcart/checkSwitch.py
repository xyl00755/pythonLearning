#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
1.检查是否需要弹出后续的验证信息
http://127.0.0.1:8080/mallws/shoppingcart/checkSwitch.json
{
    "token":"123",                       // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
		"success": "0",                  //0-成功  1-未知错误
        "bigCouponFlag": "0",            //0-需要开启 1-不需要开启
        "amount": "20"                   //提示金额（分）
    },
     "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.checkSwitchResponse"
    }
}
"""

import unittest

from www.api.webservice import *
from www.common.database import update
from www.common.excel import wsData


class checkSwitch(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')
    Param = wsData('Param')

    def setUp(self):
        update('update dlpromotionx.dl_promotionx_rule set rule_desc = ?,coupon_amount = ? where id = ?', self.Param.bigCouponFlag, str(int(self.Param.amount)/100), '9')

    # S1.检查是否需要校验大额红包
    def test_checkSwitch_bigRedPacket(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        checkSwitch = ws.checkSwitch()
        self.assertEqual(checkSwitch.model['success'], '0')
        self.assertEqual(checkSwitch.model['bigCouponFlag'], self.Param.bigCouponFlag)
        self.assertEqual(checkSwitch.model['amount'], self.Param.amount)

    # S2.不带token
    def test_checkSwitch_noToken(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        checkSwitch = ws.checkSwitch(token='null')
        self.assertEqual(checkSwitch.code, 600)

    # S3.修改配置文件后检查
    def test_checkSwitch_modify(self):
        update('update dlpromotionx.dl_promotionx_rule set rule_desc = ?,coupon_amount = ? where id = ?', '0', '5', '9')

        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        checkSwitch = ws.checkSwitch()
        self.assertEqual(checkSwitch.model['success'], '0')
        self.assertEqual(checkSwitch.model['bigCouponFlag'], '0')
        self.assertEqual(checkSwitch.model['amount'], '500')

    def tearDown(self):
        update('update dlpromotionx.dl_promotionx_rule set rule_desc = ?,coupon_amount = ? where id = ?', self.Param.bigCouponFlag, str(int(self.Param.amount)/100), '9')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(checkSwitch("test_checkSwitch_bigRedPacket"))
    suite.addTest(checkSwitch("test_checkSwitch_noToken"))
    suite.addTest(checkSwitch("test_checkSwitch_modify"))
    return suite