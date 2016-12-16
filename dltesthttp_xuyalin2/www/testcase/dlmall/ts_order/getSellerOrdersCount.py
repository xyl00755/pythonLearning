#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
http://127.0.0.1:8280/orders/getSellerOrdersCount.html?date=1474532184439

{
    "customerId": "cb595ea8968a4b87b885d08a2834904e",
    "status": null
}
"""
class getSellerOrdersCount(unittest.TestCase):

    UserShop=eData('WebManager')

    def test_getSellerOrdersCount(self):
        dlservice = dlmall()
        s = dlservice.login(self.UserShop.username,self.UserShop.password)
        sellerCount=dlservice.getSellerOrdersCount(s)
        self.assertEqual(sellerCount['customerId'],'cb595ea8968a4b87b885d08a2834904e')
        self.assertEqual(sellerCount['status'],None)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getSellerOrdersCount("test_getSellerOrdersCount"))
    return suite

if __name__ == '__main__':
    #create_engine()
    runner = unittest.TextTestRunner()
    runner.run(getSellerOrdersCount.suite())