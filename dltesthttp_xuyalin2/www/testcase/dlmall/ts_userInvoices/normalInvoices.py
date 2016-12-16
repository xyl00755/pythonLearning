#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/userInvoices/normal.html

get
require:
response: json string

 {
    "status": 0,
    "msg": "",
    "data": {
        "count": 1,
        "list": [
            {
                "customerId": "3b60e4efef4f43709dbfb909e0393d63",
                "invoiceId": "01247144fa7f4799b45b4b3f548b68ee",
                "invoiceType": "N011",
                "invoiceHeader": "鸿燕副食",
                "isDefault": "1",
                "createdTimestamp": "1464915551000",
                "createdPerson": "hongan",
                "updateTimestamp": "1464915551000",
                "updatePerson": "hongan"
            }
        ]
    }
}

"""

class normalInvoices(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserInvoicesInfo = eData('UserInvoices')
    dlservice = dlmall()
    s = dlservice.login(UserShop.username, UserShop.password)



    def setUp(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)

    def addInvoices(self,invoicesType,isDefalut= 0):
        for i in range(3):
            self.dlservice.addInvoices(self.s,self.UserInvoicesInfo.invoicesHeader+str(i),invoicesType,isDefalut)

    #验证普通发票列表长度是否正确
    def test_normalInvoices_list(self):
        self.addInvoices(self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)
        normalinvoiceslist= self.dlservice.normalInvoices(self.s)
        self.assertEqual(normalinvoiceslist['status'],0)
        self.assertEqual(normalinvoiceslist['data']['count'],3)
        self.assertEqual(len(normalinvoiceslist['data']['list']),3)


    #插入值是否和返回值一致
    def test_normalInvoices_invoiceHeader(self):
        self.addInvoices(self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)
        normalinvoiceslist= self.dlservice.normalInvoices(self.s)
        self.assertEqual(normalinvoiceslist['data']['list'][0]['customerId'],self.UserInvoicesInfo.user_id)
        self.assertEqual(normalinvoiceslist['data']['list'][0]['invoiceHeader'].encode('utf-8'),u'刘莎测试地址2'.encode('utf-8'))


    #验证有且只能有一个默认的发票抬头
    def test_normalInvoices_isDefault(self):
        self.addInvoices(self.UserInvoicesInfo.invoicesType,self.UserInvoicesInfo.isDefault)
        normalinvoiceslist= self.dlservice.normalInvoices(self.s)
        count = 0
        for i in range(3):
            if ('1' ==normalinvoiceslist['data']['list'][i]['isDefault']):
                count+=1
        self.assertEqual(count,1)


    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?',
               self.UserInvoicesInfo.user_id)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(normalInvoices("test_normalInvoices_list"))
    suite.addTest(normalInvoices("test_normalInvoices_invoiceHeader"))
    suite.addTest(normalInvoices("test_normalInvoices_isDefault"))
    return suite

