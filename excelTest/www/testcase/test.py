#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HTMLTestRunner

import sys
path = sys.path[0] + '/../..'
sys.path.append(path)
import unittest

from www.testcase.ts_ws_login import login
from www.common.database import *
from www.testcase.ts_ws_shoppingcart import createOrderByShoppingcart
from www.testcase.ts_ws_password import modifyPassword
from www.testcase.ts_ws_merch import getMerchList
from www.testcase.ts_ws_shoppingcart import addShoppingcart
from www.testcase.ts_ws_deliverAddress import getDeliverAddressList
from www.testcase.ts_ws_deliverAddress import addDeliverAddress
from www.testcase.ts_ws_invoice import addInvoice
from www.testcase.ts_ws_merch import getMerchDetail

if __name__ == '__main__':


    create_engine()
    runner = unittest.TextTestRunner()
    #runner.run(login.suite())

    #filePath = "pyResult.html"
    #fp = file(filePath,'wb')
    #runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Python Test Report',description='This  is Python  Report')
    runner.run(getMerchDetail.suite())
    #runner.run(addDeliverAddress.suite())
    #runner.run(modifyPassword.suite())
    #fp.close()
    #runner.run(ts_ws_invoice_getInvoiceList.suite())
    #runner.run(ts_ws_invoice_modifyInvoice.suite())
    #runner.run(ts_ws_invoice_setDefaultInvoice.suite())

    #runner.run(ts_ws_common_getTopicList.suite())

