#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0034.经销商管理员获取我的丹露终端店审批详情
http://127.0.0.1:8280/mallws/mydl/approval/getApprovalDetail.json
{
    "token":"123",                                          // 必须
    "approvalId":"TAL6646620150102911",                     // 必须 审批id
    "taskId":"123"                                         // 必须 工作流taskId
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                     // 成功 0-成功
        "approvalDetail": {
            "approvalId": "TAL9807720151000463",            // 审批id
            "taskId": "",                                   // 工作流id
			"approvalStatus": "",                           // 审批状态 03-待审核(经销商),04-审核通过,05-审核不通过【03之前的状态经销商看不到】
            "terminalFullName": "s",                        // 终端店全名
            "terminalArea": "辽宁大连市西岗区",             // 终端店地区
            "terminalAddr": "黄浦路977号",                  // 终端店街道
            "terminalContactName": "周先生",                // 终端店联系人
            "terminalContactTel": "15142423615",            // 终端店联系人电话
            "identityCode": null,                           // 身份证号
            "businessLicenseCode": null,                    // 营业执照号
            "terminalLoginName": "yuminglei_8",             // 终端店登陆名
            "registerTel": "",                              // 注册电话
            "email": "",                                    // 邮箱
            "storeType": "烟酒专卖店",                      // 店铺类型
            "emergencyContactPersonName": null,             // 紧急联系人
            "emergencyContactPersonTel": null,              // 紧急联系人电话
            "terminalIdentificationCardUrl": "http://172.16.75.182/upload/2015/10/28/10/52/1446000739776.jpg",  // 负责人身份证扫描件
            "businessLicenseUrl": "http://172.16.75.182/upload/2015/10/28/10/52/1446000746269.jpg",             // 营业执照扫描件
            "taxRegistrationCertificateUrl": "http://172.16.75.182/upload/2015/10/28/10/52/1446000750906.jpg",  // 税务登记证
            "othersCertificateUrl": "http://172.16.75.182/upload/2015/10/28/10/52/1446000758243.jpg"            // 其它证件
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.approval.ApprovalDetailResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
status说明:
"""

class getApprovalDetail(unittest.TestCase):
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

    #获取待审核审批详情
    def test_getApprovalDetail_approvel(self):
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
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.model['approvalDetail']['approvalStatus'],'03')
        self.assertGetDetailSuccess(getApprovalDetail=getDetail)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #获取审核通过审批详情'
    def test_getApprovalDetail_approvelAccept(self):
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
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='0',approvalReason='')
        self.assertEqual(audit.model['success'],'0')
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.model['approvalDetail']['approvalStatus'],'04')
        self.assertGetDetailSuccess(getApprovalDetail=getDetail)
        update('delete from dluser.dl_user where user_account=?',self.UserShop3.username)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        update('delete from dlcompany.dl_biz_base_info where company_name=?',self.UserShop3.fullName)

    #获取审核拒绝审批详情
    def test_getApprovalDetail_approvelRefused(self):
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
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.model['approvalDetail']['approvalStatus'],'05')
        self.assertGetDetailSuccess(getApprovalDetail=getDetail)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #经销商销售员获取待审批详情
    def test_getApprovalDetail_saler(self):
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
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.code,300)
        self.assertEqual(getDetail.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #经销商采购员获取待审批详情
    def test_getApprovalDetail_buyer(self):
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
        ws.login(self.UserShop6.username,self.UserShop6.password)
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.code,300)
        self.assertEqual(getDetail.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #经销商配送员获取待审批详情
    def test_getApprovalDetail_seder(self):
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
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.code,300)
        self.assertEqual(getDetail.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #经销商财务员获取待审批详情
    def test_getApprovalDetail_finer(self):
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
        ws.login(self.UserShop5.username,self.UserShop5.password)
        getDetail=ws.getApprovalDetail(approvalId=approvid,taskId=taskid)
        self.assertEqual(getDetail.code,300)
        self.assertEqual(getDetail.description,'错误的权限!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #approvalId为空
    def test_getApprovalDetail_approvalIdNull(self):
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
        getDetail=ws.getApprovalDetail(approvalId='',taskId=taskid)
        self.assertEqual(getDetail.code,500)
        self.assertEqual(getDetail.description,'服务器异常!')
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #taskId为空(接口可以执行成功)

    def assertGetDetailSuccess(self,getApprovalDetail=None):
        self.assertEqual(getApprovalDetail.model['approvalDetail']['terminalFullName'],self.UserShop3.fullName)
        self.assertEqual(getApprovalDetail.model['approvalDetail']['terminalArea'],self.UserShop3.localProvince+'-'+self.UserShop3.localCity+'-'+self.UserShop3.localCountry)
        self.assertEqual(getApprovalDetail.model['approvalDetail']['terminalAddr'],self.UserShop3.localStreet)
        self.assertEqual(getApprovalDetail.model['approvalDetail']['businessLicenseCode'],self.UserShop3.busLicenseNum)
        self.assertEqual(getApprovalDetail.model['approvalDetail']['terminalLoginName'],self.UserShop3.username)
        self.assertEqual(getApprovalDetail.model['approvalDetail']['registerTel'],self.UserShop3.registerTel)
        self.assertEqual(getApprovalDetail.model['approvalDetail']['storeType'],self.UserShop3.shopType)

    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getApprovalDetail("test_getApprovalDetail_approvel"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_approvelAccept"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_approvelRefused"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_saler"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_buyer"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_seder"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_finer"))
    suite.addTest(getApprovalDetail("test_getApprovalDetail_approvalIdNull"))

    return suite