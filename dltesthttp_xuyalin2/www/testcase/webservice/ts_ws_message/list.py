#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
0257.消息列表
接口名称：
	标准JSON接口 http://127.0.0.1:8181/message/list
	JSONP接口 http://127.0.0.1:8181/p/message/list
接口说明：查询用户对应类型的消息列表
接口参数：
{
    "id":"",
    "channelId":"CH01",
    "receiverUserId":"561a843bad834d74a5dcf6a63a358479",
    "receiverCompanyId":"fc0f1b3e41c8466f883c132855cdca4e",
    "type":"T02",
    "defaultPaginationStrategy":false,
    "page":1,
    "rows":15
}
接口参数说明：
 	id可选，其他必传。type消息类型实现树形结构，可以传递非叶子节点，defaultPaginationStrategy 为true使用默认的分页策略，此时忽略 page 和 rows，否则使用 page 和 rows 分页。
接口返回说明：
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "messageList": [
            {
                "id": "903B121AEF164FFAPELB6152O96eF4E1",
                "originalMessageId": "49421F44A1064C38A3C994D6DD98F1FF",
                "receiverId": "fc0f1b3e41c8466f883c132855cdca4e",
                "type": "T020101",
                "channelId": "CH01",
                "content": "您取消订单【10000022223333（金额：10000元）】的请求卖家已拒绝，若有疑问可直接联系卖家。跳转到订单跟踪页面。",
                "templateLink": "/index",
                "sendResult": "02",
                "readStatus": "02",
                "businessKey": "10441519150437",
                "bizCreatedTimestamp": "2016-03-17 15:20:06",
                "sendDatetime": "2016-03-17 15:20:45",
                "expireDatetime": "2016-03-24 15:20:45",
                "orderMessageModel": {
                    "orderId": "11774d56885047c3843ea7562edac678",
                    "orderNo": "10441519150437",
                    "payType": "2",
                    "payNo": "90441519150438",
                    "goodsModelList": [
                        {
                            "name": "金六福 eeee4444",
                            "number": "1箱",
                            "goodsPic": "//asset.danlu.com/upload/goods/2016/2/22/bfd00ed2d3578b081df8fcd2ef96aaaa.jpg"
                        }
                    ]
                },
                "approvalMessageModel": null
            },
            {
                "id": "903B121AEF164SFfPELB6152O968F4E2",
                "originalMessageId": "49421F44A1064C38A3C994D6DD98F1FF",
                "receiverId": "fc0f1b3e41c8466f883c132855cdca4e",
                "type": "T020204",
                "channelId": "CH01",
                "content": "订单【10000022223333（金额：10000元）】支付金额异常，已被冻结，请联系丹露处理。跳转到订单跟踪页面。",
                "templateLink": "/index",
                "sendResult": "02",
                "readStatus": "02",
                "businessKey": "10441519150437",
                "bizCreatedTimestamp": "2016-03-17 15:20:06",
                "sendDatetime": "2016-03-17 15:20:45",
                "expireDatetime": "2016-03-24 15:20:45",
                "orderMessageModel": {
                    "orderId": "11774d56885047c3843ea7562edac678",
                    "orderNo": "10441519150437",
                    "payType": "2",
                    "payNo": "90441519150438",
                    "goodsModelList": [
                        {
                            "name": "金六福 eeee4444",
                            "number": "1箱",
                            "goodsPic": "//asset.danlu.com/upload/goods/2016/2/22/bfd00ed2d3578b081df8fcd2ef96aaaa.jpg"
                        }
                    ]
                },
                "approvalMessageModel": null
            }
        ],
        "resultCount": 0,
        "pageCount": 0,
        "currentPage": 1
    },
    "metadata": {
        "type": 0,
        "clazz": "com.danlu.dlsms.model.pub.res.MessageListResponse"
    }
}
	遵循WebService规则，外层code 200代表系统成功，其他代表系统异常，内层success 0代表业务执行成功。
	当前系统中，如果消息类型为订单类型，则 orderMessageMode 有值，如果为终端店注册类型，则 approvalMessageModel 有值。
"""
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData


class list(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    Merch1 = wsData('Merch1')

    #读取销售订单相关信息(不使用分页)
    def test_read_sellOrderNopage(self):
        ws = webservice()
        sellOrderNum = select('select * from dlsms.dl_message  where receiver_id = ? and type like ? and channel_id = ?',self.DealMager.companyId, 'T02%', 'CH01')
        sellOrder = ws.list(channelId='CH01',receiverUserId=self.DealMager.userId,receiverCompanyId=self.DealMager.companyId,type='T02',defaultPaginationStrategy='false',page='1',rows='900000')
        self.assertEquals(sellOrder.code, 200)
        self.assertEqual(sellOrder.model['success'], '0')
        self.assertEqual(len(sellOrder.model['messageList']),len(sellOrderNum))
    #读取销售订单相关信息(使用分页)
    def test_read_sellOrderPage(self):
        ws = webservice()
        sellOrderNum = select( 'select * from dlsms.dl_message  where receiver_id = ? and type like ? and channel_id = ?',self.DealMager.companyId, 'T02%', 'CH01')
        sellOrder = ws.list(channelId='CH01', receiverUserId=self.DealMager.userId,receiverCompanyId=self.DealMager.companyId, type='T02', defaultPaginationStrategy='true', page=None, rows=None)
        self.assertEquals(sellOrder.code, 200)
        self.assertEqual(sellOrder.model['success'], '0')
        self.assertEqual(len(sellOrder.model['messageList']), 15)
    #读取审批消息
    def test_read_Approval(self):
        ws = webservice()
        ApprovalNum = select(
            'select * from dlsms.dl_message  where receiver_id = ? and type like ? and channel_id = ?',
            self.DealMager.userId, 'T01%', 'CH01')
        Approval = ws.list(channelId='CH01', receiverUserId=self.DealMager.userId, receiverCompanyId=self.DealMager.userId, type='T01', defaultPaginationStrategy='false',page='1', rows='900000')
        self.assertEquals(Approval.code, 200)
        self.assertEqual(Approval.model['success'], '0')
        self.assertEqual(len(Approval.model['messageList']), len(ApprovalNum))
    #读取采购订单消息
    def test_read_PurchaseOrder(self):
        ws = webservice()
        PurchaseOrderNum = select('select * from dlsms.dl_message  where receiver_id = ? and type like ? and channel_id = ?',self.UserShop.companyId, 'T02%', 'CH01')
        PurchaseOrder = ws.list(channelId='CH01',receiverUserId=self.UserShop.userId,receiverCompanyId=self.UserShop.companyId,type='T02',defaultPaginationStrategy='false',page='1',rows='900000')
        self.assertEquals(PurchaseOrder.code, 200)
        self.assertEqual(PurchaseOrder.model['success'], '0')
        self.assertEqual(len(PurchaseOrder.model['messageList']),len(PurchaseOrderNum ))
    #读取红包类型消息
    def test_read_CouponMessage(self):
        ws = webservice()
        CouponMessageNum = select('select * from dlsms.dl_message  where receiver_id = ? and type like ? and channel_id = ?',self.UserShop.companyId, 'T05%', 'CH01')
        CouponMessage = ws.list(channelId='CH01',receiverUserId=self.UserShop.userId,receiverCompanyId=self.UserShop.companyId,type='T05',defaultPaginationStrategy='false',page='1',rows='900000')
        self.assertEquals(CouponMessage.code, 200)
        self.assertEqual(CouponMessage.model['success'], '0')
        self.assertEqual(len(CouponMessage.model['messageList']),len(CouponMessageNum))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(list('test_read_sellOrderNopage'))
    suite.addTest(list('test_read_sellOrderPage'))
    suite.addTest(list('test_read_Approval'))
    suite.addTest(list('test_read_PurchaseOrder'))
    suite.addTest(list('test_read_CouponMessage'))
    return suite


