#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0259.按类型标记消息为已读
接口名称：
	标准JSON接口 http://127.0.0.1:8181/message/markAsReadByType
	JSONP接口 不提供
接口说明：按照类型标记消息为已读
接口参数：
{
    "receiverUserId":"561a843bad834d74a5dcf6a63a358479",
    "receiverCompanyId":"fc0f1b3e41c8466f883c132855cdca4e",
    "type":"T02"
}
接口参数说明：
 	全部必传
接口返回说明：
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}
	遵循WebService规则，外层code 200代表系统成功，其他代表系统异常，内层success 0代表业务执行成功。
"""
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData


class markAsReadByType(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    Merch1 = wsData('Merch1')

    def setUp(self):
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '00DCEE2C6A5942BBA097C3ACFFC47A8A')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '1FAFB941460847F0B96A9FFEA182A28F')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '0001486CC5724CD7A9B1B4AA085B3B69')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '09CCB8DBF42E41E583C9B76423941271')

    # 标记采购订单信息已读
    def test_markAsRead_PurchaseOrder(self):
        ws = webservice()
        unreadPurchaseOrderNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ? and type like ?',self.UserShop.companyId, '01','T02%')
        markAsReadRst = ws.markAsReadByType(receiverUserId=self.UserShop.userId,receiverCompanyId=self.UserShop.companyId, type='T02')
        self.assertEquals(markAsReadRst.code, 200)
        self.assertEqual(markAsReadRst.model['success'], '0')
        for i in range(0,len(unreadPurchaseOrderNum)):
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadPurchaseOrderNum[i]['id'])
            self.assertEquals(readRst[0].read_status,'02')
    # 标记销售订单信息已读
    def test_markAsRead_SellOrder(self):
        ws = webservice()
        unreadSellOrderNum = select( 'select * from dlsms.dl_message where receiver_id = ? and read_status = ?  and type like ?',self.DealMager.userId, '01', 'T02%')
        markAsReadRst = ws.markAsReadByType(receiverUserId=self.DealMager.userId,receiverCompanyId=self.DealMager.companyId, type='T02')
        self.assertEquals(markAsReadRst.code, 200)
        self.assertEqual(markAsReadRst.model['success'], '0')
        for i in range(0, len(unreadSellOrderNum)):
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadSellOrderNum[i]['id'])
            self.assertEquals(readRst[0].read_status, '02')
    # 标记审批审批信息已读
    def test_markAsRead_Approval(self):
        ws = webservice()
        unreadApprovalNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ? and type like ?', self.DealMager.userId, '01','T01%')
        markAsReadRst = ws.markAsReadByType(receiverUserId=self.DealMager.userId,receiverCompanyId=self.DealMager.userId, type='T01')
        self.assertEquals(markAsReadRst.code, 200)
        self.assertEqual(markAsReadRst.model['success'], '0')
        for i in range(0, len(unreadApprovalNum)):
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadApprovalNum[i]['id'])
            self.assertEquals(readRst[0].read_status, '02')
    #标记红包消息
    def test_markAsRead_Coupon(self):
        ws = webservice()
        unreadCouponNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ?  and type like ?',self.UserShop.companyId, '01','T05%')
        markAsReadRst = ws.markAsReadByType(receiverUserId=self.UserShop.userId,receiverCompanyId=self.UserShop.companyId, type='T05')
        self.assertEquals(markAsReadRst.code, 200)
        self.assertEqual(markAsReadRst.model['success'], '0')
        for i in range(0,len(unreadCouponNum)):
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadCouponNum[i]['id'])
            self.assertEquals(readRst[0].read_status,'02')
    # 标记其他消息已读
    def test_markAsRead_Other(self):
        ws = webservice()
        unreadOtherNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ? and type like ?',self.UserShop.companyId, '01','T04%')
        markAsReadRst = ws.markAsReadByType(receiverUserId=self.UserShop.userId,receiverCompanyId=self.UserShop.companyId, type='T05')
        self.assertEquals(markAsReadRst.code, 200)
        self.assertEqual(markAsReadRst.model['success'], '0')
        for i in range(0,len(unreadOtherNum)):
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadOtherNum[i]['id'])
            self.assertEquals(readRst[0].read_status,'02')

    def tearDown(self):
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '00DCEE2C6A5942BBA097C3ACFFC47A8A')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '1FAFB941460847F0B96A9FFEA182A28F')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '0001486CC5724CD7A9B1B4AA085B3B69')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '09CCB8DBF42E41E583C9B76423941271')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(markAsReadByType('test_markAsRead_PurchaseOrder'))
    suite.addTest(markAsReadByType('test_markAsRead_SellOrder'))
    suite.addTest(markAsReadByType('test_markAsRead_Approval'))
    suite.addTest(markAsReadByType('test_markAsRead_Coupon'))
    suite.addTest(markAsReadByType('test_markAsRead_Other'))
    return suite