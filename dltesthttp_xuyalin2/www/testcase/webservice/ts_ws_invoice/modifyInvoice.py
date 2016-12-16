#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0202.修改发票
http://127.0.0.1:8280/mallws/mydl/invoice/modifyInvoice.json
{
    "token":"66dc3c0d3cf7408c8d1845b9448a0e37",             // 必须
    "invoice": {                                            // 发票模型
        "invoiceId": null,                                  // 原来是什么填什么
        "invoiceType": "N011",                              // 原来是什么填什么
        "invoiceHeader": "DJDJDJ",                          // N011-可选修改 N012-null 发票抬头
        "companyName": null,                                // N011-null N012-可选修改 公司名
        "taxpayerRegistrationNumber": null,                 // N011-null N012-可选修改 纳税人识别号
        "registerAddress": null,                            // N011-null N012-可选修改 注册地址
        "registerTel": null,                                // N011-null N012-可选修改 注册电话
        "depositBank": null,                                // N011-null N012-可选修改 开户银行
        "accountBank": null,                                // N011-null N012-可选修改 帐户银行
        "receiveManName": null,                             // N011-null N012-可选修改 收票人姓名
        "receiveManTel": null,                              // N011-null N012-可选修改 收票人电话
        "receiveManProvince": null,                         // N011-null N012-可选修改 收票人省份
        "receiveManAddress": null                           // N011-null N012-可选修改 收票人详细地址
    }
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "2",                                      // 成功 0-成功 1-失败 2-字段校验不过 3-普通发票不存在 4-普通发票抬头字数超50 5-普通发票重名
		"checkResult": {
		  "firstValue": "companyName",                    	 //错误位置
		  "secondValue": "错误信息"                			 //错误信息
		}
	},
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.invoice.AddModifyInvoiceResponse"
    }
}

参数校验: 理由同添加接口
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

class modifyInvoice(unittest.TestCase):

    UserShop2 = wsData('TmlShop2')
    UserShopMin = wsData('TmlShopMin')
    UserShopMax = wsData('TmlShopMax')

    # S1.修改普通发票抬头
    def test_modifyInvoice_normal(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = 'test')
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N011')
        modInvNormal = ws.modifyInvoice(invoiceId = invoiceNormal.invoice_id, invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(modInvNormal.model['success'], '0')
        modInvNormalList = ws.getInvoiceList()
        self.assertGetNormalSuccess(modInvNormalList, self.UserShop2)

    # S2.修改不存在的普通发票抬头
    def test_modifyInvoice_normalNotExist(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        modInvNormal = ws.modifyInvoice(invoiceId = 'notExist', invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(modInvNormal.model['success'], '3')

    # S3.修改普通发票抬头为空
    def test_modifyInvoice_normalNull(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N011')
        modInvNormal = ws.modifyInvoice(invoiceId = invoiceNormal.invoice_id, invoiceHeader = '')
        self.assertEqual(modInvNormal.model['success'], '2')
        modInvNormalList = ws.getInvoiceList()
        self.assertGetNormalSuccess(modInvNormalList, self.UserShop2)

    # S4.修改普通发票抬头超过50个字符
    def test_modifyInvoice_normalUp(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N011')
        modInvNormal = ws.modifyInvoice(invoiceId = invoiceNormal.invoice_id, invoiceHeader = 'abcdefghijklmnopqrstuvwxyz123456790一二三四五六七八12345678')
        self.assertEqual(modInvNormal.model['success'], '2')
        self.assertEqual(modInvNormal.model['checkResult']['firstValue'], 'invoiceHeader')
        self.assertEqual(modInvNormal.model['checkResult']['secondValue'], '发票抬头50字以内')
        modInvNormalList = ws.getInvoiceList()
        self.assertGetNormalSuccess(modInvNormalList, self.UserShop2)

    # S5.修改普通发票抬头重名
    def test_modifyInvoice_normalRep(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceHeader = self.UserShop2.invoiceHeader)
        ws.addInvoice(invoiceHeader = 'temp')
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_header = ?', self.UserShop2.userId, 'temp')
        modInvNormal = ws.modifyInvoice(invoiceId = invoiceNormal.invoice_id, invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(modInvNormal.model['success'], '5')

    # S6.修改其他人的普通发票
    def test_modifyInvoice_normalOther(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        modInvNormal = ws.modifyInvoice(invoiceId = '08d78a452140460da15c3fe32ac39d5b', invoiceHeader = self.UserShop2.invoiceHeader)
        self.assertEqual(modInvNormal.model['success'], '3')



    # S1.修改增值税发票为最小值
    def test_modifyInvoice_vatMin(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        invoiceVat = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N012')
        modInvVatMin = ws.modifyInvoice(invoiceId = invoiceVat.invoice_id, invoiceType = 'N012', companyName =self.UserShopMin.companyName, taxpayerRegistrationNumber =self.UserShopMin.taxpayerRegistrationNumber, registerAddress =self.UserShopMin.registerAddress,
                                  registerTel = self.UserShopMin.registerTel, depositBank =self.UserShopMin.depositBank, accountBank =self.UserShopMin.accountBank,
                                  receiveManName =self.UserShopMin.receiveManName, receiveManTel =self.UserShopMin.receiveManTel, receiveManProvince = self.UserShopMin.receiveManProvince,
                                  receiveManAddress = self.UserShopMin.receiveManAddress)
        self.assertEqual(modInvVatMin.model['success'], '0')


    # S2.修改增值税发票为最大值——错误 #5360
    def test_modifyInvoice_vatMax(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        invoiceVat = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N012')
        modInvVatMax = ws.modifyInvoice(invoiceId = invoiceVat.invoice_id, invoiceType = 'N012', companyName =self.UserShopMax.companyName, taxpayerRegistrationNumber =self.UserShopMax.taxpayerRegistrationNumber, registerAddress =self.UserShopMax.registerAddress,
                                  registerTel = self.UserShopMax.registerTel, depositBank =self.UserShopMax.depositBank, accountBank =self.UserShopMax.accountBank,
                                  receiveManName =self.UserShopMax.receiveManName, receiveManTel =self.UserShopMax.receiveManTel, receiveManProvince = self.UserShopMax.receiveManProvince,
                                  receiveManAddress = self.UserShopMax.receiveManAddress)
        self.assertEqual(modInvVatMax.model['success'], '0')

    # S3.修改增值税发票字段为空

    # S4.修改增值税发票字段超过最大值


    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?', self.UserShop2.userId)

    # 查询普通发票成功验证方法
    def assertGetNormalSuccess(self, rsp, invoice, code = 200, success = '0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['normalInvoiceList'][0]['invoiceType'], 'N011')
        self.assertEqual(rsp.model['normalInvoiceList'][0]['invoiceHeader'], invoice['invoiceHeader'])
        self.assertEqual(rsp.model['normalInvoiceList'][0]['isDefault'], '0')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(modifyInvoice("test_modifyInvoice_normal"))
    suite.addTest(modifyInvoice("test_modifyInvoice_normalNotExist"))
    suite.addTest(modifyInvoice("test_modifyInvoice_normalNull"))
    suite.addTest(modifyInvoice("test_modifyInvoice_normalUp"))
    suite.addTest(modifyInvoice("test_modifyInvoice_normalRep"))
    suite.addTest(modifyInvoice("test_modifyInvoice_normalOther"))
    suite.addTest(modifyInvoice("test_modifyInvoice_vatMin"))
    suite.addTest(modifyInvoice("test_modifyInvoice_vatMax"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'suite')