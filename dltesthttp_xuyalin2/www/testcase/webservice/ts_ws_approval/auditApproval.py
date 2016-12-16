#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0035.经销商管理员我的丹露审批
http://127.0.0.1:8280/mallws/mydl/approval/auditApproval.json
{
    "token":"123",                      // 必须
    "approvalId":"TAL9604920150102796", // 必须 审批id
    "taskId":"123",                     // 必须 工作流id
    "auditStatus":"1",                  // 必须 审批状态 0 同意 1 拒绝
    "approvalReason":"123123"           // 必须 审批理由
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                      // 0-成功 1-重复审批
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    /// 必须验证
    auditStatus             @NotNull    @Pattern(regexp = "0|1")
    approvalReason          @NotNull    @Size(min = 2, max = 300)
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
param说明:
    taskId为工作流id 列表接口中未审批的单子有这个id 已审批的单子没有 但是详情页面必须把taskId带过来 如果是已审批的单子 传递一个空字符串
"""

class auditApproval(unittest.TestCase):
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

    #正确审批同意
    def test_auditApproval_accept(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
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
        selectSql=select_int('select count(*) from dluser.dl_user where user_account=?',self.UserShop3.username)
        self.assertEqual(selectSql,1)
        update('delete from dluser.dl_user where user_account=?',self.UserShop3.username)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        update('delete from dlcompany.dl_biz_base_info where company_name=?',self.UserShop3.fullName)

    #正确审批拒绝
    def test_auditApproval_refuse(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
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
        selectSql=select_int('select count(*) from dluser.dl_user where user_account=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)
        selectSql2=select_one('select * from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        self.assertEqual(selectSql2.flow_status,'05')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #经销商销售员审批
    def test_auditApproval_saler(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        ws.login(self.UserShop2.username,self.UserShop2.password)
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.code,300)
        self.assertEqual(audit.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #经销商采购员审批
    def test_auditApproval_buyer(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        ws.login(self.UserShop6.username,self.UserShop6.password)
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.code,300)
        self.assertEqual(audit.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #经销商配送员审批
    def test_auditApproval_seder(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        ws.login(self.UserShop4.username,self.UserShop4.password)
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.code,300)
        self.assertEqual(audit.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #经销商财务员审批
    def test_auditApproval_finer(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='15')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        ws.login(self.UserShop5.username,self.UserShop5.password)
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.code,300)
        self.assertEqual(audit.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #重复审批
    def test_auditApproval_repeat(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
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
        selectSql=select_int('select count(*) from dluser.dl_user where user_account=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)
        selectSql2=select_one('select * from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        self.assertEqual(selectSql2.flow_status,'05')
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'1')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #approvalId为空
    def test_auditApproval_approvalIdNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId='',taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.code,500)
        self.assertEqual(audit.description,'服务器异常!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #审批理由位数等于2
    def test_auditApproval_reasonMin(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝')
        self.assertEqual(audit.model['success'],'0')
        selectSql=select_int('select count(*) from dluser.dl_user where user_account=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)
        selectSql2=select_one('select * from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        self.assertEqual(selectSql2.flow_status,'05')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #审批理由位数小于2

    #审批理由大于30

    #审批理由为空（拒绝审批理由为空也可以审批通过）
    def test_auditApproval_reasonNull(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='')
        self.assertEqual(audit.model['success'],'0')
        selectSql=select_int('select count(*) from dluser.dl_user where user_account=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)
        selectSql2=select_one('select * from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        self.assertEqual(selectSql2.flow_status,'05')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #审批理由等于30
    def test_auditApproval_reasonMax(self):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝')
        self.assertEqual(audit.model['success'],'0')
        selectSql=select_int('select count(*) from dluser.dl_user where user_account=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)
        selectSql2=select_one('select * from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        self.assertEqual(selectSql2.flow_status,'05')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(auditApproval("test_auditApproval_accept"))
    suite.addTest(auditApproval("test_auditApproval_refuse"))
    suite.addTest(auditApproval("test_auditApproval_saler"))
    suite.addTest(auditApproval("test_auditApproval_buyer"))
    suite.addTest(auditApproval("test_auditApproval_seder"))
    suite.addTest(auditApproval("test_auditApproval_finer"))
    suite.addTest(auditApproval("test_auditApproval_repeat"))
    suite.addTest(auditApproval("test_auditApproval_approvalIdNull"))
    suite.addTest(auditApproval("test_auditApproval_reasonMin"))
    suite.addTest(auditApproval("test_auditApproval_reasonNull"))
    suite.addTest(auditApproval("test_auditApproval_reasonMax"))
    return suite