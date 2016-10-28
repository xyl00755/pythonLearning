#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(sys.path[0])

import unittest
from www.common.database import create_engine
from www.testcase.dldata.ts_dealerQuery import queryCouponTotalAmtOnAdmin

if __name__ == '__main__':

    create_engine()
    runner = unittest.TextTestRunner()
    runner.run(queryCouponTotalAmtOnAdmin.suite())




