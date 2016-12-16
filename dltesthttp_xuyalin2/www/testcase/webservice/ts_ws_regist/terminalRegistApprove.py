#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0246.终端店注册提交-含邀请码、验证码（已经上线）
http://127.0.0.1:8280/mallws/regist/terminalRegistApprove.json
{
    "terminalLoginName": "Test001",                            //用户名 允许为空
    "password": "123456",                                      //必填 密码
    "registerTel": "13399998888",                              //必填 手机号
    "terminalFullName": "终端店名",                            //必填 终端店名称
	"verificationCode": "8258",                                //必填 验证码
    "invitationCode": "2WDqoJ",                                //必填 邀请码
    "businessLicenseCode": "GBK23467",                         //必填 营业执照号
    "storeTypeCode": "S012",                                   //必填 店铺类型
    "terminalAreaProvinceCode": "CHNP014",                     //必填 终端店地址-省
    "terminalAreaCityCode": "CHNP014C012",                     //必填 终端店地址-市
    "terminalAreaDistrictCode": "CHNP014C012D124",             //必填 终端店地址-区县
    "terminalAddress": "黄浦路977号"                           //必填 详细地址
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                      // 成功 0-成功 1-失败 2-注册繁忙
		"checkResult": null                                  //校验通过
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.RegistResponse"
    }
}

{
  "code": 200,
  "description": "执行成功!",
  "model": {
    "success": "1",                                          // 成功 0-成功 1-失败
    "checkResult": {
      "firstValue": "terminalLoginName",                     //错误位置
      "secondValue": "您提交的用户名已被注册"                //错误信息
    }
  },
  "metadata": {
    "type": 0,
    "clazz": "cn.com.hd.mall.web.webservices.entity.response.regist.RegistResponse"
  }
}

参数校验:
    // 必须验证
    "terminalLoginName"                         @NotNull，不为空字符串，不能重复，由3-30位字母、数字和_组成，以字母开头
    "password"                                  @NotNull，不为空字符串，不能包含汉字，6-16位字符
    "registerTel"                               @NotNull，不为空字符串，@Pattern(regexp = "^((13[0-9])|(15[^4,\\D])|(18[0,5-9]))\\d{8}$")
	"verificationCode"							@NotNull，不为空字符串
    "invitationCode"							可以为空，@Pattern(regexp = "^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6}$")
    "terminalFullName"                          @NotNull，不为空字符串，60字以内
    "businessLicenseCode"                       @NotNull，不为空字符串，30字以内
    "storeTypeCode"                             @NotNull，不为空字符串
    "terminalAreaProvinceCode"                  @NotNull，不为空字符串
    "terminalAreaCityCode"                      @NotNull，不为空字符串
    "terminalAreaDistrictCode"                  @NotNull，不为空字符串
    "terminalAddress"                           @NotNull，不为空字符串，140字以内
code说明:
    200-成功 400-非法的参数 500-服务器异常
"""
class terminalRegistApprove(unittest.TestCase):
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


    #正确注册有用户名有邀请码的终端店
    def test_terminalRegistApprove_usrInvataion(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)


    #正确注册无用户名有邀请码的终端店
    def test_terminalRegistApprove_noUsrInvataion(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)
        selectUserName=select_one('select * from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectUserName.terminal_user_name,'dl'+self.UserShop3.registerTel)
        ws.login(self.UserShop4.username,self.UserShop4.password)
        getList=ws.getApprovalList(approvalStatus='0',page='1',rows='1')
        approvid=getList.model['approvalList'][0]['approvalId']
        update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',approvid)

    #正确注册有用户名无邀请码的终端店
    def test_terminalRegistApprove_usrNoInvataion(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode='',
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)


    #正确注册无用户名无邀请码的终端店
    def test_terminalRegistApprove_noUsrNoInvataion(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode='',
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)
        selectUserName=select_one('select * from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectUserName.terminal_user_name,'dl'+self.UserShop3.registerTel)


    #注册用户名以数字开头
    def test_terminalRegistApprove_usrNumStart(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='123456789',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalLoginName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'用户名由3-30位字母、数字和_组成，以字母开头')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #注册已存在的用户名
    def test_terminalRegistApprove_usrExist(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop1.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='111111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalLoginName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'您提交的用户名已被注册')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #注册用户名长度超过30
    def test_terminalRegistApprove_usrLong(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='testatzddmaxmaxmaxmaxmaxmaxmax1',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='111111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalLoginName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'用户名由3-30位字母、数字和_组成，以字母开头')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #注册用户名长度等于30
    def test_terminalRegistApprove_usrMax(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='testatzddmaxmaxmaxmaxmaxmaxma1',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)

    #注册用户名长度小于3
    def test_terminalRegistApprove_usrShort(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='zd',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalLoginName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'用户名由3-30位字母、数字和_组成，以字母开头')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #注册用户名长度等于3
    def test_terminalRegistApprove_usrMin(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='qwe',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)

    #注册用户名输入特殊字符
    def test_terminalRegistApprove_usrSpecial(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName='!@#$%^&*',password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalLoginName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'用户名由3-30位字母、数字和_组成，以字母开头')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #密码输入长度超过16
    def test_terminalRegistApprove_pswLong(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password='Danlu99maxmaxmax1',registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'password')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'密码由6-16位字母、数字和_组成，区分大小写')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #密码长度等于16
    def test_terminalRegistApprove_pswMax(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop5.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)

    #密码输入长度小于6
    def test_terminalRegistApprove_pswShort(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password='Danlu',registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'password')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'密码由6-16位字母、数字和_组成，区分大小写')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #密码为空
    def test_terminalRegistApprove_pswNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password='',registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'password')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入密码')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #密码输入汉字
    def test_terminalRegistApprove_pswChinese(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password='接口自动化测试',registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'password')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'密码由6-16位字母、数字和_组成，区分大小写')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入手机号为空
    def test_terminalRegistApprove_telNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel='',verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'registerTel')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入手机号')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入手机号长度不正确
    def test_terminalRegistApprove_telLong(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel='185498565238',verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'registerTel')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入正确的手机号')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入手机号号段不正确
    def test_terminalRegistApprove_telStyle(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel='21345678901',verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'registerTel')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入正确的手机号')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入已经注册的手机号
    def test_terminalRegistApprove_telExist(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop1.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'registerTel')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'手机号已经注册过，请更换手机号进行注册')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入待审批的手机号18349200236
    def test_terminalRegistApprove_telApprove(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel='18349200236',verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'registerTel')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'手机号已经注册过，请更换手机号进行注册')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入验证码为空
    def test_terminalRegistApprove_verificationNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'verificationCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'验证码错误')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入验证码不正确
    def test_terminalRegistApprove_verificationError(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='123456789',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'verificationCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'验证码错误')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_user_name=?',self.UserShop3.username)
        self.assertEqual(selectSql,0)

    #输入不存在的邀请码
    def test_terminalRegistApprove_notExistInvataion(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode='接口自动化测试错误邀请码',
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'invitationCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'邀请码不正确，请重新输入')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入终端店名称等于60(错误 #6008)
    def test_terminalRegistApprove_tmlFullNameMax(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName='便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利店便利哦',businessLicenseCode=self.UserShop3.busLicenseNum,
                                           storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)

    #输入终端店名称超过60
    def test_terminalRegistApprove_tmlFullNameLong(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop5.fullName+'超',businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalFullName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'终端店名称60字以内')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入终端店名称为空
    def test_terminalRegistApprove_tmlFullNameNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName='',businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalFullName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入终端店名称')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入已存在的终端店名称
    def test_terminalRegistApprove_tmlFullNameExist(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop1.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalFullName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'终端店名称已被注册')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入终端店名称含有特殊字符
    def test_terminalRegistApprove_tmlFullNameSpecial(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName='!@#!@#!@#!@#$',businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalFullName')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'终端店名称只允许中文、英文、数字和下划线_')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入营业执照号等于30
    def test_terminalRegistApprove_licenseNumMax(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop5.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)

    #输入营业执照号大于30
    def test_terminalRegistApprove_licenseNumLong(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop5.busLicenseNum+'1',storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'businessLicenseCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'营业执照号30字以内')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #输入营业执照号为空
    def test_terminalRegistApprove_licenseNumNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode='',storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'businessLicenseCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入营业执照号')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #店铺类型为空
    def test_terminalRegistApprove_storeTypeNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode='',terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'storeTypeCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请选择店铺类型')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #终端店地址省为空
    def test_terminalRegistApprove_terminalAreaProvinceCodeNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode='',
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalAreaProvinceCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请选择终端店区域')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #终端店地址市为空
    def test_terminalRegistApprove_terminalAreaCityCodeNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode='',terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalAreaCityCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请选择终端店区域')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #终端店地址区为空
    def test_terminalRegistApprove_terminalAreaDistrictCodeNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode='',terminalAddress=self.UserShop3.localStreet)
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalAreaDistrictCode')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请选择终端店区域')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #终端店详细地址等于140
    def test_terminalRegistApprove_terminalAddressMax(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop5.localStreet)
        self.assertEqual(tmlRegist.model['success'],'0')
        self.assertEqual(tmlRegist.model['checkResult'],None)
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,1)

    #终端店详细地址大于140
    def test_terminalRegistApprove_terminalAddressLong(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress=self.UserShop5.localStreet+'超')
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalAddress')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'详细地址140字以内')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #终端店详细地址为空
    def test_terminalRegistApprove_terminalAddressNull(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress='')
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalAddress')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'请输入详细地址')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    #终端店地址含有特殊字符
    def test_terminalRegistApprove_terminalAddressSpecial(self):
        ws=webservice()
        tmlRegist=ws.terminalRegistApprove(terminalLoginName=self.UserShop3.username,password=self.UserShop3.password,registerTel=self.UserShop3.registerTel,verificationCode='1111',invitationCode=self.UserShop4.invitationCode,
                                           terminalFullName=self.UserShop3.fullName,businessLicenseCode=self.UserShop3.busLicenseNum,storeTypeCode=self.UserShop3.storeTypeCode,terminalAreaProvinceCode=self.UserShop3.areaProvinceCode,
                                           terminalAreaCityCode=self.UserShop3.areaCityCode,terminalAreaDistrictCode=self.UserShop3.areaDistrictCode,terminalAddress='！@#！@#！@#！@#')
        self.assertEqual(tmlRegist.model['success'],'1')
        self.assertEqual(tmlRegist.model['checkResult']['firstValue'],'terminalAddress')
        self.assertEqual(tmlRegist.model['checkResult']['secondValue'],'您输入的终端店地址含有特殊字符')
        selectSql=select_int('select count(*) from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        self.assertEqual(selectSql,0)

    def tearDown(self):
        applyId=select_one('select apply_id from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)
        if applyId!=None:
            update('delete from dlworkflow.act_hi_procinst where BUSINESS_KEY_=?',str(applyId.apply_id))
            update('delete from dlworkflow.dl_apply_terminal where terminal_tel=?',self.UserShop3.registerTel)


def suite():
    suite=unittest.TestSuite()


    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrInvataion"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_noUsrInvataion"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrNoInvataion"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_noUsrNoInvataion"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrNumStart"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrExist"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrLong"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrMax"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrShort"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrMin"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_usrSpecial"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_pswLong"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_pswMax"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_pswShort"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_pswNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_pswChinese"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_telNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_telLong"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_telStyle"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_telExist"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_telApprove"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_verificationNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_verificationError"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_notExistInvataion"))
    # #suite.addTest(terminalRegistApprove("test_terminalRegistApprove_tmlFullNameMax"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_tmlFullNameLong"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_tmlFullNameNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_tmlFullNameExist"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_tmlFullNameSpecial"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_licenseNumMax"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_licenseNumLong"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_licenseNumNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_storeTypeNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAreaProvinceCodeNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAreaCityCodeNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAreaDistrictCodeNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAddressMax"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAddressLong"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAddressNull"))
    suite.addTest(terminalRegistApprove("test_terminalRegistApprove_terminalAddressSpecial"))

    return suite
