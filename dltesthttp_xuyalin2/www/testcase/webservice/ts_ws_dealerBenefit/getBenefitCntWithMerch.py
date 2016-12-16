#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData

"""
LB04.商品详情：可领优惠券个数(与商品绑定)
http://127.0.0.1:8280/mallws/dealerBenefit/getCouponCntWithMerch.json
{
	"token":"123",
    "merchId":"67d4cb03595348cdacd61000bc96ba03"                   // 必须 商品ID
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                            // 0-成功 1-失败
		"activityCnt": "3"                                         // 可领优惠券个数
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.dealerBenefit.GetBenefitCntWithMerchResponse"
    }
}
"""

class getBenefitCntWithMerch(unittest.TestCase):
    UserShop=wsData('TmlShop')
    Merch=wsData('Merch1')

    #商品详情页正确获取可领优惠券个数
    def test_getBenefitCntWithMerch(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getBenifit=ws.getBenefitCntWithMerch(merchId=self.Merch.goodsId)
        self.assertEqual(getBenifit.model['success'],'0')
        self.assertNotEqual(getBenifit.model['activityCnt'],'')

    #merchId为空
    def test_getBenefitCntWithMerch_merchIdNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getBenifit=ws.getBenefitCntWithMerch(merchId='')
        self.assertEqual(getBenifit.model['success'],'1')
        self.assertEqual(getBenifit.model['activityCnt'],None)

    #merchId不存在
    def test_getBenefitCntWithMerch_merchIdNotExist(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getBenifit=ws.getBenefitCntWithMerch(merchId='1234567890')
        self.assertEqual(getBenifit.model['success'],'0')
        self.assertEqual(getBenifit.model['activityCnt'],'0')

    #商品已下架
    def test_getBenefitCntWithMerch_goodsUnder(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','02',self.Merch.goodsId)
        getBenifit=ws.getBenefitCntWithMerch(merchId=self.Merch.goodsId)
        self.assertEqual(getBenifit.model['success'],'0')
        # self.assertEqual(getBenifit.model['activityCnt'],'0')
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch.goodsId)

    #无token值
    def test_getBenefitCntWithMerch_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getBenifit=ws.getBenefitCntWithMerch(merchId=self.Merch.goodsId,token='null')
        self.assertEqual(getBenifit.code,600)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getBenefitCntWithMerch("test_getBenefitCntWithMerch"))
    suite.addTest(getBenefitCntWithMerch("test_getBenefitCntWithMerch_merchIdNull"))
    suite.addTest(getBenefitCntWithMerch("test_getBenefitCntWithMerch_merchIdNotExist"))
    suite.addTest(getBenefitCntWithMerch("test_getBenefitCntWithMerch_goodsUnder"))
    suite.addTest(getBenefitCntWithMerch("test_getBenefitCntWithMerch_tokenNull"))
    return suite