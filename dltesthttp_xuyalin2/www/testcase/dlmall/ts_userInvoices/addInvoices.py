#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/userInvoices/add.html

post
require: json data

{
    "invoiceHeader": "丹露测试发票抬头3",
    "invoicesType": "N011",
    "isDefault": "1"
}

response: json string
{
    "status": 1,
    "msg": "",
    "data":""
}

"""

class addInvoices(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserInvoicesInfo = eData('UserInvoices')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)

    #增加发票抬头成功
    def test_addInvoices_sucess(self):
        addinvoices= self.dlservice.addInvoices(self.s,self.UserInvoicesInfo.invoicesHeader,self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)
        self.assertEqual(addinvoices['status'],0)

    #重复增加相同的发票抬头失败
    def test_addInvoices_failed(self):
        self.dlservice.addInvoices(self.s,self.UserInvoicesInfo.invoicesHeader,self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)
        addinvoices= self.dlservice.addInvoices(self.s,self.UserInvoicesInfo.invoicesHeader,self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)
        self.assertEqual(addinvoices['status'],1)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(addInvoices("test_addInvoices_sucess"))
    suite.addTest(addInvoices("test_addInvoices_failed"))
    return suite
