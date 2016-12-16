#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0260.获取各种类型的最新一种消息
接口名称：
	标准JSON接口 http://127.0.0.1:8181/message/retrieveNewestOneMessage
	JSONP接口 不提供
接口说明：获取各种类型的最新一条消息
接口参数：
{
    "channelId":"CH01",
    "receiverUserId":"561a843bad834d74a5dcf6a63a358479",
    "receiverCompanyId":"fc0f1b3e41c8466f883c132855cdca4e",
    "type":"T0201,T0202,T01"
}
接口参数说明：
 	全部必传，type为逗号分隔的字符串，比如传递T0201,T0202,T01，则查询T0201的最新一条消息和T0202的最新一条消息和T01的最新一条消息返回。
接口返回说明：
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "message": {
            "T0201": "卖家：wwww<br />订单金额178.00元<br />订单号：10441519150437",
            "T01": "目前审批类型未提供文言",
            "T0202": "卖家：wwww<br />订单金额178.00元<br />订单号：10441519150437"
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "com.danlu.dlsms.model.pub.res.MsgNewestOneMessageResponse"
    }
}
	遵循WebService规则，外层code 200代表系统成功，其他代表系统异常，内层success 0代表业务执
"""
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData


class retrieveNewestOneMessage(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    Merch1 = wsData('Merch1')
    #传入类型为空获取消息

    #获取采购订单最新一条消息
    def test_retrieveNewestOneMessage_PurchaseOrder(self):
        PurchaseOrderNews = select_one('select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.UserShop.companyId,'T02%','CH01')
        ws = webservice()
        retrieveNewestOneMessage = ws.retrieveNewestOneMessage(channelId='CH01',receiverUserId=self.UserShop.userId,receiverCompanyId=self.UserShop.companyId,type='T02')
        self.assertEquals(retrieveNewestOneMessage.code, 200)
        self.assertEqual(retrieveNewestOneMessage.model['success'], '0')
        self.assertEqual(retrieveNewestOneMessage.model['message']['T02'], PurchaseOrderNews.content)
    #获取销售订单最新一条消息
    def test_retrieveNewestOneMessage_sellOrder(self):
        sellOrderNews = select_one('select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.DealMager.companyId,'T02%','CH01')
        ws = webservice()
        retrieveNewestOneMessage = ws.retrieveNewestOneMessage(channelId='CH01',receiverUserId=self.DealMager.userId,receiverCompanyId=self.DealMager.companyId,type='T02')
        self.assertEquals(retrieveNewestOneMessage.code, 200)
        self.assertEqual(retrieveNewestOneMessage.model['success'], '0')
        self.assertEqual(retrieveNewestOneMessage.model['message']['T02'], sellOrderNews.content)
    #获取审批最新一条消息
    def test_retrieveNewestOneMessage_Approval(self):
        ApprovalNews = select_one(
            'select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',
            self.DealMager.userId, 'T01%', 'CH01')
        ws = webservice()
        retrieveNewestOneMessage = ws.retrieveNewestOneMessage(channelId='CH01', receiverUserId=self.DealMager.userId,
                                                               receiverCompanyId=self.DealMager.companyId, type='T01')
        self.assertEquals(retrieveNewestOneMessage.code, 200)
        self.assertEqual(retrieveNewestOneMessage.model['success'], '0')
        self.assertEqual(retrieveNewestOneMessage.model['message']['T01'], ApprovalNews.content)
    #获取红包相关最新一条消息
    def test_retrieveNewestOneMessage_Coupon(self):
        CouponNews = select_one( 'select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.UserShop.companyId, 'T05%', 'CH01')
        ws = webservice()
        retrieveNewestOneMessage = ws.retrieveNewestOneMessage(channelId='CH01', receiverUserId=self.UserShop.userId, receiverCompanyId=self.UserShop.companyId, type='T05')
        self.assertEquals(retrieveNewestOneMessage.code, 200)
        self.assertEqual(retrieveNewestOneMessage.model['success'], '0')
        self.assertEqual(retrieveNewestOneMessage.model['message']['T05'], CouponNews.content)
    #终端店获取所有类型最后一条消息(订单、红包)
    def test_retrieveNewestOneMessage_TmlShop(self):
        PurchaseOrderNews = select_one('select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.UserShop.companyId, 'T02%', 'CH01')
        CouponNews = select_one('select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.UserShop.companyId, 'T05%', 'CH01')
        ws = webservice()
        retrieveNewestOneMessage = ws.retrieveNewestOneMessage(channelId='CH01', receiverUserId=self.UserShop.userId,
                                                               receiverCompanyId=self.UserShop.companyId, type='T02,T05')
        self.assertEquals(retrieveNewestOneMessage.code, 200)
        self.assertEqual(retrieveNewestOneMessage.model['success'], '0')
        self.assertEqual(retrieveNewestOneMessage.model['message']['T02'], PurchaseOrderNews.content)
        self.assertEqual(retrieveNewestOneMessage.model['message']['T05'], CouponNews.content)
    #经销商获取所有类型最后一条消息(订单、红包、审批)
    def test_retrieveNewestOneMessage_DealShopMager(self):
        sellOrderNews = select_one( 'select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.DealMager.companyId, 'T02%', 'CH01')
        CouponNews = select_one('select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.DealMager.companyId, 'T05%', 'CH01')
        ApprovalNews = select_one( 'select * from dlsms.dl_message where receiver_id = ? and type like ? and channel_id= ? ORDER BY biz_created_timestamp DESC',self.DealMager.userId, 'T01%', 'CH01')
        ws = webservice()
        retrieveNewestOneMessage = ws.retrieveNewestOneMessage(channelId='CH01', receiverUserId=self.DealMager.userId, receiverCompanyId=self.DealMager.companyId,type='T01,T02,T05')
        self.assertEquals(retrieveNewestOneMessage.code, 200)
        self.assertEqual(retrieveNewestOneMessage.model['success'], '0')
        self.assertEqual(retrieveNewestOneMessage.model['message']['T02'], sellOrderNews.content)
        self.assertEqual(retrieveNewestOneMessage.model['message']['T05'], CouponNews.content)
        self.assertEqual(retrieveNewestOneMessage.model['message']['T01'], ApprovalNews.content)
def suite():
    suite = unittest.TestSuite()
    suite.addTest(retrieveNewestOneMessage('test_retrieveNewestOneMessage_PurchaseOrder'))
    suite.addTest(retrieveNewestOneMessage('test_retrieveNewestOneMessage_sellOrder'))
    suite.addTest(retrieveNewestOneMessage('test_retrieveNewestOneMessage_Approval'))
    suite.addTest(retrieveNewestOneMessage('test_retrieveNewestOneMessage_Coupon'))
    suite.addTest(retrieveNewestOneMessage('test_retrieveNewestOneMessage_TmlShop'))
    suite.addTest(retrieveNewestOneMessage('test_retrieveNewestOneMessage_DealShopMager'))
    return suite