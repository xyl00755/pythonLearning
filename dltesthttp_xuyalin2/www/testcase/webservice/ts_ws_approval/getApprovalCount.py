#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0032.经销商管理员获取我的丹露终端店审批数量
http://127.0.0.1:8280/mallws/mydl/approval/getApprovalCount.json
{
    "token":"123"                   // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                 // 成功 0-成功
        "pendingApprovalCount": "0",    // 待审批数量
        "acceptApprovalCount": "0",     // 已通过数量
        "refusedApprovalCount": "0"     // 已拒绝数量
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.approval.ApprovalCountResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    已审批数量 = 已通过数量 + 已拒绝数量
"""

class getApprovalCount(unittest.TestCase):
    UserShop=wsData('DealMager')
    #经销商销售员
    UserShop2=wsData('DealSaler')
    #经销商采购员
    UserShop6=wsData('DealBuyer')
    #经销商配送员
    UserShop4=wsData('DealSeder')
    #经销商财务员
    UserShop5=wsData('DealFiner')

    UserShop3 = wsData('RegistTmlShop')

    def setUp(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)


    #正确获取审批数量(无审批数据情况下)
    def test_getApprovalCount_no(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.model['success'],'0')
        self.assertEqual(getCount.model['pendingApprovalCount'],'0')
        self.assertEqual(getCount.model['acceptApprovalCount'],'0')
        self.assertEqual(getCount.model['refusedApprovalCount'],'0')

    #正确获取审批数量（有待审批数据情况下）
    def test_getApprovalCount_one(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一个待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.model['success'],'0')
        self.assertEqual(getCount.model['pendingApprovalCount'],'1')
        self.assertEqual(getCount.model['acceptApprovalCount'],'0')
        self.assertEqual(getCount.model['refusedApprovalCount'],'0')
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #正确获取审批数量（有审批通过的数据情况下）
    def test_getApprovalCount_accept(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一个待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='0',approvalReason='')
        self.assertEqual(audit.model['success'],'0')
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.model['success'],'0')
        self.assertEqual(getCount.model['pendingApprovalCount'],'0')
        self.assertEqual(getCount.model['acceptApprovalCount'],'1')
        self.assertEqual(getCount.model['refusedApprovalCount'],'0')
        update('delete from dluser.dl_user where user_account=?',self.UserShop3.username)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        update('delete from dlcompany.dl_biz_base_info where company_name=?',self.UserShop3.fullName)

    #正确获取审批数量（有审批拒绝的数据情况下）错误 #6026
    def test_getApprovalCount_refuse(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一个待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功')
        self.assertEqual(audit.model['success'],'0')
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.model['success'],'0')
        self.assertEqual(getCount.model['pendingApprovalCount'],'0')
        self.assertEqual(getCount.model['acceptApprovalCount'],'0')
        self.assertEqual(getCount.model['refusedApprovalCount'],'1')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #销售员角色登录获取审批数量
    def test_getApprovalCount_saler(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.code,300)
        self.assertEqual(getCount.description,'错误的权限!')

    #采购员角色登录获取审批数量
    def test_getApprovalCount_buyer(self):
        ws=webservice()
        ws.login(self.UserShop6.username,self.UserShop6.password)
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.code,300)
        self.assertEqual(getCount.description,'错误的权限!')

    #配送员角色登录获取审批数量
    def test_getApprovalCount_seder(self):
        ws=webservice()
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.code,300)
        self.assertEqual(getCount.description,'错误的权限!')

    #财务员角色登录获取审批数量
    def test_getApprovalCount_finer(self):
        ws=webservice()
        ws.login(self.UserShop5.username,self.UserShop5.password)
        getCount=ws.getApprovalCount()
        self.assertEqual(getCount.code,300)
        self.assertEqual(getCount.description,'错误的权限!')

    #token为空
    def test_getApprovalCount_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getCount=ws.getApprovalCount(token='')
        self.assertEqual(getCount.code,100)
        self.assertEqual(getCount.description,'token验证失败，请重新登录!')

    #token不存在
    def test_getApprovalCount_tokenNotExist(self):
        ws=webservice()
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getCount=ws.getApprovalCount(token='null')
        self.assertEqual(getCount.code,600)
        self.assertEqual(getCount.description,'请重新登陆')

    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getApprovalCount("test_getApprovalCount_no"))
    suite.addTest(getApprovalCount("test_getApprovalCount_one"))
    suite.addTest(getApprovalCount("test_getApprovalCount_accept"))
    #suite.addTest(getApprovalCount("test_getApprovalCount_refuse"))
    suite.addTest(getApprovalCount("test_getApprovalCount_saler"))
    suite.addTest(getApprovalCount("test_getApprovalCount_buyer"))
    suite.addTest(getApprovalCount("test_getApprovalCount_seder"))
    suite.addTest(getApprovalCount("test_getApprovalCount_finer"))
    suite.addTest(getApprovalCount("test_getApprovalCount_tokenNull"))
    suite.addTest(getApprovalCount("test_getApprovalCount_tokenNotExist"))
    return suite
