#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *
from www.operation.redisCache import deleteActivityKey

"""
WQ01.获取我的经销商优惠券/红包 列表
http://127.0.0.1:8280/mallws/dealerCoupon/getCouponList.json
{
	"token":"123",
	"couponStatus":"1",                                           // 必须 优惠劵状态（01–未使用;02-已使用;03-已过期）
	"dealerCouponType":"1",										  // 必须 类型 11-经销商优惠券 10-经销商红包
    "page":1,                                                     // 必须
    "rows":20                                                     // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                            // 0-成功 1-失败
		"couponList": [                                           // 经销商优惠券/红包 列表
			{
				"couponCode":"10006230",                          // 优惠券/红包编号
				"orderNo":"1011",								  // 使用订单编号(已使用的经销商优惠券/红包特有)
				"couponName":"**优惠券",                          // 优惠券/红包名称
				"couponStatus":"01",                              // 优惠劵/红包状态（01–未使用;02-已使用;03-已过期）
				"couponAmt":"20000",                              // 优惠券/红包金额
				"timeLeft":"12",							      // 剩余天数
				"expireDate":"2016-09-18",                        // 过期日期
				"useDate":"2016-09-01",                           // 使用日期
                "amtUseLimit":"满200可以使用",                    // 金额使用限制
				"dealerLimit":"湖北人人大",                       // 经销商使用限制
				"channelLimit":"烟酒专卖店",                      // 渠道使用限制
				"merchLimit":"白云边1919",                        // 商品使用限制
				"platformLimit":"web,app",                        // 平台使用限制

			}
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerCoupon.GetCouponListResponse"
    }
}
"""
class getDealerCouponList(unittest.TestCase):
    UserShop=wsData('TmlShop')
    coupon1=eData('AvailableCouponsBenfits')

    def setUp(self):
        self.tearDown()

    #正确获取未使用的经销商优惠券
    def test_getCouponList_0111(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        # ws.achieveCoupon(activityId=self.coupon1.benefitActivityId)
        # time.sleep(60)
        getCoupon=ws.getDealerCouponList(couponStatus='01',dealerCouponType='11',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertSucces2(res=getCoupon,couponType=11)

    #正确获取已使用的经销商优惠券
    def test_getCouponList_0211(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        # ws.achieveCoupon(activityId=self.coupon1.benefitActivityId)
        # time.sleep(60)
        #self.changeCouponStatus(couponStatus='02',couponType=11)
        getCoupon=ws.getDealerCouponList(couponStatus='02',dealerCouponType='11',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertSucces2(res=getCoupon,couponType=11)

    #正确获取已过期的经销商优惠券
    def test_getCouponList_0411(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        # ws.achieveCoupon(activityId=self.coupon1.benefitActivityId)
        # time.sleep(60)
        # self.changeCouponStatus(couponStatus='04',couponType=11)
        getCoupon=ws.getDealerCouponList(couponStatus='04',dealerCouponType='11',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertSucces2(res=getCoupon,couponType=11)

    #正确获取未使用的经销商红包
    def test_getCouponList_0110(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        # achieve=ws.achieveCoupon(activityId=self.coupon1.couponActivityId)
        # time.sleep(60)
        getCoupon=ws.getDealerCouponList(couponStatus='01',dealerCouponType='10',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertSucces2(res=getCoupon,couponType=10)
        # self.deleteSql(couponType=10)

    #正确获取已使用的经销商红包
    def test_getCouponList_0210(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        # ws.achieveCoupon(activityId=self.coupon1.couponActivityId)
        # time.sleep(60)
        # self.changeCouponStatus(couponStatus='02',couponType=10)
        getCoupon=ws.getDealerCouponList(couponStatus='02',dealerCouponType='10',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertSucces2(res=getCoupon,couponType=10)

    #正确获取已过期的经销商红包
    def test_getCouponList_0410(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        # ws.achieveCoupon(activityId=self.coupon1.couponActivityId)
        # time.sleep(60)
        # self.changeCouponStatus(couponStatus='04',couponType=10)
        getCoupon=ws.getDealerCouponList(couponStatus='04',dealerCouponType='10',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertSucces2(res=getCoupon,couponType=10)

    #couponStatus为空
    def test_getCouponList_couponStatusNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getDealerCouponList(couponStatus='',dealerCouponType='11',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')
        self.assertEqual(getCoupon.model['couponList'],[])

    #dealerCouponType为空
    def test_getCouponList_couponTypeNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getDealerCouponList(couponStatus='01',dealerCouponType='',page=1,rows=15)
        self.assertEqual(getCoupon.model['success'],'0')

    #page&rows为空
    def test_getCouponList_pageNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getDealerCouponList(couponStatus='01',dealerCouponType='11',page=None,rows=None)
        self.assertEqual(getCoupon.model['success'],'0')

    #token为空
    def test_getCouponList_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCoupon=ws.getDealerCouponList(couponStatus='01',dealerCouponType='11',page=1,rows=15,token='null')
        self.assertEqual(getCoupon.code,600)

    def assertSucces(self,res=None,couponType=None):
        if couponType==11:
            couponList=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id=? and issue_person=?',self.coupon1.benefitActivityId,self.coupon1.tmlCompanyId)
            couponEntityId=couponList.dealer_coupon_entity_id
            couponEntity=select_one('select * from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id=?',couponEntityId)
            coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',self.coupon1.dealerBenefitId)
            for i in range(len(res.model['couponList'])):
                if res.model['couponList'][i]['couponCode']==couponEntityId:
                    self.assertEqual(res.model['couponList'][i]['couponName'],couponEntity.dealer_coupon_name)
                    self.assertEqual(res.model['couponList'][i]['couponStatus'],couponEntity.dealer_coupon_entity_status)
                    self.assertEqual(res.model['couponList'][i]['couponAmt'],str(coupon.coupon_min_amt))
                    self.assertIn(res.model['couponList'][i]['expireDate'],str(couponEntity.uneffective_time))
                    self.assertIn(res.model['couponList'][i]['useDate'],str(couponEntity.effective_time))
                    self.assertEqual(res.model['couponList'][i]['amtUseLimit'],str(couponEntity.effective_amount))
                    self.assertEqual(res.model['couponList'][i]['dealerLimit'],couponEntity.dealer_name)
                    self.assertEqual(res.model['couponList'][i]['channelLimit'],'烟酒专卖店')
                    self.assertEqual(res.model['couponList'][i]['merchLimit'],couponEntity.goods_name)
                    self.assertEqual(res.model['couponList'][i]['merchId'],couponEntity.goods_id)
        else:
            couponList=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id=? and issue_person=?',self.coupon1.couponActivityId,self.coupon1.tmlCompanyId2)
            couponEntityId=couponList.dealer_coupon_entity_id
            couponEntity=select_one('select * from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id=?',couponEntityId)
            coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',self.coupon1.dealerCouponId)
            for i in range(len(res.model['couponList'])):
                if res.model['couponList'][i]['couponCode']==couponEntityId:
                    self.assertEqual(res.model['couponList'][i]['couponName'],couponEntity.dealer_coupon_name)
                    self.assertEqual(res.model['couponList'][i]['couponStatus'],couponEntity.dealer_coupon_entity_status)
                    self.assertEqual(res.model['couponList'][i]['couponAmt'],str(coupon.coupon_min_amt))
                    self.assertIn(res.model['couponList'][i]['expireDate'],str(couponEntity.uneffective_time))
                    self.assertIn(res.model['couponList'][i]['useDate'],str(couponEntity.effective_time))
                    self.assertEqual(res.model['couponList'][i]['amtUseLimit'],str(couponEntity.effective_amount))
                    self.assertEqual(res.model['couponList'][i]['dealerLimit'],couponEntity.dealer_name)
                    self.assertEqual(res.model['couponList'][i]['channelLimit'],'烟酒专卖店')
                    self.assertEqual(res.model['couponList'][i]['merchLimit'],None)
                    self.assertEqual(res.model['couponList'][i]['merchId'],None)
    def assertSucces2(self,res=None,couponType=None):
        if couponType==11:
            if res.model['couponList'] != []:
                couponEntityId=res.model['couponList'][0]['couponCode']
                couponIdSql=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_entity_id=?',couponEntityId)
                couponId=couponIdSql.dealer_coupon_id
                coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',couponId)
                couponEntity=select_one('select * from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id=?',couponEntityId)
                for i in range(len(res.model['couponList'])):
                    if res.model['couponList'][i]['couponCode']==couponEntityId:
                        self.assertEqual(res.model['couponList'][i]['couponName'],couponEntity.dealer_coupon_name)
                        self.assertEqual(res.model['couponList'][i]['couponStatus'],couponEntity.dealer_coupon_entity_status)
                        self.assertEqual(res.model['couponList'][i]['couponAmt'],str(coupon.coupon_min_amt))
                        self.assertIn(res.model['couponList'][i]['expireDate'],str(couponEntity.uneffective_time))
                        self.assertIn(res.model['couponList'][i]['useDate'],str(couponEntity.effective_time))
                        self.assertEqual(res.model['couponList'][i]['amtUseLimit'],str(couponEntity.effective_amount))
                        self.assertEqual(res.model['couponList'][i]['dealerLimit'],couponEntity.dealer_name)
                        #self.assertEqual(res.model['couponList'][i]['channelLimit'],'烟酒专卖店')
                        self.assertEqual(res.model['couponList'][i]['merchLimit'],couponEntity.goods_name)
                        self.assertEqual(res.model['couponList'][i]['merchId'],couponEntity.goods_id)
        else:
            if res.model['couponList'] != []:
                couponEntityId=res.model['couponList'][0]['couponCode']
                couponIdSql=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_entity_id=?',couponEntityId)
                couponId=couponIdSql.dealer_coupon_id
                coupon=select_one('select * from dlcoupon.dl_coupon_detail where coupon_id=?',couponId)
                couponEntity=select_one('select * from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id=?',couponEntityId)
                for i in range(len(res.model['couponList'])):
                    if res.model['couponList'][i]['couponCode']==couponEntityId:
                        self.assertEqual(res.model['couponList'][i]['couponName'],couponEntity.dealer_coupon_name)
                        self.assertEqual(res.model['couponList'][i]['couponStatus'],couponEntity.dealer_coupon_entity_status)
                        #self.assertEqual(res.model['couponList'][i]['couponAmt'],str(coupon.coupon_min_amt))
                        self.assertIn(res.model['couponList'][i]['expireDate'],str(couponEntity.uneffective_time))
                        self.assertIn(res.model['couponList'][i]['useDate'],str(couponEntity.effective_time))
                        self.assertEqual(res.model['couponList'][i]['amtUseLimit'],str(couponEntity.effective_amount))
                        self.assertEqual(res.model['couponList'][i]['dealerLimit'],couponEntity.dealer_name)
                        #self.assertEqual(res.model['couponList'][i]['channelLimit'],'烟酒专卖店')
                        self.assertEqual(res.model['couponList'][i]['merchLimit'],couponEntity.goods_name)
                        self.assertEqual(res.model['couponList'][i]['merchId'],couponEntity.goods_id)



    #改变优惠券红包使用状态
    def changeCouponStatus(self,couponStatus=None,couponType=None):
        if couponType==11:
            couponList=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id=? and issue_person=?',self.coupon1.benefitActivityId,self.coupon1.tmlCompanyId)
            couponEntityId=couponList.dealer_coupon_entity_id
            update('update dlpromotionx.dl_dealer_coupon_snapshot set dealer_coupon_entity_status=? where dealer_coupon_id=?',couponStatus,couponEntityId)
        else:
            couponList=select_one('select * from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id=? and issue_person=?',self.coupon1.couponActivityId,self.coupon1.tmlCompanyId2)
            couponEntityId=couponList.dealer_coupon_entity_id
            update('update dlpromotionx.dl_dealer_coupon_snapshot set dealer_coupon_entity_status=? where dealer_coupon_id=?',couponStatus,couponEntityId)


    def tearDown(self):
        update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',self.coupon1.dealerBenefitId)  # 领取实体快照
        update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',self.coupon1.dealerBenefitId)  # 领取记录
        # 恢复库存
        update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',0,0,self.coupon1.dealerBenefitId)
        deleteActivityKey(benefitActivityId=self.coupon1.benefitActivityId,benefitId=self.coupon1.dealerBenefitId,tmlCompanyId=self.coupon1.tmlCompanyId)  #删除redis中的缓存

    def deleteSql(self,couponType=None):
        if couponType==11:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',self.coupon1.dealerBenefitId)  # 领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',self.coupon1.dealerBenefitId)  # 领取记录
            # 恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',0,0,self.coupon1.dealerBenefitId)
            deleteActivityKey(benefitActivityId=self.coupon1.benefitActivityId,benefitId=self.coupon1.dealerBenefitId,tmlCompanyId=self.coupon1.tmlCompanyId)  #删除redis中的缓存
        else:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',self.coupon1.dealerCouponId)  # 领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',self.coupon1.dealerCouponId)  # 领取记录
            # 恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',0,0,self.coupon1.dealerCouponId)
            deleteActivityKey(couponActivityId=self.coupon1.couponActivityId,tmlCompanyId=self.coupon1.tmlCompanyId2)  #删除redis中的缓存




def suite():
    suite = unittest.TestSuite()
    suite.addTest(getDealerCouponList("test_getCouponList_0111"))
    suite.addTest(getDealerCouponList("test_getCouponList_0211"))
    suite.addTest(getDealerCouponList("test_getCouponList_0411"))
    suite.addTest(getDealerCouponList("test_getCouponList_0110"))
    suite.addTest(getDealerCouponList("test_getCouponList_0210"))
    suite.addTest(getDealerCouponList("test_getCouponList_0410"))
    suite.addTest(getDealerCouponList("test_getCouponList_couponStatusNull"))
    suite.addTest(getDealerCouponList("test_getCouponList_couponTypeNull"))
    suite.addTest(getDealerCouponList("test_getCouponList_pageNull"))
    suite.addTest(getDealerCouponList("test_getCouponList_tokenNull"))
    return suite

