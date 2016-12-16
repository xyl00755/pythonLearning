#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0203.设置默认发票
http://127.0.0.1:8280/mallws/mydl/invoice/setDefaultInvoice.json
{
    "token":"66dc3c0d3cf7408c8d1845b9448a0e37",             // 必须
    "invoiceId":"8c67a8cdca294d25ad1e7d8b8f7e95c2"          // 必须 发票id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-未知失败 2-只有一张发票，不允许修改 3-发票不存在
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

class setDefaultInvoice(unittest.TestCase):

    UserShop1 = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    #create_engine('danlu2_test', 'b49d2591f2a0577B', 'dl_company', 'danlu2test.mysql.rds.aliyuncs.com', '3406')

    # S1.设置发票为默认发票
    def test_setDefault_normal(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = 'Normal1')
        ws.addInvoice(invoiceHeader = 'Normal2')
        invoice1 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal1')
        self.assertEqual(invoice1.is_default, '1')
        invoice2 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal2')
        setDefault = ws.setDefaultInvoice(invoiceId = invoice2.invoice_id)
        self.assertEqual(setDefault.model['success'], '0')

        invoice1 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal1')
        invoice2 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal2')
        self.assertEqual(invoice1.is_default, '0')
        self.assertEqual(invoice2.is_default, '1')

    # S2.设置已默认的发票为默认发票
    def test_setDefault_normalAgain(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = 'Normal1')
        ws.addInvoice(invoiceHeader = 'Normal2')
        invoice1 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal1')
        setDefault = ws.setDefaultInvoice(invoiceId = invoice1.invoice_id)
        self.assertEqual(setDefault.model['success'], '1')

        invoice1 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal1')
        invoice2 = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'Normal2')
        self.assertEqual(invoice1.is_default, '1')
        self.assertEqual(invoice2.is_default, '0')

    # S3.设置不存在的发票为默认发票
    def test_setDefault_notExist(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        setDefault = ws.setDefaultInvoice(invoiceId = 'notExist')
        self.assertEqual(setDefault.model['success'], '3')

    # S4.invoiceid为空设置为默认发票——bug5153，其实success不应该为3
    def test_setDefault_normalNull(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        setDefault = ws.setDefaultInvoice(invoiceId = 'notExist')
        self.assertEqual(setDefault.model['success'], '3')

    # S5.设置其他人的发票为默认发票
    def test_setDefault_normalOther(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        setDefault = ws.setDefaultInvoice(invoiceId = self.UserShop1.invoiceId)
        self.assertEqual(setDefault.model['success'], '3')


    # S6.设置增值税发票为默认发票
    def test_setDefault_vat(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvVAT = ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        setDefault = ws.setDefaultInvoice(invoiceId = 'notExist')
        self.assertEqual(setDefault.model['success'], '3')

    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?', self.UserShop2.userId)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(setDefaultInvoice("test_setDefault_normal"))
    suite.addTest(setDefaultInvoice("test_setDefault_normalAgain"))
    suite.addTest(setDefaultInvoice("test_setDefault_notExist"))
    suite.addTest(setDefaultInvoice("test_setDefault_normalNull"))
    suite.addTest(setDefaultInvoice("test_setDefault_vat"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'suite')