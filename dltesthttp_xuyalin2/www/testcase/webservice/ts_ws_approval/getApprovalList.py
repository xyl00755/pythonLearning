#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0033.经销商管理员获取我的丹露终端店审批列表
http://127.0.0.1:8280/mallws/mydl/approval/getApprovalList.json
{
    "token":"123",              // 必须
    "approvalStatus":"0",       // 必须 审批状态 0-待审批 1-已审批
    "page":"1",                 // 必须 第几页
    "rows":"15"                 // 必须 每页条数
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                             // 成功 0-成功
        "approvalList": [
            {
                "approvalId": "TAL9807720151000463",                // 审批id
                "taskId": "",                                       // 工作流taskId
                "approvalStatus": "2",                              // 审批状态 0-待审批 1-已同意 2-已拒绝
                "terminalLoginName": "s",                    		// 终端店用户名
                "terminalFullName": "s",                            // 终端店名
                "terminalFullAddr": "辽宁大连市西岗区黄浦路977号"   // 终端店全地址
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.approval.ApprovalListResponse"
    }
}

参数校验:
    approvalStatus              @NotNull    @Pattern(regexp = "0|1")
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class getApprovalList(unittest.TestCase):
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

    #正确获取待审批列表（无待审批数据的情况下）
    def test_getApprovalList(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        self.assertEqual(getList.model['success'],'0')
        self.assertEqual(getList.model['approvalList'],[])

    #正确获取待审批列表（有待审批数据的情况下）
    def test_getApprovalList_existApprove(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一条待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        self.assertEqual(getList.model['success'],'0')
        self.assertEqual(getList.model['approvalList'][0]['terminalLoginName'],self.UserShop3.username)
        self.assertEqual(getList.model['approvalList'][0]['terminalFullName'],self.UserShop3.fullName)
        self.assertEqual(getList.model['approvalList'][0]['terminalFullAddr'],self.UserShop3.localProvince+'-'+self.UserShop3.localCity+'-'+self.UserShop3.localCountry+'-'+self.UserShop3.localStreet)
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #正确获取已审批列表（无已审批数据的情况下）
    def test_getApprovalList_notExistRefuse(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一条待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='1',page='1',rows='15')
        self.assertEqual(getList.model['success'],'0')
        self.assertEqual(getList.model['approvalList'],[])
        getList2=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        approvid=getList2.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #正确获取已审批列表（有已审批数据的情况下）
    def test_getApprovalList_existRefuse(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一条待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        getList=ws.getApprovalList(approvalStatus='1',page='1',rows='15')
        self.assertEqual(getList.model['success'],'0')
        self.assertEqual(getList.model['approvalList'][0]['approvalStatus'],'2')
        self.assertEqual(getList.model['approvalList'][0]['terminalLoginName'],self.UserShop3.username)
        self.assertEqual(getList.model['approvalList'][0]['terminalFullName'],self.UserShop3.fullName)
        self.assertEqual(getList.model['approvalList'][0]['terminalFullAddr'],self.UserShop3.localProvince+'-'+self.UserShop3.localCity+'-'+self.UserShop3.localCountry+'-'+self.UserShop3.localStreet)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #销售员角色登录获取待审批列表
    def test_getApprovalList_saler(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        self.assertEqual(getList.code,300)
        self.assertEqual(getList.description,'错误的权限!')

    #采购员角色登录获取待审批列表
    def test_getApprovalList_buyer(self):
        ws=webservice()
        ws.login(self.UserShop6.username,self.UserShop6.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        self.assertEqual(getList.code,300)
        self.assertEqual(getList.description,'错误的权限!')

    #配送员角色登录获取待审批列表
    def test_getApprovalList_seder(self):
        ws=webservice()
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        self.assertEqual(getList.code,300)
        self.assertEqual(getList.description,'错误的权限!')

    #财务员角色登录获取待审批列表
    def test_getApprovalList_finer(self):
        ws=webservice()
        ws.login(self.UserShop5.username,self.UserShop5.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        self.assertEqual(getList.code,300)
        self.assertEqual(getList.description,'错误的权限!')

    #验证翻页是否正常（每页显示一条，第一页有一条数据，第二页则无数据）
    def test_getApprovalList_page(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        #注册一条待审批的数据
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList1=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        self.assertEqual(getList1.model['success'],'0')
        approvid=getList1.model['approvalList'][0]['approvalId']
        self.assertEqual(getList1.model['approvalList'][0]['terminalLoginName'],self.UserShop3.username)
        self.assertEqual(getList1.model['approvalList'][0]['terminalFullName'],self.UserShop3.fullName)
        self.assertEqual(getList1.model['approvalList'][0]['terminalFullAddr'],self.UserShop3.localProvince+'-'+self.UserShop3.localCity+'-'+self.UserShop3.localCountry+'-'+self.UserShop3.localStreet)
        getList2=ws.getApprovalList(approvalStatus='0',page='2',rows='1')
        self.assertEqual(getList2.model['approvalList'],[])
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getApprovalList("test_getApprovalList"))
    suite.addTest(getApprovalList("test_getApprovalList_existApprove"))
    suite.addTest(getApprovalList("test_getApprovalList_existRefuse"))
    suite.addTest(getApprovalList("test_getApprovalList_notExistRefuse"))
    suite.addTest(getApprovalList("test_getApprovalList_saler"))
    suite.addTest(getApprovalList("test_getApprovalList_buyer"))
    suite.addTest(getApprovalList("test_getApprovalList_seder"))
    suite.addTest(getApprovalList("test_getApprovalList_finer"))
    suite.addTest(getApprovalList("test_getApprovalList_page"))

    return suite


