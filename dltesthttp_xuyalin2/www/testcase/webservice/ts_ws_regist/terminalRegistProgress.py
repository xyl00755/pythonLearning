#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
1.终端店注册查看审批进度
http://127.0.0.1:8080/mallws/regist/terminalRegistProgress.json
{
    "username":"gaojian",                                  //必须 手机号或用户名唯一
    "password":"123456"                                    //必须 密码
}
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                    // 0-成功 1-失败（原因）
        "status":  "1" ,                                   // 0-通过  1-拒绝 2-审批中
        "registProgressList": [
                      {
                        "time": "08-23 20:51:24",                                               //时间
                        "description": "内测-开发部高健(dl_gaojian)提交了申请",                  //内容
                        "reason":"终端店类型不正确"                                             //拒绝原因
                      }
                    ],
        "registInfo":{
            "terminalTel":"18349349070",                            //手机号
            "terminalUserName":"GAOJIAN ",                          //用户名
            "terminalName":"高健的终端店",                          //终端店名称
            "businessLicenseCode":"111111",                         //营业执照号码
            "terminalTypeCode":"S011",                              //商业超市
                                                                    // 1.烟酒专卖店  S011
                                                                    // 2.便利店      S012
                                                                    // 3.餐饮店      S013
                                                                    // 4.商业超市    S014
                                                                    // 5.其他        S015
            "terminalDetailAddress":"成都市高新区环球中心",         //终端店详细地址
            "invitationCode":"1234",                                //邀请码  可以为null  （3 <= 长度 <= 8）
            "applyId":"1231231414",                                  //注册号
            "terminalAreaFullName":"四川省成都市高新区",            //终端店所在地区名字
            "terminalAreaCode":"CHNP007C056D0594"                  //终端店所在地
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.TerminalRegistProgressResponse"
    }
}
"""

class terminalRegistProgress(unittest.TestCase):
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

    #用用户名查看审批进度（待审批）
    def test_terminalRegistProgress_usr(self):
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
        self.assertNotEqual(registProgress.model['registProgressList'][0]['time'],'')
        self.assertEqual(registProgress.model['registProgressList'][0]['description'],'注册自动化烟酒专卖店(testatzddRegist)提交了申请')
        self.assertRegistInfoSuccess(registPro=registProgress)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #用手机号查看审批进度（待审批）
    def test_terminalRegistProgress_tel(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        ws.login(self.UserShop3.username,self.UserShop3.password)
        registProgress=ws.terminalRegistProgress(self.UserShop3.registerTel,self.UserShop3.password)
        self.assertEqual(registProgress.model['success'],'0')
        self.assertEqual(registProgress.model['status'],'2')
        self.assertNotEqual(registProgress.model['registProgressList'][0]['time'],'')
        self.assertEqual(registProgress.model['registProgressList'][0]['description'],'注册自动化烟酒专卖店(testatzddRegist)提交了申请')
        self.assertRegistInfoSuccess(registPro=registProgress)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #用用户名查看拒绝审批进度（经销商拒绝）
    def test_terminalRegistProgress_refused(self):
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
        registProgress=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress.model['success'],'0')
        self.assertEqual(registProgress.model['status'],'1')
        self.assertNotEqual(registProgress.model['registProgressList'][0]['time'],'')
        self.assertEqual(registProgress.model['registProgressList'][0]['description'],'经销商（测试自动化配送商01）拒绝了您的申请 ')
        self.assertEqual(registProgress.model['registProgressList'][0]['reason'],'拒绝该终端店注册成功！')
        self.assertNotEqual(registProgress.model['registProgressList'][1]['time'],'')
        self.assertEqual(registProgress.model['registProgressList'][1]['description'],'注册自动化烟酒专卖店(testatzddRegist)提交了申请')
        self.assertRegistInfoSuccess(registPro=registProgress)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #用用户名查看审批通过审批进度
    def test_terminalRegistProgress_accept(self):
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
        registProgress2=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress2.model['success'],'0')
        self.assertEqual(registProgress2.model['status'],'0')
        self.assertNotEqual(registProgress2.model['registProgressList'][0]['time'],'')
        self.assertEqual(registProgress2.model['registProgressList'][0]['description'],'经销商（测试自动化配送商01）同意了您的申请')
        self.assertNotEqual(registProgress2.model['registProgressList'][1]['time'],'')
        self.assertEqual(registProgress2.model['registProgressList'][1]['description'],'注册自动化烟酒专卖店(testatzddRegist)提交了申请')
        self.assertRegistInfoSuccess(registPro=registProgress2)
        getList=ws.getApprovalList(approvalStatus='1',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dluser.dl_user where user_account=?',self.UserShop3.username)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        update('delete from dlcompany.dl_biz_base_info where company_name=?',self.UserShop3.fullName)

    #经过一次拒绝重新提交查看审批进度
    def test_terminalRegistProgress_repeatRegist(self):
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
        registProgress=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress.model['success'],'0')
        self.assertEqual(registProgress.model['status'],'1')
        self.assertNotEqual(registProgress.model['registProgressList'][0]['time'],'')
        self.assertEqual(registProgress.model['registProgressList'][0]['description'],'经销商（测试自动化配送商01）拒绝了您的申请 ')
        self.assertEqual(registProgress.model['registProgressList'][0]['reason'],'拒绝该终端店注册成功！')
        self.assertNotEqual(registProgress.model['registProgressList'][1]['time'],'')
        self.assertEqual(registProgress.model['registProgressList'][1]['description'],'注册自动化烟酒专卖店(testatzddRegist)提交了申请')
        self.assertRegistInfoSuccess(registPro=registProgress)
        registRepeat=ws.terminalInformationModify(applyId=approvid,terminalName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,terminalTypeCode=self.UserShop3.storeTypeCode,terminalAreaCode=self.UserShop3.areaCode,
                                                  terminalDetailAddress=self.UserShop3.localStreet)
        self.assertEqual(registRepeat.model['success'],'0')
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)
        registProgress2=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress2.model['success'],'0')
        self.assertEqual(registProgress2.model['status'],'2')
        self.assertNotEqual(registProgress2.model['registProgressList'][0]['time'],'')
        self.assertEqual(registProgress2.model['registProgressList'][0]['description'],'注册自动化烟酒专卖店(testatzddRegist)提交了申请')
        self.assertRegistInfoSuccess(registPro=registProgress2)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList2=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid2=getList2.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.dl_apply_terminal where apply_id=?',approvid2)
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid2)

    #无session
    def test_terminalRegistProgress_noSession(self):
        ws=webservice()
        #注册一个待审批的终端店
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        registProgress=ws.terminalRegistProgress(self.UserShop3.username,self.UserShop3.password)
        self.assertEqual(registProgress.model['success'],'1')
        self.assertEqual(registProgress.model['status'],None)
        self.assertEqual(registProgress.model['registProgressList'],None)
        self.assertEqual(registProgress.model['registInfo'],None)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    def assertRegistInfoSuccess(self,registPro=None):
        self.assertEqual(registPro.model['registInfo']['terminalTel'],self.UserShop3.registerTel)
        self.assertEqual(registPro.model['registInfo']['terminalUserName'],self.UserShop3.username)
        self.assertEqual(registPro.model['registInfo']['terminalName'],self.UserShop3.fullName)
        self.assertEqual(registPro.model['registInfo']['businessLicenseCode'],self.UserShop3.busLicenseNum)
        self.assertEqual(registPro.model['registInfo']['terminalTypeCode'],self.UserShop3.storeTypeCode)
        self.assertEqual(registPro.model['registInfo']['terminalDetailAddress'],self.UserShop3.localStreet)
        self.assertEqual(registPro.model['registInfo']['terminalAreaFullName'],self.UserShop3.localProvince+self.UserShop3.localCity+self.UserShop3.localCountry)
        self.assertEqual(registPro.model['registInfo']['terminalAreaCode'],self.UserShop3.areaCode)

    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(terminalRegistProgress("test_terminalRegistProgress_usr"))
    suite.addTest(terminalRegistProgress("test_terminalRegistProgress_tel"))
    suite.addTest(terminalRegistProgress("test_terminalRegistProgress_refused"))
    suite.addTest(terminalRegistProgress("test_terminalRegistProgress_accept"))
    suite.addTest(terminalRegistProgress("test_terminalRegistProgress_repeatRegist"))
    suite.addTest(terminalRegistProgress("test_terminalRegistProgress_noSession"))
    return suite

