#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0256.消息数量
接口名称：
	标准JSON接口 http://127.0.0.1:8181/message/count
	JSONP接口 http://127.0.0.1:8181/p/message/count
接口说明：查询用户的消息数量，包括全部数量和未读数量
接口参数：
{
    "channelId":"CH01",
    "receiverUserId":"e9ba06042b97458bb8cfdb6873c30e2a",
    "receiverCompanyId":"e9ba06042b97458bb8cfdb6873asdfd"
}
接口参数说明：
 	全部必传，channelId 参考常量 com.danlu.dlsms.constant.MsgCommonConst.MsgChannel
接口返回说明：
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "msgCount": {
            "unreadCount": {
                "T0201": 0,
                "T01": 0,
                "T03,T04": 0,
                "T0202": 0
            },
            "allCount": {
                "T0201": 0,
                "T01": 0,
                "T03,T04": 0,
                "T0202": 0
            },
            "extensionCount": {
                "iRisedCount": 0,
                "hasCheckedCount": 0
            }
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "com.danlu.dlsms.model.pub.res.MsgCountResponse"
    }
}
	遵循WebService规则，外层code 200代表系统成功，其他代表系统异常，内层success 0代表业务执行成功。
	返回两个Map，Key为消息的类型，value为对应的数量，如果不存在相应的键值对则认为没有此类型的消息。消息类型参考常量 com.danlu.dlsms.constant.MsgTypeConst
"""

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import wsData


class count(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    Merch1 = wsData('Merch1')

    # S1.获取终端店消息数量(包括全部数量和未读数量)
    def test_count_NumberTmlShop(self):
        ws = webservice()
        msgRstAllCount = select('select * from dlsms.dl_message  where receiver_id = ?  and channel_id = ?',self.UserShop.companyId,'CH01')
        msgRstUnreadCount = select('select * from dlsms.dl_message  where receiver_id = ? and read_status = ? and channel_id = ?' , self.UserShop.companyId,'01','CH01')

        msgCount = ws.messageCount(receiverUserId = self.UserShop.userId, receiverCompanyId=self.UserShop.companyId)
        allcount = msgCount.model['msgCount']['allCount']
        unreadCount = msgCount.model['msgCount']['unreadCount']
        allcountnum = 0
        unreadnum = 0
        for key,value in allcount.items():
            if (len(key) == 3 or ',' in key):
                allcountnum = allcountnum+value

        for key,value in unreadCount.items():
            if (len(key) == 3 or ',' in key):
                unreadnum = unreadnum+value
        self.assertEquals(msgCount.code, 200)
        self.assertEqual(msgCount.model['success'], '0')
        self.assertEqual(allcountnum, len(msgRstAllCount))
        self.assertEqual(unreadnum , len(msgRstUnreadCount))
    # 获取经销商消息数量(包括全部数量和未读数量)
    def test_count_NumberDealShop(self):
        ws = webservice()
        PartCount = select('select * from dlsms.dl_message  where receiver_id = ?  and channel_id = ?',self.DealMager.companyId, 'CH01')
        ApprovalCount = select('select * from dlsms.dl_message  where receiver_id = ?  and channel_id = ?',self.DealMager.userId, 'CH01')
        msgRstUnreadCount = select( 'select * from dlsms.dl_message  where receiver_id = ? and read_status = ? and channel_id = ?',self.DealMager.companyId, '01', 'CH01')
        ApprovalUnread = select( 'select * from dlsms.dl_message  where receiver_id = ? and read_status = ? and channel_id = ?',self.DealMager.userId, '01', 'CH01')
        msgCount = ws.messageCount(receiverUserId=self.DealMager.userId, receiverCompanyId=self.DealMager.companyId)
        allcount = msgCount.model['msgCount']['allCount']
        unreadCount = msgCount.model['msgCount']['unreadCount']
        allcountnum = 0
        unreadnum = 0
        for key, value in allcount.items():
            if (len(key) == 3 or ',' in key):
                allcountnum = allcountnum + value

        for key, value in unreadCount.items():
            if (len(key) == 3 or ',' in key):
                unreadnum = unreadnum + value
        self.assertEquals(msgCount.code, 200)
        self.assertEqual(msgCount.model['success'], '0')
        self.assertEqual(allcountnum, len(PartCount )+len(ApprovalCount))
        self.assertEqual(unreadnum, len(msgRstUnreadCount)+len(ApprovalUnread))
def suite():
    suite = unittest.TestSuite()
    suite.addTest(count("test_count_NumberTmlShop"))
    suite.addTest(count("test_count_NumberDealShop"))
    return suite