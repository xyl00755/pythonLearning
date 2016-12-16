#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest

from www.common.database import *
from www.common.excel import *
from www.api.webservice import *


"""
LB02.领券中心/抢经销商红包：可参与的活动列表(筛选条件)
http://127.0.0.1:8280/mallws/dealerCoupon/getActivityList.json
{
	"token":"123",
	"dealerCouponType":"10",                                       // 经销商优惠券类型：10-红包 11-优惠券
    "categoryCode": "C01L0101",                                    // 类目code：C01L0101-白酒 C01L0102-葡萄酒 C01T01-茶 C01L0103-洋酒 C01L0104-啤酒 C01X0101-其他饮品
	"dealerName": "测试经销商",                                    // 发放店铺：经销商名字（支持模糊查询）
    "merchName":"五粮液",                                          // 适用商品：商品名字（支持模糊查询）
    "sortField":"0",                                               // 排序字段：0-按面额排序 1-按过期时间排序
    "sortType":"0"                                                 // 排序方式：0-升序 1-降序
	"page":1,                                                      // 必须
    "rows":20                                                      // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                             // 0-成功 1-失败
		"activityList": [                                          // 优惠券活动列表
			{
				"activityId":"activity01",                         // 优惠券活动主健
				"activityStatus":"01",                             // 优惠券活动状态：01-可领取 02-已领取 03-已领完 04-已过期
				"couponAmt":"20000",                               // 优惠券金额：单位分
				"amtUseLimit":"满200可以使用",                     // 金额使用限制
				"dealerLimit":"湖北人人大",                        // 经销商使用限制
				"channelLimit":"烟酒专卖店",                       // 渠道使用限制
				"merchLimit":"白云边1919",                         // 商品使用限制
				"platformLimit":"web,app",                         // 平台使用限制
				"expireDate":"2016-09-18",                         // 过期日期
				"useDate":"2016-09-01"                             // 使用日期
			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.GetActivityListResponse"
    }
}
"""

class getActivityList(unittest.TestCase):

    UserCoupon = eData('TmlShop')
    CouponLst1 = eData('CouponLst1')
    CouponLst2 = eData('CouponLst2')
    CouponLst3 = eData('CouponLst3')
    CouponLst5 = eData('CouponLst5')
    GiftMoney1 = eData('GiftMoney1')

    #获取全部优惠卷列表
    def test_getActicityList_all(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        allCouponList = ws.getActivityList(dealerCouponType = 11,rows = 9999,page = 1)
        self.test_assertParameter_key(allCouponList,self.CouponLst1)

    #获取优惠卷列表为空的情况
    def test_getCouponList_wasNull(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType='11',dealerName= 'wgh测试经销商11'.encode('utf-8'),page='1', rows='9999')
        self.assertEqual(getActivityList.model['success'], '0')
        flag = False
        if getActivityList.model['activityList'] is None:
            flag = True
        self.assertEqual(flag, True, 'the activityList is not null')

    #验证优惠卷数量的情况
    def test_getCouponList_notNull(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11 ,page = 1 ,rows = 9999)
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0 , len(getActivityList.model['activityList'])):
          i += 1
          if i == 5:
             flag = True
             self.assertEqual(flag,True,'the number of coupon is wrong')

    #获取优惠卷列表为不为空的情况:判断优惠卷分页以及是否会重复
    def test_getCouponList_CountCoupon(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11 ,rows = 99999)
        CountingCoupon = len(getActivityList.model['activityList'])
        self.assertEqual(getActivityList.code,200)
        self.assertEqual(getActivityList.model['success'],'0')
        appearTime  = 0
        for k in range(1,CountingCoupon/20+2):
            for i in range(0,len(getActivityList.model['activityList'])):
                if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdWhiteWine:
                    appearTime += 1
                else:
                    k += 1
        self.assertEqual(appearTime,1,self.CouponLst1.activityIdWhiteWine + 'is appeared more than one times')

    #按照白酒类目进行筛选
    def test_getCouponList_byWhitewine(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01L0101',rows = 999,page = 1 )
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][0]['activityId'] == self.CouponLst1.activityIdWhiteWine:
                if getActivityList.model['activityList'][1]['activityId'] == self.CouponLst5.activityId:
                    flag = True
                    self.assertEqual(flag,True, self.CouponLst1.activityIdWhiteWine + 'is not found')

    #按照葡萄酒泪目进行筛选
    def test_getCouponList_byRedwine(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01L0102',rows = 999,page = 1)
        self.assertEqual(getActivityList.code, 200)
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdRedWine:
                flag = True
        self.assertEqual(flag,True,self.CouponLst1.activityIdRedWine + 'is not found')

    #按照茶泪目进行筛选
    def test_getCouponList_byTea(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01T01',rows = 999,page = 1)
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdGreenTea:
                flag = True
        self.assertEqual(flag,True,self.CouponLst1.activityIdGreenTea + 'is not found')

    #按照洋酒泪目进行筛选
    def test_getCouponList_byForwine(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01L0103',rows = 999,page = 1)
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdForWine:
                flag = True
        self.assertEqual(flag,True,self.CouponLst1.activityIdForWine + 'is not found')


    #按照啤酒类目进行筛选
    def test_getCouponList_byBeer(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01L0104',rows = 999,page = 1)
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdBeer:
                flag = True
        self.assertEqual(flag,True,self.CouponLst1.activityIdBeer + 'is not found')

    #按照其它饮品类目进行筛选
    def test_getCouponList_byOther(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01X0101',rows = 999,page = 1)
        self.assertEqual(getActivityList.model['success'],'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdDrinking:
                flag = True
        self.assertEqual(flag,True,self.CouponLst1.activityIdDrinking + 'is not found')


    #组合筛选返回结果为空的情况
    def test_getCouponList_combinationConditionNull(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01X0101',dealerName = '测试经销商', rows = 999,page = 1)
        self.assertEqual(getActivityList.model['success'], '0')
        flag = False
        if getActivityList.model['activityList'] is None:
                flag = True
        self.assertEqual(flag,True,'found is wrong')


    #组合筛选返回结果不为空的情况
    def test_getCouponList_combinationConditionNotNull(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getActivityList = ws.getActivityList(dealerCouponType = 11,categoryCode = 'C01T01',merchName = '扩展名MaxMaxMaxMaxMaxMa',rows = 999,page = 1)
        self.assertEqual(getActivityList.model['success'] ,'0')
        flag = False
        for i in range(0,len(getActivityList.model['activityList'])):
            if getActivityList.model['activityList'][i]['activityId'] == self.CouponLst1.activityIdGreenTea:
                flag = True
        self.assertEqual(flag,True,self.CouponLst1.activityIdGreenTea + 'is not found')


    #领券中心排序功能，升序排列和降序排列
    def test_getCouponList_SortCouponList(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)

        #按照面额升序排列
        getActivityListAmtAsc = ws.getActivityList(dealerCouponType= 11,sortField = 0,sortType = 0,rows = 999,page = 1)
        self.assertEqual(getActivityListAmtAsc.model['activityList'][0]['activityId'] , self.CouponLst1.activityIdRedWine)
        self.assertEqual(getActivityListAmtAsc.model['activityList'][3]['activityId'] , self.CouponLst5.activityId)

        #按照面额降序排列
        getActivityListAmtDesc = ws.getActivityList(dealerCouponType = 11,sortField = 0,sortType = 1,rows = 999,page = 1 )
        self.assertEqual(getActivityListAmtDesc.model['activityList'][0]['activityId'],self.CouponLst1.activityIdGreenTea)
        self.assertEqual(getActivityListAmtDesc.model['activityList'][1]['activityId'],self.CouponLst1.activityIdForWine)

        #按照过期时间升序排列
        getActivityListDateAsc = ws.getActivityList(dealerCouponType = 11,sortField = 1,sortType = 0,rows = 999,page = 1)
        self.assertEqual(getActivityListDateAsc.model['activityList'][0]['activityId'],self.CouponLst5.activityId)
        self.assertEqual(getActivityListDateAsc.model['activityList'][1]['activityId'],self.CouponLst1.activityIdWhiteWine)

        #按照过期时间降序排列
        getActivityListDateDesc = ws.getActivityList(dealerCouponType = 11,sortField = 1,sortType = 1,rows = 999,page = 1)
        self.assertEqual(getActivityListDateDesc.model['activityList'][0]['activityId'],self.CouponLst1.activityIdForWine)
        self.assertEqual(getActivityListDateDesc.model['activityList'][1]['activityId'],self.CouponLst1.activityIdRedWine)

    #获取红包数据列表
    def test_getGiftMoneyList_allGiftMoney(self):
        ws = webservice()
        ws.login(self.UserCoupon.username,self.UserCoupon.password)
        getGiftMoneyList = ws.getActivityList(dealerCouponType = 10,rows = 999,page = 1)
        self.assertEqual(getGiftMoneyList.model['success'],'0')
        flag = False
        for i in range(0,len(getGiftMoneyList.model['activityList'])):
            if getGiftMoneyList.model['activityList'][i]['activityId'] == self.GiftMoney1.activityId:
                flag = True
        self.assertEqual(flag,True,self.GiftMoney1.activityId + 'is not found')

    #校验具体rsp的body键值对类型一致
    def test_assertCouponList_rspBody(self):
      ws = webservice()
      ws.login(self.UserCoupon.username,self.UserCoupon.password)
      allActivityList = ws.getActivityList(dealerCouponType = 11,rows = 999,page = 1)
      self.assertEqual(allActivityList.code, 200)

    def test_assertParameter_key(self,rspBody,coupon , success = '0',description = u'执行成功'):
         self.assertEqual(rspBody.model['success'], success)
         flag = False
         for i in range(1,len(rspBody.model['activityList'])):
          if rspBody.model['activityList'][i]['activityStatus'] == 01:
            pass
          else:
            return  flag
         self.assertEqual(rspBody.model['activityList'][i]['activityId'],coupon.activityId)
         self.assertEqual(rspBody.model['activityList'][i]['activityStatus'],coupon.CouponAmt)
         self.assertEqual(rspBody.model['activityList'][i]['couponAmt'],coupon.CouponAmt)
         self.assertEqual(rspBody.model['activityList'][i]['amtUseLimit'],coupon.amtUseLimit)
         self.assertEqual(rspBody.model['activityList'][i]['dealerLimit'],coupon.dealerLimit)
         self.assertEqual(rspBody.model['activityList'][i]['channelLimit'],coupon.channelLimit)
         self.assertEqual(rspBody.model['activityList'][i]['merchLimit'],coupon.merchLimit)
         self.assertEqual(rspBody.model['activityList'][i]['platformLimit'],coupon.platformLimit)
         self.assertEqual(rspBody.model['activityList'][i]['expireDate'],coupon.expireDate)
         self.assertEqual(rspBody.model['activityList'][i]['useDate'],coupon.useDate)
         flag = True
         self.assertEqual(flag,True,self.UserCoupon.activityId + 'is not found')


#将上面的def添加到test suite中
def suite():
    suite = unittest.TestSuite()
    suite.addTest(getActivityList("test_getActicityList_all"))
    suite.addTest(getActivityList("test_getCouponList_wasNull"))
    suite.addTest(getActivityList("test_getCouponList_notNull"))
    suite.addTest(getActivityList("test_getCouponList_CountCoupon"))
    suite.addTest(getActivityList("test_getCouponList_byWhitewine"))
    suite.addTest(getActivityList("test_getCouponList_byRedwine"))
    suite.addTest(getActivityList("test_getCouponList_byTea"))
    suite.addTest(getActivityList("test_getCouponList_byForwine"))
    suite.addTest(getActivityList("test_getCouponList_byBeer"))
    suite.addTest(getActivityList("test_getCouponList_byOther"))
    suite.addTest(getActivityList('test_getCouponList_combinationConditionNull'))
    suite.addTest(getActivityList("test_getCouponList_combinationConditionNotNull"))
    suite.addTest(getActivityList("test_getCouponList_SortCouponList"))
    suite.addTest(getActivityList("test_getGiftMoneyList_allGiftMoney"))
    suite.addTest(getActivityList("test_assertCouponList_rspBody"))
    return suite