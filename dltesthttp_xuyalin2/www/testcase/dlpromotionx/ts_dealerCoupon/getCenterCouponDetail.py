#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *
from www.api.dlpromotionx import *

"""
url:
http://127.0.0.1:8280/dealerCoupon/getGoodsCouponDetail
request:
 {
    "companyId": "asdasd",
    "dealerCouponType": "10",
    "categoryCode": "C01L0102",
    "brandIds": ["123"，"123"，"123"],
    "dealerName": "河北人人大",
    "goodsName": "茅台500mL",
    "showWay": "0",
    "pageIndex": 1,
    "pageSize": 2,
    "sortParams": "default"
  }


response:
 {
  "status": 0,
  "data": {
    "data_list": [
      {
        "dealerCouponName": "广州酒类专卖店连锁有限公司",
        "dealerCouponType": "11",
        "availableChannel": "S011,S012",
        "dealerCouponImgUrl": "http://www.danlu.com/resources/images/home/newIndex/logo.png",
        "platformLimit": "WEB",
        "activityId": "1111616038328",
        "activityName": "广州酒类专卖店连锁有限公司送券活动",
        "effectiveDate": "2016.10.10",
        "unEffectiveDate": "2016.10.20",
        "dealerId": "xx",
        "dealerName": "广州酒类专卖店连锁有限公司",
        "goodsId": "1ef4f0f84096e24c16a61d74787d4beb",
        "goodsName": "马爹利名士干邑白兰地",
        "dealerCouponId": "2806039403",
        "dealerCouponStatus": 4,
        "couponMinAmt": 1000,
        "effectiveAmt": 2000,
        "expiredStatus": 0,
        "effectiveAmtFlag": 1
      },
      {
        "dealerCouponName": "广州酒类专卖店连锁有限公司",
        "dealerCouponType": "11",
        "availableChannel": "S011,S012",
        "dealerCouponImgUrl": "http://www.danlu.com/resources/images/home/newIndex/logo.png",
        "platformLimit": "WEB",
        "activityId": "1111616038328",
        "activityName": "广州酒类专卖店连锁有限公司送券活动",
        "effectiveDate": "2016.10.10",
        "unEffectiveDate": "2016.10.20",
        "dealerId": "xx",
        "dealerName": "广州酒类专卖店连锁有限公司",
        "goodsId": "1ef4f0f84096e24c16a61d74787d4beb",
        "goodsName": "马爹利名士干邑白兰地",
        "dealerCouponId": "2806039403",
        "dealerCouponStatus": 4,
        "couponMinAmt": 1000,
        "effectiveAmt": 2000,
        "expiredStatus": 0,
        "effectiveAmtFlag": 1
      }
    ],
    "total": 2,
    "index": 1,
    "size": 5,
    "sort": ""
  },
  "msg": "查询成功"
}

  """

class getCenterCouponDetail(unittest.TestCase):

    UserShop1=wsData('DealMager')
    UserShop2=wsData('TmlShop')

    #用例执行前的操作
    #def setUp(self):

    #检验查询结果为优惠券
    def test_YHQ(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="11",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["dealerCouponType"],"11")

    #检验查询结果为经销商红包
    def test_dealerCoupon(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["dealerCouponType"],"10")

    #检验优惠券查询结果的可用店铺类型均含有该终端店的类型
    def test_availableChannel_YHQ(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="11",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(unicode(self.UserShop2.shopType,"utf-8") in each["availableChannel"],True)

    #检验经销商红包查询结果的可用店铺类型均含有该终端店的类型
    def test_availableChannel_dealerCoupon(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(unicode(self.UserShop2.shopType,"utf-8") in each["availableChannel"],True)

    #检验优惠券的查询结果均为APP、WEB通用
    def test_channel_YHQ(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["platformLimit"],"WEB;APP")

    #检验经销商红包的查询结果均为APP、WEB通用
    def test_channel_dealerCoupon(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="11",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["platformLimit"],"WEB;APP")

    #检验通过经销商查询的结果均为该经销商下的优惠券
    def test_dealerName_YHQ(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="11",categoryCode=None,brandIds=None,dealerName=self.UserShop1.fullName,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["dealerName"],unicode(self.UserShop1.fullName,'utf-8'))

    #检验通过经销商查询的结果均为该经销商下的经销商红包
    def test_dealerName_dealerCoupon(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=self.UserShop1.fullName,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["dealerName"],unicode(self.UserShop1.fullName,'utf-8'))

    #检验经销商红包的goodsName为空
    def test_dealerCoupon_goodsNameIsNone(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertEqual(each["goodsName"],None)

    #校验优惠券的goodsName不为空
    def test_YHQ_goodsNameIsNotNone(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="11",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        for each in info["data"]["data_list"]:
            self.assertIsNot(each["goodsName"],None)

    #校验优惠券每页展示12条数据
    def test_pageSize_YHQ(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="11",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        self.assertEqual(info['data']['size'],12)

    #校验经销商红包每页展示12条数据
    def test_pageSize_dealerCoupon(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        self.assertEqual(info['data']['size'],12)

    #校验total字段和list长度一致
    def test_totalEqualsList(self):
        dlservice = dlpromotionx()
        info = dlservice.getCenterCouponDetail(companyId=self.UserShop2.companyId,dealerCouponType="10",categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=1,pageSize=12,sortParams='default')
        self.assertEqual(info['data']['total'],len(info['data']['data_list']))


    #用例执行完后的操作
    #def tearDown(self):

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getCenterCouponDetail("test_YHQ"))    #done
    suite.addTest(getCenterCouponDetail("test_dealerCoupon"))     #done
    suite.addTest(getCenterCouponDetail("test_availableChannel_YHQ"))   #done
    suite.addTest(getCenterCouponDetail("test_availableChannel_dealerCoupon"))    #done
    suite.addTest(getCenterCouponDetail("test_channel_YHQ"))        #done
    suite.addTest(getCenterCouponDetail("test_channel_dealerCoupon"))   #done
    suite.addTest(getCenterCouponDetail("test_dealerName_YHQ"))   #done
    suite.addTest(getCenterCouponDetail("test_dealerName_dealerCoupon"))  #done
    suite.addTest(getCenterCouponDetail("test_dealerCoupon_goodsNameIsNone"))  #done
    suite.addTest(getCenterCouponDetail("test_YHQ_goodsNameIsNotNone"))   #done
    suite.addTest(getCenterCouponDetail("test_pageSize_YHQ"))   #done
    suite.addTest(getCenterCouponDetail("test_pageSize_dealerCoupon"))  #done
    suite.addTest(getCenterCouponDetail("test_totalEqualsList"))  #done
    return suite