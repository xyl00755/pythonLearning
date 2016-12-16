#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0258.标记消息为已读
接口名称：
	标准JSON接口 http://127.0.0.1:8181/message/markAsRead
	JSONP接口 http://127.0.0.1:8181/p/message/markAsRead
接口说明：标记消息为已读
接口参数：
{
    "msgIds":" e9ba06042b97458bb8cfdb6873c30e2a "
}
接口参数说明：
 	msgIds 为逗号分隔的字符串，必传。
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


class markAsRead(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    Merch1 = wsData('Merch1')

    def setUp(self):
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '00DCEE2C6A5942BBA097C3ACFFC47A8A')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '1FAFB941460847F0B96A9FFEA182A28F')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '0001486CC5724CD7A9B1B4AA085B3B69')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '09CCB8DBF42E41E583C9B76423941271')

    #标记采购订单信息已读
    def test_markAsRead_PurchaseOrder(self):
        ws = webservice()
        unreadPurchaseOrderNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ? and type like ?',self.UserShop.companyId, '01','T02%')
        for i in range(0,len(unreadPurchaseOrderNum)):
            markAsReadRst= ws.markAsRead(msgIds=unreadPurchaseOrderNum[i]['id'])
            self.assertEquals(markAsReadRst.code, 200)
            self.assertEqual(markAsReadRst.model['success'], '0')
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadPurchaseOrderNum[i]['id'])
            self.assertEquals(readRst[0].read_status,'02')
    #标记销售订单信息已读
    def test_markAsRead_SellOrder(self):
         ws = webservice()
         unreadSellOrderNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ?  and type like ?',self.DealMager.companyId, '01','T02%')
         for i in range(0, len(unreadSellOrderNum)):
             markAsReadRst = ws.markAsRead(msgIds=unreadSellOrderNum[i]['id'])
             self.assertEquals(markAsReadRst.code, 200)
             self.assertEqual(markAsReadRst.model['success'], '0')
             readRst = select('select * from dlsms.dl_message  where id = ? ', unreadSellOrderNum[i]['id'])
             self.assertEquals(readRst[0].read_status, '02')
    #标记审批审批信息已读
    def test_markAsRead_Approval(self):
        ws = webservice()
        unreadApprovalNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ? and type like ?',
                                    self.DealMager.userId, '01','T01%')
        for i in range(0, len(unreadApprovalNum)):
            markAsReadRst = ws.markAsRead(msgIds=unreadApprovalNum[i]['id'])
            self.assertEquals(markAsReadRst.code, 200)
            self.assertEqual(markAsReadRst.model['success'], '0')
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadApprovalNum[i]['id'])
            self.assertEquals(readRst[0].read_status, '02')
    #标记红包消息已读
    def test_markAsRead_Coupon(self):
        ws = webservice()
        unreadCouponNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ?  and type like ?',self.UserShop.companyId, '01','T05%')
        for i in range(0,len(unreadCouponNum)):
            markAsReadRst= ws.markAsRead(msgIds=unreadCouponNum[i]['id'])
            self.assertEquals(markAsReadRst.code, 200)
            self.assertEqual(markAsReadRst.model['success'], '0')
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadCouponNum[i]['id'])
            self.assertEquals(readRst[0].read_status,'02')
    #标记其他消息已读
    def test_markAsRead_Other(self):
        ws = webservice()
        unreadOtherNum = select('select * from dlsms.dl_message where receiver_id = ? and read_status = ? and type like ?',self.UserShop.companyId, '01','T04%')
        for i in range(0,len(unreadOtherNum)):
            markAsReadRst= ws.markAsRead(msgIds=unreadOtherNum[i]['id'])
            self.assertEquals(markAsReadRst.code, 200)
            self.assertEqual(markAsReadRst.model['success'], '0')
            readRst = select('select * from dlsms.dl_message  where id = ? ', unreadOtherNum[i]['id'])
            self.assertEquals(readRst[0].read_status,'02')


    def tearDown(self):
        update('update dlsms.dl_message set read_status = ? where id = ? ','01', '00DCEE2C6A5942BBA097C3ACFFC47A8A')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '1FAFB941460847F0B96A9FFEA182A28F')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '0001486CC5724CD7A9B1B4AA085B3B69')
        update('update dlsms.dl_message set read_status = ? where id = ? ', '01', '09CCB8DBF42E41E583C9B76423941271')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(markAsRead('test_markAsRead_PurchaseOrder'))
    suite.addTest(markAsRead('test_markAsRead_SellOrder'))
    suite.addTest(markAsRead('test_markAsRead_Approval'))
    suite.addTest(markAsRead('test_markAsRead_Coupon'))
    suite.addTest(markAsRead('test_markAsRead_Other'))
    return suite