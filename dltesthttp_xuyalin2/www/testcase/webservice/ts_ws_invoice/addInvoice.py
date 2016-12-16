#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
http://127.0.0.1:8280/mallws/mydl/invoice/addInvoice.json
{
    "token":"36805433b4d14ba98faf37b0edefe53a",             // 必须
    "invoice": {                                            // 发票模型
        "invoiceType": "N011",                              // 必须 发票类型 N011-普通发票 N012-增值税发票
        "invoiceHeader": "DJDJDJ",                          // N011-必须 N012-null 发票抬头
        "companyName": null,                                // N011-null N012-必须 公司名
        "taxpayerRegistrationNumber": null,                 // N011-null N012-必须 纳税人识别号
        "registerAddress": null,                            // N011-null N012-必须 注册地址
        "registerTel": null,                                // N011-null N012-必须 注册电话
        "depositBank": null,                                // N011-null N012-必须 开户银行
        "accountBank": null,                                // N011-null N012-必须 帐户银行
        "receiveManName": null,                             // N011-null N012-必须 收票人姓名
        "receiveManTel": null,                              // N011-null N012-必须 收票人电话
        "receiveManProvince": null,                         // N011-null N012-必须 收票人省份
        "receiveManAddress": null                           // N011-null N012-必须 收票人详细地址
    }
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "2",                                     // 成功 0-成功 1-未知失败 2-普通字段校验不过,"checkResult"提示错误详情 3-普通发票抬头字数超50 4-普通发票重名 5-超过最大限制
		"checkResult": {
		  "firstValue": "companyName",                    	//错误位置
		  "secondValue": "错误信息"                			//错误信息
		}
	},
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.invoice.AddModifyInvoiceResponse"
    }
}

参数校验:
    invoiceType         @NotNull        @Pattern(regexp = "(N011)|(N012)")
    invoiceHeader       @Size(min = 1, max = 50)                            // 发票抬头 50字以内
    companyName         @Size(min = 1, max = 60)                            // 公司名称 60字以内
    taxpayerRegistrationNumber          @Pattern(regexp = "\\w{20}")        // 纳税人识别码 20位
    registerAddress     @Size(min = 1, max = 50)                            // 注册地址 50字以内
    registerTel         @Pattern(regexp =                                   // 注册电话 验证手机号、座机格式
						"((0\\d{2,3}-)?\\d{7,8})|(^1[34578]\\d{9}$)")
	depositBank         @Size(min = 1, max = 60)                            // 开户银行 60字以内
    accountBank         @Size(min = 1, max = 60)                            // 银行账户 60字以内
    receiveManName      @Size(min = 1, max = 60)                            // 收票人姓名 60字以内
    receiveManTel       @Pattern(regexp = "^1[34578]\\d{9}$")               // 收票人手机 验证手机号格式
    receiveManProvince  @Size(min = 1, max = 10)                            // 收票人省份 10字以内
    receiveManAddress   @Size(min = 1, max = 60)                            // 详细地址 60字以内
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class addInvoice(unittest.TestCase):

    UserShop2 = wsData('TmlShop2')
    UserShopMin = wsData('TmlShopMin')
    UserShopMax = wsData('TmlShopMax')

    def setUp(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?', self.UserShop2.userId)

    # S1.添加普通发票
    def test_addInvoice_normal(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvNormal = ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(addInvNormal.model['success'], '0')
        addInvNormalList = ws.getInvoiceList()
        self.assertGetNormalSuccess(addInvNormalList, self.UserShop2.invoiceHeader)


    #S2. 增加最小字符的普通发票
    def test_addInvoice_normalMin(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvNormalMin = ws.addInvoice(invoiceHeader = self.UserShopMin.invoiceHeader)
        self.assertEqual(addInvNormalMin.model['success'], '0')
        addInvNormalMinList = ws.getInvoiceList()
        self.assertGetNormalSuccess(addInvNormalMinList, self.UserShopMin.invoiceHeader)


    #S3. 增加最大字符的普通发票
    def test_addInvoice_normalMax(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvNormalMax = ws.addInvoice(invoiceHeader = self.UserShopMax.invoiceHeader)
        self.assertEqual(addInvNormalMax.model['success'], '0')
        addInvNormalMaxList = ws.getInvoiceList()
        self.assertGetNormalSuccess(addInvNormalMaxList, self.UserShopMax.invoiceHeader)

    #S4. 增加抬头为空的普通发票
    def test_addInvoice_normalNull(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvNormalNull = ws.addInvoice(invoiceHeader = '')
        self.assertEqual(addInvNormalNull.model['checkResult']['firstValue'], 'invoiceHeader')
        self.assertEqual(addInvNormalNull.model['checkResult']['secondValue'], '请填写发票抬头')
        addInvNormalNullList = ws.getInvoiceList()
        self.assertEquals(addInvNormalNullList.model['normalInvoiceList'], [])

    #S5. 增加抬头超过50位字符的普通发票
    def test_addInvoice_normalUp(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvNormalUp = ws.addInvoice(invoiceHeader = 'abcdefghijklmnopqrstuvwxyz123456790一二三四五六七八12345678')
        self.assertEqual(addInvNormalUp.model['success'], '2')
        self.assertEqual(addInvNormalUp.model['checkResult']['firstValue'], 'invoiceHeader')
        self.assertEqual(addInvNormalUp.model['checkResult']['secondValue'], '发票抬头50字以内')
        addInvNormalUpList = ws.getInvoiceList()
        self.assertEquals(addInvNormalUpList.model['normalInvoiceList'], [])

    # S6.添加相同抬头的普通发票
    def test_addInvoice_normalRep(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        addInvNormalRep = ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(addInvNormalRep.model['success'], '4')

    # S7 添加16条普通发票
    def test_addInvoice_normalMore(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = '1')
        ws.addInvoice(invoiceHeader = '2')
        ws.addInvoice(invoiceHeader = '3')
        ws.addInvoice(invoiceHeader = '4')
        ws.addInvoice(invoiceHeader = '5')
        ws.addInvoice(invoiceHeader = '6')
        ws.addInvoice(invoiceHeader = '7')
        ws.addInvoice(invoiceHeader = '8')
        ws.addInvoice(invoiceHeader = '9')
        ws.addInvoice(invoiceHeader = '10')
        ws.addInvoice(invoiceHeader = '11')
        ws.addInvoice(invoiceHeader = '12')
        ws.addInvoice(invoiceHeader = '13')
        ws.addInvoice(invoiceHeader = '14')
        ws.addInvoice(invoiceHeader = '15')
        addInvNormalMoreList = ws.getInvoiceList()
        self.assertEqual(len(addInvNormalMoreList.model['normalInvoiceList']), 15)
        addInvNormalMore = ws.addInvoice(invoiceHeader = '16')
        self.assertEqual(addInvNormalMore.model['success'], '5')

    # S8.添加第一张发票时为默认发票，添加第二张时不为默认发票
    def test_addInvoice_normalDefault(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = '默认')
        ws.addInvoice(invoiceHeader = '非默认')
        addInvnormalDefault = ws.getInvoiceList()
        if(addInvnormalDefault.model['normalInvoiceList'][0]['invoiceHeader'] == '默认'):
            self.assertEqual(addInvnormalDefault.model['normalInvoiceList'][0]['isDefault'], '0')
            self.assertEqual(addInvnormalDefault.model['normalInvoiceList'][1]['isDefault'], '1')
        elif(addInvnormalDefault.model['normalInvoiceList'][0]['invoiceHeader'] == '非默认'):
            self.assertEqual(addInvnormalDefault.model['normalInvoiceList'][0]['isDefault'], '1')
            self.assertEqual(addInvnormalDefault.model['normalInvoiceList'][1]['isDefault'], '0')


    # S1.添加增值税发票
    def test_addInvoice_vat(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvVAT = ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        self.assertEqual(addInvVAT.model['success'], '0')
        addInveVatList = ws.getInvoiceList()
        self.assertGetVatSuccess(addInveVatList, self.UserShop2)

    #S2. 增加最小字符的增值税发票
    def test_addInvoice_vatMin(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvVATMin = ws.addInvoice(invoiceType = 'N012', companyName =self.UserShopMin.companyName, taxpayerRegistrationNumber =self.UserShopMin.taxpayerRegistrationNumber, registerAddress =self.UserShopMin.registerAddress,
                                  registerTel = self.UserShopMin.registerTel, depositBank =self.UserShopMin.depositBank, accountBank =self.UserShopMin.accountBank,
                                  receiveManName =self.UserShopMin.receiveManName, receiveManTel =self.UserShopMin.receiveManTel, receiveManProvince = self.UserShopMin.receiveManProvince,
                                  receiveManAddress = self.UserShopMin.receiveManAddress)
        self.assertEqual(addInvVATMin.model['success'], '0')
        addInveVatList = ws.getInvoiceList()
        self.assertGetVatSuccess(addInveVatList, self.UserShopMin)

    #S3. 增加最大字符的增值税发票——错误 #5360
    def test_addInvoice_vatMax(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        addInvVAT = ws.addInvoice(invoiceType = 'N012', companyName =self.UserShopMax.companyName, taxpayerRegistrationNumber =self.UserShopMax.taxpayerRegistrationNumber, registerAddress =self.UserShopMax.registerAddress,
                                  registerTel = self.UserShopMax.registerTel, depositBank =self.UserShopMax.depositBank, accountBank =self.UserShopMax.accountBank,
                                  receiveManName =self.UserShopMax.receiveManName, receiveManTel =self.UserShopMax.receiveManTel, receiveManProvince = self.UserShopMax.receiveManProvince,
                                  receiveManAddress = self.UserShopMax.receiveManAddress)
        self.assertEqual(addInvVAT.model['success'], '0')
        addInveVatList = ws.getInvoiceList()
        self.assertGetVatSuccess(addInveVatList, self.UserShopMax)

    # S4.增加两个增值税发票
    def test_addInvoice_vatAgain(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        addInvoiceAgain = ws.addInvoice(invoiceType = 'N012', companyName = 'vatagain', taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        self.assertEqual(addInvoiceAgain.model['success'], '5')

    # S5.添加字段为空的增值税发票

    # S6.添加字段超过规定范围的增值税发票



    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?', self.UserShop2.userId)


    # 数据库中的默认和真实默认不一致，所以需要real一下
    def realDefault(self, is_default):
        if(is_default=='0'):
            return '1'
        elif(is_default=='1'):
            return '0'


    # 查询普通发票成功验证方法
    def assertGetNormalSuccess(self, rsp, invoiceHeader, isDefault = '1',code = 200, success = '0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['normalInvoiceList'][0]['invoiceType'], 'N011')
        self.assertEqual(rsp.model['normalInvoiceList'][0]['invoiceHeader'], invoiceHeader)
        self.assertEqual(rsp.model['normalInvoiceList'][0]['isDefault'], self.realDefault(isDefault))

    # 查询增值发票成功验证方法
    def assertGetVatSuccess(self, rsp, User, code = 200, success = '0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['vatInvoice']['invoiceType'], 'N012')
        self.assertEqual(rsp.model['vatInvoice']['companyName'], User['companyName'])
        self.assertEqual(rsp.model['vatInvoice']['taxpayerRegistrationNumber'], User['taxpayerRegistrationNumber'])
        self.assertEqual(rsp.model['vatInvoice']['registerAddress'], User['registerAddress'])
        self.assertEqual(rsp.model['vatInvoice']['registerTel'], User['registerTel'])
        self.assertEqual(rsp.model['vatInvoice']['depositBank'], User['depositBank'])
        self.assertEqual(rsp.model['vatInvoice']['accountBank'], User['accountBank'])
        self.assertEqual(rsp.model['vatInvoice']['isDefault'], '0')
        self.assertEqual(rsp.model['vatInvoice']['receiveManName'], User['receiveManName'])
        self.assertEqual(rsp.model['vatInvoice']['receiveManTel'], User['receiveManTel'])
        self.assertEqual(rsp.model['vatInvoice']['receiveManProvince'], User['receiveManProvince'])
        self.assertEqual(rsp.model['vatInvoice']['receiveManAddress'], User['receiveManAddress'])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(addInvoice("test_addInvoice_normal"))
    suite.addTest(addInvoice("test_addInvoice_normalMin"))
    suite.addTest(addInvoice("test_addInvoice_normalMax"))
    suite.addTest(addInvoice("test_addInvoice_normalNull"))
    suite.addTest(addInvoice("test_addInvoice_normalUp"))
    suite.addTest(addInvoice("test_addInvoice_normalRep"))
    suite.addTest(addInvoice("test_addInvoice_normalMore"))
    suite.addTest(addInvoice("test_addInvoice_normalDefault"))
    suite.addTest(addInvoice("test_addInvoice_vat"))
    suite.addTest(addInvoice("test_addInvoice_vatMin"))
    suite.addTest(addInvoice("test_addInvoice_vatMax"))
    suite.addTest(addInvoice("test_addInvoice_vatAgain"))
    return suite


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'suite')