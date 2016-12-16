#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.excel import *

"""
0001.登陆
http://127.0.0.1:8880/login/login.json
{
    "username":"testliqi",
    "password":"e10adc3949ba59abbe56e057f20f883e"
}

{
  "code": 200,
  "description": "执行成功!",
  "model": {
    "success": "0",                                         // 登陆是否成功 0-成功 2-用户不存在 3-终端店正在审核中 4-用户名或密码错误 5-帐号所在省份暂时无法登录
    "sessionId": "f9eabd69-df4e-4986-b368-758399c76afb",
    "token": "f94a74c793d84c97a9a5fa74a308e853",
    "userId": "346b22f8e2624ac41a8ea9967816fe95",
    "companyId": "6fb850120da449ef98a2c7e641100e02",
    "userRole": "T_ROLE",                                   // 角色 B_R_ADMI-经销商管理员 B_R_PURC-经销商采购员 B_R_SALE-经销商销售员 B_R_SEND-经销商配送员 T_ROLE-终端店
    "fullName": "自动化烟酒专卖店",
    "areaCode": "CHNP035C345D2998"
  },
  "metadata": {
    "type": 0,
    "clazz": "cn.com.hd.mall.web.webservices.entity.response.login.LoginResponse"
  }
}
"""

class login(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserDealMgr = wsData('DealMager')
    UserDealBuy = wsData('DealBuyer')
    UserDealSal = wsData('DealSaler')
    UserDealSed = wsData('DealSeder')
    UserDealFin = wsData('DealFiner')
    Param = wsData('Param')

    # S1.登陆终端店用户名，验证登录接口是否正确
    def test_Login_TmlShop(self):
        dl = webservice().login(self.UserShop.username, self.UserShop.password)
        self.assertLoginSuccess(dl, self.UserShop, actForceInd = self.Param.zddActForceInd)

    # 使用手机号码登录
    def test_Login_TmlShopTel(self):
        dl = webservice().login(self.UserShop.mobileNumber, self.UserShop.password)
        self.assertLoginSuccess(dl, self.UserShop, actForceInd = self.Param.zddActForceInd)

    # S2.用户名（3位）和密码（6位）最小值登录
    def test_Login_Min(self):
        UserMin = wsData('TmlShopMin')
        dlMin = webservice().login(UserMin.username, UserMin.password)
        self.assertLoginSuccess(dlMin, UserMin, actForceInd = self.Param.zddActForceInd)

    # S3.用户名（30位）和密码（16位）最大值登录
    def test_Login_Max(self):
        UserMax = wsData('TmlShopMax')
        dlMax = webservice().login(UserMax.username, UserMax.password)
        self.assertLoginSuccess(dlMax, UserMax, actForceInd = self.Param.zddActForceInd)



    # S4.用户名不存在
    def test_Login_ErrName(self):
        dlErrName = webservice().login('ErrName', '123456')
        self.assertEqual(dlErrName.model['success'], '2')

    # S5.用户名为空——参数非法，实际更正后报错修改为相应的错误码
    def test_Login_NullName(self):
        dlNullName = webservice().login('', '123456')
        self.assertEqual(dlNullName.model['success'], '2')

    # S6.用户名不足3位——参数非法，实际更正后报错修改为相应的错误码
    def test_Login_UndName(self):
        dlUndName = webservice().login('Un', '123456')
        self.assertEqual(dlUndName.model['success'], '2')

    # S7.用户名超过最大字符30个——参数非法，实际更正后报错修改为相应的错误码
    def test_Login_SupName(self):
        dlSupName = webservice().login('testatzdd01testatzdd0testatzdd0', '123456')
        self.assertEqual(dlSupName.model['success'], '2')


    # S8.密码错误登录终端店
    def test_Login_ErrPwd(self):
        ErrPwd = webservice().login(self.UserShop.username, '123456')
        self.assertEqual(ErrPwd.model['success'], '4')

    # S9.密码为空登录终端店——参数非法，实际更正后报错修改为相应的错误码
    def test_Login_NullPwd(self):
        NullPwd = webservice().login(self.UserShop.username, '')
        self.assertEqual(NullPwd.model['success'], '4')



    # S10.登陆经销商管理员，验证登录接口是否正确
    def test_Login_DealMager(self):
        dlDealMgr = webservice().login(self.UserDealMgr.username, self.UserDealMgr.password)
        self.assertLoginSuccess(dlDealMgr, self.UserDealMgr, actForceInd = self.Param.jxsActForceInd)

    # S11.登陆经销商采购员，验证登录接口是否正确
    def test_Login_DealSaler(self):
        dlDealSaler = webservice().login(self.UserDealSal.username, self.UserDealSal.password)
        self.assertLoginSuccess(dlDealSaler, self.UserDealSal, actForceInd = self.Param.jxsActForceInd)

    # S12.登陆经销商采购员，验证登录接口是否正确
    def test_Login_DealBuyer(self):
        dlDealBuyer = webservice().login(self.UserDealBuy.username, self.UserDealBuy.password)
        self.assertLoginSuccess(dlDealBuyer, self.UserDealBuy, actForceInd = self.Param.jxsActForceInd)

    # S13.登陆经销商配送员，验证登录接口是否正确
    def test_Login_DealSeder(self):
        dlDealSeder = webservice().login(self.UserDealSed.username, self.UserDealSed.password)
        self.assertLoginSuccess(dlDealSeder, self.UserDealSed, actForceInd = self.Param.jxsActForceInd)

    # S14.登陆经销商财务员，验证登录接口是否正确
    def test_Login_DealFiner(self):
        dlDealFiner = webservice().login(self.UserDealFin.username, self.UserDealFin.password)
        self.assertLoginSuccess(dlDealFiner, self.UserDealFin, actForceInd = self.Param.jxsActForceInd)


    # 登录成功验证方法
    def assertLoginSuccess(self, rsp, User, code = 200, success = '0', actForceInd = '0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertIsNotNone(rsp.model['sessionId'])
        self.assertIsNotNone(rsp.model['token'])
        self.assertEqual(rsp.model['userId'], str(User.userId))
        self.assertEqual(rsp.model['companyId'], str(User.companyId))
        self.assertEqual(rsp.model['userRole'], str(User.userRole))
        self.assertEqual(rsp.model['fullName'].encode('utf-8'), str(User.fullName))
        self.assertEqual(rsp.model['areaCode'], str(User.areaCode))
        self.assertEqual(rsp.model['userAcct'], str(User.username))
        self.assertEqual(rsp.model['tel'], str(User.mobileNumber))
        self.assertEqual(rsp.model['telStatus'], str(User.telStatus))
        self.assertEqual(rsp.model['firstActiveTime'], str(User.firstActiveTime))
        self.assertEqual(rsp.model['sysParm']['actForceInd'], actForceInd)
        self.assertEqual(rsp.model['sysParm']['actCouponAmt'], str(self.Param.actCouponAmt))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(login("test_Login_TmlShop"))
    suite.addTest(login("test_Login_TmlShopTel"))
    suite.addTest(login("test_Login_Min"))
    suite.addTest(login("test_Login_Max"))
    suite.addTest(login("test_Login_ErrName"))
    suite.addTest(login("test_Login_NullName"))
    suite.addTest(login("test_Login_UndName"))
    suite.addTest(login("test_Login_SupName"))
    suite.addTest(login("test_Login_ErrPwd"))
    suite.addTest(login("test_Login_NullPwd"))
    suite.addTest(login("test_Login_DealMager"))
    suite.addTest(login("test_Login_DealSaler"))
    suite.addTest(login("test_Login_DealBuyer"))
    suite.addTest(login("test_Login_DealSeder"))
    suite.addTest(login("test_Login_DealFiner"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'suite')




