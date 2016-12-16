#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0201.删除发票
http://127.0.0.1:8280/mallws/mydl/invoice/delInvoice.json
{
    "token":"36805433b4d14ba98faf37b0edefe53a",             // 必须
    "invoiceId":"c3dce8ed1d054c69963fa63b526b5884"          // 必须 发票id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-未知失败 2-发票不存在
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

class delInvoice(unittest.TestCase):

    UserShop2 = wsData('TmlShop2')
    UserShop1 = wsData('TmlShop')

    # S1.删除普通发票
    def test_delInvoice_normal(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N011')
        delInvNormal = ws.delInvoice(invoiceId = invoiceNormal.invoice_id)
        self.assertEqual(delInvNormal.model['success'], '0')
        getInvList = ws.getInvoiceList()
        self.assertEqual(getInvList.model['normalInvoiceList'],[])

    # S2.删除不存在的发票
    def test_delInvoice_notExist(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        delInvNormalNotExist = ws.delInvoice(invoiceId = 'notExist')
        self.assertEqual(delInvNormalNotExist.model['success'], '2')

    # S3.删除其他用户的发票
    def test_delInvoice_other(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        delInvNormalOther = ws.delInvoice(invoiceId = self.UserShop1.invoiceId)
        self.assertEqual(delInvNormalOther.model['success'], '2')

    # S4.删除发票后再新增同样的发票
    def test_delInvoice_again(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N011')
        ws.delInvoice(invoiceId = invoiceNormal.invoice_id)
        addInvNormalAgain = ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(addInvNormalAgain.model['success'], '0')
        invoiceNormal2 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N011')
        ws.delInvoice(invoiceId = invoiceNormal2.invoice_id)


    # S5.删除发票id为空
    def test_delInvoice_null(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        delInvNull = ws.delInvoice(invoiceId = None)
        self.assertEqual(delInvNull.model['success'], '2')

    # S6.删除增值税发票——已报bug #5358
    def test_defInvoice_vat(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        invoiceVat = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N012')
        delInvVat = ws.delInvoice(invoiceVat.invoice_id)
        self.assertEqual(delInvVat.model['success'], '1')

    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?', self.UserShop2.userId)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(delInvoice("test_delInvoice_normal"))
    suite.addTest(delInvoice("test_delInvoice_notExist"))
    suite.addTest(delInvoice("test_delInvoice_other"))
    suite.addTest(delInvoice("test_delInvoice_again"))
    suite.addTest(delInvoice("test_delInvoice_null"))
    suite.addTest(delInvoice("test_defInvoice_vat"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'suite')