#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/userInvoices/modify.html

post
require: form data

invoiceId:a3205a61f1f947df8c82648743ece3c2
invoiceHeader:丹露测试发票抬头111
invoicesType:N011


response: json string

{
    "status": 1,
    "msg": "",
    "data":""
}
"""

class modifyInvoices(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserInvoicesInfo = eData('UserInvoices')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)



    def setUp(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)

    def addInvoices(self):
        self.dlservice.addInvoices(self.s,self.UserInvoicesInfo.invoicesHeader,self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)


    #修改发票抬头成功
    def test_modifyInvoices_sucess(self):
        self.addInvoices()
        invoiceslist= self.dlservice.normalInvoices(self.s)
        name =u'丹露'
        name=name.encode('utf-8')
        modifystatus= self.dlservice.modifyInvoices(self.s,invoiceslist['data']['list'][0]['invoiceId'],name,self.UserInvoicesInfo.invoicesType)
        invoiceslist= self.dlservice.normalInvoices(self.s)
        self.assertEqual(modifystatus['status'],0)
        self.assertEqual(invoiceslist['data']['list'][0]['invoiceHeader'].encode('utf-8'),name)

    #修改发票抬头不成功
    def test_modifyInvoices_failed(self):
        self.addInvoices()
        invoiceslist= self.dlservice.normalInvoices(self.s)
        name =u'丹露'
        name=name.encode('utf-8')
        modifystatus= self.dlservice.modifyInvoices(self.s,'123456',name,self.UserInvoicesInfo.invoicesType)
        self.assertEqual(modifystatus['status'],1)


    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(modifyInvoices("test_modifyInvoices_sucess"))
    suite.addTest(modifyInvoices("test_modifyInvoices_failed"))
    return suite




