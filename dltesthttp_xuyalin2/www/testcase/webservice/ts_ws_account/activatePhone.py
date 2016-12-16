#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0291.激活手机
http://127.0.0.1:8280/mallws/mydl/account/activatePhone.json
{
	"token":"123",
    "userAcct":"testliqi",
	"userId":"2724e8f7e4da4301af2367b6ff7dd336",            // userId
	"conditionInd":"0",                                     // 0-不满足参与活动条件 1-满足条件参与激活送红包活动
	"tel":"13800138000"
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                      // 0-激活成功 1-激活失败 2-手机号已在其他地方被激活 5-其他错误
	    "couponInd":"0",                                     // 0-无红包 1-有红包
		"couponAmt":"1000"                                   // 红包金额(现在是固定值)

    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.account.ActivatePhoneResponse"
    }
}

"""
class activatePhone(unittest.TestCase):
    UserShop2=wsData('TmlShop2')
    UserShop1=wsData('TmlShop')

    #正常激活手机号(无送红包活动)
    def test_activatePhone_noCoupon(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd='0',tel=self.UserShop2.mobileNumber)
        self.assertEqual(activatePhoneNum.model['success'],'0')
        self.assertEqual(activatePhoneNum.model['couponInd'],'0')
        self.assertEqual(activatePhoneNum.model['couponAmt'],'')
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #正常激活手机号(有送红包活动)
    def test_activatePhone_coupon(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=1,tel=self.UserShop2.mobileNumber)
        self.assertEqual(activatePhoneNum.model['success'],'0')
        self.assertEqual(activatePhoneNum.model['couponInd'],'1')
        self.assertEqual(activatePhoneNum.model['couponAmt'],'1000')
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #手机号格式不正确（长度）
    def test_activatePhone_telLong(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel='185498556874589')
        self.assertEqual(activatePhoneNum.model['success'],'1')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #手机号格式不正确（不存在的号段）错误 #5704
    def test_activatePhone_telStyle(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel='22345678912')
        self.assertEqual(activatePhoneNum.model['success'],'1')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #其他用户已经激活的手机号
    def test_activatePhone_otherActivate(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel=self.UserShop1.mobileNumber)
        self.assertEqual(activatePhoneNum.model['success'],'2')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #其他用户未激活的手机号
    def test_activatePhone_otherNoActivate(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop1.username,userId=self.UserShop1.userId,conditionInd=0,tel=self.UserShop2.mobileNumber)
        self.assertEqual(activatePhoneNum.model['success'],'2')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop1.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop1.userId,userAcct=self.UserShop1.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #手机号处于待审批当中(错误 #5696)（待审批账号：testsun456789 密码：123456 手机号：18349200236）
    def test_activatePhone_otherApprove(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel='18349200236')
        self.assertEqual(activatePhoneNum.model['success'],'2')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #手机号处于审批已拒绝(错误 #5696)（待审批账号：testsun456789 密码：123456 手机号：18349200236）
    def test_activatePhone_otherApproveRefused(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','05','testsun456789')
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel='18349200236')
        self.assertEqual(activatePhoneNum.model['success'],'2')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])


    #手机号重复激活
    def test_activatePhone_repeat(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel=self.UserShop2.mobileNumber)
        self.assertEqual(activatePhoneNum.model['success'],'0')
        self.assertEqual(activatePhoneNum.model['couponInd'],'0')
        self.assertEqual(activatePhoneNum.model['couponAmt'],'')
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])
        activatePhoneNumRepeat=ws.activatePhone(userAcct=self.UserShop2.username,userId=self.UserShop2.userId,conditionInd=0,tel=self.UserShop2.mobileNumber)
        self.assertEqual(activatePhoneNumRepeat.model['success'],'2')
        self.assertEqual(activatePhoneNumRepeat.model['couponInd'],None)
        self.assertEqual(activatePhoneNumRepeat.model['couponAmt'],None)
        update('update dluser.dl_user set user_phone_status =? where user_id=?','1',self.UserShop2.userId)

    #userAccount与userID不一致
    def test_activatePhone_inconsistent(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId='123456789',conditionInd=0,tel=self.UserShop2.mobileNumber)
        self.assertEqual(activatePhoneNum.model['success'],'5')
        self.assertEqual(activatePhoneNum.model['couponInd'],None)
        self.assertEqual(activatePhoneNum.model['couponAmt'],None)
        telStatusSql=select_one('select user_phone_status from dluser.dl_user where user_id=?',self.UserShop2.userId)
        telStatus=ws.getAcctInfo(userId=self.UserShop2.userId,userAcct=self.UserShop2.username)
        self.assertEqual(str(telStatusSql.user_phone_status),telStatus.model['telStatus'])

    #token值错误
    def test_activatePhone_tokenError(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId='123456789',conditionInd=0,tel=self.UserShop2.mobileNumber,token='123456789')
        self.assertEqual(activatePhoneNum.model,None)
        self.assertEqual(activatePhoneNum.code,100)

    #无token
    def test_activatePhone_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        activatePhoneNum=ws.activatePhone(userAcct=self.UserShop2.username,userId='123456789',conditionInd=0,tel=self.UserShop2.mobileNumber,token='null')
        self.assertEqual(activatePhoneNum.model,None)
        self.assertEqual(activatePhoneNum.code,600)



    def tearDown(self):
        update('update dluser.dl_user set user_phone_status =? where user_id=?','1',self.UserShop2.userId)
        update('update dlworkflow.dl_apply_terminal set flow_status=? where terminal_user_name=?','02','testsun456789')

def suite():
    suite=unittest.TestSuite()

    suite.addTest(activatePhone("test_activatePhone_noCoupon"))
    suite.addTest(activatePhone("test_activatePhone_coupon"))
    suite.addTest(activatePhone("test_activatePhone_telLong"))
    suite.addTest(activatePhone("test_activatePhone_telStyle"))
    suite.addTest(activatePhone("test_activatePhone_otherActivate"))
    suite.addTest(activatePhone("test_activatePhone_otherNoActivate"))
    suite.addTest(activatePhone("test_activatePhone_otherApprove"))
    suite.addTest(activatePhone("test_activatePhone_otherApproveRefused"))
    suite.addTest(activatePhone("test_activatePhone_repeat"))
    suite.addTest(activatePhone("test_activatePhone_inconsistent"))
    suite.addTest(activatePhone("test_activatePhone_tokenError"))
    suite.addTest(activatePhone("test_activatePhone_tokenNull"))

    return suite