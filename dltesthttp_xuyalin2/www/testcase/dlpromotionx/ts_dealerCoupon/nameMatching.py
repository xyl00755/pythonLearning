#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *

"""
URL：http://127.0.0.1:8280//nameMatching
请求示例：
{
    'dealerName':隆兴旺超市,
    'companyType':S01,
    'pageIndex':1,
    'pageSize':10
}

返回示例：
 {
    "status": 0,
    "data": {
      "storeList":[
        {
         "companyId": "企业ID",
          "companyName":"买家名称或店铺名称",
          "companyType":"企业类型",
          "terminalType":"终端店类型",
          "invitationCompany":"邀请企业",
          "invitationUser":"邀请销售员",
          "regAreaCode":"注册地址",
          "detailAddress":"详细地址",
          "contactName":"联系人"
        },
        {
          "companyId": "企业ID",
          "companyName":"买家名称或店铺名称",
          "companyType":"企业类型",
          "terminalType":"终端店类型",
          "invitationCompany":"邀请企业",
          "invitationUser":"邀请销售员",
          "regAreaCode":"注册地址",
          "detailAddress":"详细地址",
          "contactName":"联系人"
        }
      ]
    },
    "msg":"查询成功"
  }
"""

class nameMatching(unittest.TestCase):

    #执行用例前的操作
    #def setUp(self):

    #（交易平台）联想的所有值为经销商
    def test_nameMatching_mall_JXS(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.nameMatching(dealerName='test',companyType = "S02",pageIndex = 1,pageSize = 10)
        for each in nameMatchingInfo["data"]:
            self.assertEqual(each["companyType"],"S02")


    #（交易平台）验证数量正确性（返回10个带有"test"的经销商名称，前提：经销商名包含“test”的数量超过10个）
    def test_nameMatching_mall_number10(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.nameMatching(dealerName='test',companyType = "S02",pageIndex = 1,pageSize = 10)
        self.assertEqual(len(nameMatchingInfo['data']),10)


    #（交易平台）验证联想正确性（返回全匹配‘test’的经销商名称，前提：经销商名包含“test”的数量超过10个）
    def test_nameMatching_mall_contain(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.nameMatching(dealerName='test',companyType = "S02",pageIndex = 1,pageSize = 10)
        for each in nameMatchingInfo["data"]:
            self.assertEqual("test" in each['companyName'],True)


    #（运营平台）联想的所有值为终端店
    def test_nameMatching_admin_ZDD(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.nameMatching(dealerName='test',companyType = "S01",pageIndex = 1,pageSize = 10)
        for each in nameMatchingInfo["data"]:
            self.assertEqual(each["companyType"],"S01")


    #（运营平台）验证数量正确性（返回10个带有"test"的终端店名称，前提：终端店名包含“test”的数量超过10个）
    def test_nameMatching_admin_number10(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.nameMatching(dealerName='test',companyType = "S01",pageIndex = 1,pageSize = 10)
        self.assertEqual(len(nameMatchingInfo['data']),10)


    #（运营平台）验证联想正确性（返回全匹配‘test’的终端店名称，前提：终端店名包含“test”的数量超过10个）
    def test_nameMatching_admin_contain(self):
        dlservice = dlpromotionx()
        nameMatchingInfo = dlservice.nameMatching(dealerName='test',companyType = "S01",pageIndex = 1,pageSize = 10)
        for each in nameMatchingInfo["data"]:
            self.assertEqual("test" in each['companyName'],True)

    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite=unittest.TestSuite()
    suite.addTest(nameMatching("test_nameMatching_mall_JXS"))
    suite.addTest(nameMatching("test_nameMatching_mall_number10"))
    suite.addTest(nameMatching("test_nameMatching_mall_contain"))
    suite.addTest(nameMatching("test_nameMatching_admin_ZDD"))
    suite.addTest(nameMatching("test_nameMatching_admin_number10"))
    suite.addTest(nameMatching("test_nameMatching_admin_contain"))
    return suite