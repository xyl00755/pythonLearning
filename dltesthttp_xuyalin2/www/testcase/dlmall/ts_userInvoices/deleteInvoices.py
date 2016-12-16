#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/userInvoices/delete.html

post
require: data form

invoiceId:a3205a61f1f947df8c82648743ece3c2

response: json string
{
    "status": 1,
    "msg": "",
    "data":""
}

"""

class deleteInvoices(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserInvoicesInfo = eData('UserInvoices')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)

    def setUp(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)

    def addInvoices(self,isDefault):
        self.dlservice.addInvoices(self.s,self.UserInvoicesInfo.invoicesHeader,self.UserInvoicesInfo.invoicesType,isDefault)


    #非默认发票抬头删除成功

    def test_deleteInvoices_notDefault(self):
        self.addInvoices(0)
        invoiceslist= self.dlservice.normalInvoices(self.s)
        deletestatus= self.dlservice.deleteInvoices(self.s,invoiceslist['data']['list'][0]['invoiceId'])
        self.assertEqual(deletestatus['status'],0)

    #默认发票抬头删除成功
    def test_deleteInvoices_default(self):
        self.addInvoices(self.UserInvoicesInfo.isDefault)
        invoicelist=self.dlservice.normalInvoices(self.s)
        deletestatus=self.dlservice.deleteInvoices(self.s,invoicelist['data']['list'][0]['invoiceId'])
        self.assertEqual(deletestatus['status'],0)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(deleteInvoices("test_deleteInvoices_notDefault"))
    suite.addTest(deleteInvoices("test_deleteInvoices_default"))
    return suite




