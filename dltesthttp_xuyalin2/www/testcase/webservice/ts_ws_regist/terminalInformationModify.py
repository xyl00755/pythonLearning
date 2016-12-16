#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
2.终端店注册资料修改再注册
http://127.0.0.1:8080/mallws/regist/terminalInformationModify.json
{
    "applyId":"1231231414",                                         //必须 注册号
    "terminalName":"高健的终端店",                                  //必须 终端店名称(检测)
    "businessLicenseCode":"111111",                                 //必须 营业执照号码
    "terminalTypeCode":"S011",                                      //必须 商业超市
                                                                    // 1.烟酒专卖店  S011
                                                                    // 2.便利店      S012
                                                                    // 3.餐饮店      S013
                                                                    // 4.商业超市    S014
                                                                    // 5.其他        S015
    "terminalAreaCode":"CHNP007C056D0594",                          //必须 终端店所在地
    "terminalDetailAddress":"成都市高新区环球中心"                  //必须 终端店详细地址
}
{
    "code": 200,
    "description": "执行成功!",
    "model": {//验证失败
        "success": "1",                                                 // 0-成功 1-失败
        "checkResult":"营业执照号30字以内"                              // 错误信息
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.TerminalInformationModifyResponse"
    }
}
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                  //0-成功 1-失败
        "checkResult": "提交成功"                                        //校验通过
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.TerminalInformationModifyResponse"
    }
}

"""

class terminalInformationModify(unittest.TestCase):
    UserShop1=wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    UserShop3 = wsData('RegistTmlShop')
    UserShop4 = wsData('DealMager')
    UserShop5=wsData('TmlShopMax')
    UserShop6=wsData('TmlShopMin')

    def setUp(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)


    #终端店注册拒绝后正确重新修改再注册
    def test_terminalInformationModify(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'0')
        self.assertEqual(registRepeat.model['checkResult'],'提交成功')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,2)
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList2=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid2=getList2.model['approvalList'][0]['approvalId']
        approveStatus=getList2.model['approvalList'][0]['approvalStatus']
        self.assertEqual(approveStatus,'0')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid2)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid2)

    #applyId不存在
    def test_terminalInformationModify_applyIdNotExist(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId='1234567890',terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'审批状态发生改变！')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #applyId为空
    def test_terminalInformationModify_applyIdNull(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId='',terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'审批状态发生改变！')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #applyId对应的终端店处于待审批状态(功能 #6078)
    def test_terminalInformationModify_approve(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        ws.login(self.UserShop3.username,self.UserShop3.password)
        registProgress=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress.model['success'],'0')
        self.assertEqual(registProgress.model['status'],'2')
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'审批状态发生改变！')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #applyId对应的终端店审批通过状态
    def test_terminalInformationModify_accept(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop3.username,self.UserShop3.password)
        registProgress=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress.model['success'],'0')
        self.assertEqual(registProgress.model['status'],'2')
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='0',approvalReason='')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'审批状态发生改变！')
        update('delete from dluser.dl_user where user_account=?',self.UserShop3.username)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        update('delete from dlcompany.dl_biz_base_info where company_name=?',self.UserShop3.fullName)

    #终端店名称为空
    def test_terminalInformationModify_terminalNameNull(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName='',businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'请输入终端店名称')

    #输入终端店名称超过60
    def test_terminalInformationModify_terminalNamelong(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop5.fullName+'超',businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'终端店名称60字以内')

    #输入终端店名称等于60
    def test_terminalInformationModify_terminalNameMax(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName='便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利哦',businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'0')
        self.assertEqual(registRepeat.model['checkResult'],'提交成功')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,2)
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList2=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid2=getList2.model['approvalList'][0]['approvalId']
        approveStatus=getList2.model['approvalList'][0]['approvalStatus']
        self.assertEqual(approveStatus,'0')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid2)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid2)

    #输入已存在的终端店名称
    def test_terminalInformationModify_terminalNameExist(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop1.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'终端店名称已被注册')

    #输入终端店名称含有特殊字符
    def test_terminalInformationModify_terminalNameSpecial(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName='!@#$%^&*()',businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'终端店名称只允许中文、英文、数字和下划线_')

    #输入营业执照号等于30
    def test_terminalInformationModify_licencsMax(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop5.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'0')
        self.assertEqual(registRepeat.model['checkResult'],'提交成功')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,2)
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList2=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid2=getList2.model['approvalList'][0]['approvalId']
        approveStatus=getList2.model['approvalList'][0]['approvalStatus']
        self.assertEqual(approveStatus,'0')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid2)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid2)

    #输入营业执照号大于30
    def test_terminalInformationModify_licenseLong(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop5.busLicenseNum+'1',terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'营业执照号30字以内')

    #输入营业执照号为空
    def test_terminalInformationModify_licenseNull(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode='',terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'请输入营业执照号')

    #店铺类型为空
    def test_terminalInformationModify_storeTypeNull(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode='',terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'请选择店铺类型')

    #终端店所在地为空
    def test_terminalInformationModify_areaCodeNull(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode='',
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'请选择终端店区域')

    #终端店详细地址等于140
    def test_terminalInformationModify_detailAddressMax(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop5.localStreet)
        self.assertEqual(registRepeat.model['success'],'0')
        self.assertEqual(registRepeat.model['checkResult'],'提交成功')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,2)
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList2=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid2=getList2.model['approvalList'][0]['approvalId']
        approveStatus=getList2.model['approvalList'][0]['approvalStatus']
        self.assertEqual(approveStatus,'0')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid2)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid2)

    #终端店详细地址大于140
    def test_terminalInformationModify_detailAddressLong(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop5.localStreet+'超')
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'详细地址140字以内')

    #终端店详细地址为空
    def test_terminalInformationModify_detailAddressNull(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress='')
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'请输入详细地址')

    #终端店地址含有特殊字符
    def test_terminalInformationModify_detailAddressSpecial(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        taskid=getList.model['approvalList'][0]['taskId']
        audit=ws.auditApproval(approvalId=approvid,taskId=taskid,auditStatus='1',approvalReason='拒绝该终端店注册成功！')
        self.assertEqual(audit.model['success'],'0')
        ws.login(self.UserShop3.username,self.UserShop3.password)
        ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress='!@#$%^&*()')
        self.assertEqual(registRepeat.model['success'],'1')
        self.assertEqual(registRepeat.model['checkResult'],'您输入的终端店地址含有特殊字符')



    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(terminalInformationModify("test_terminalInformationModify"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_applyIdNotExist"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_applyIdNull"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_approve"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_accept"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_terminalNameNull"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_terminalNamelong"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_terminalNameMax"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_terminalNameExist"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_terminalNameSpecial"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_licencsMax"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_licenseLong"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_licenseNull"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_storeTypeNull"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_areaCodeNull"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_detailAddressMax"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_detailAddressLong"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_detailAddressNull"))
    suite.addTest(terminalInformationModify("test_terminalInformationModify_detailAddressSpecial"))


    return suite
