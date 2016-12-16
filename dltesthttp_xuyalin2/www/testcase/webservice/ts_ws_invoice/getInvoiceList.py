#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0204.发票列表
http://127.0.0.1:8280/mallws/mydl/invoice/getInvoiceList.json
{
    "token":"66dc3c0d3cf7408c8d1845b9448a0e37"                              // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                     // 成功 0-成功
        "normalInvoiceList": [                                              // 普通发票列表
            {
                "customerId": "76fc5f07fcef421a9cd4b9cb17ca1f27",           // 用户id
                "invoiceId": "c9f0150a179e43c5a5bbd7566a94c13a",            // 发票id
                "invoiceType": "N011",                                      // 发票类型 N011-普通发票 N012-增值税发票
                "invoiceHeader": "DHC",                                     // 发票抬头
                "companyName": "",
                "taxpayerRegistrationNumber": "",
                "registerAddress": "",
                "registerTel": "",
                "depositBank": "",
                "accountBank": "",
                "accountLicence": "",
                "isDefault": "0",                                           // 是否默认 0-默认 1-非默认
                "receiveManName": null,
                "receiveManTel": null,
                "receiveManProvince": null,
                "receiveManAddress": null
            }
        ],
        "vatInvoice": {                                                   // 增值税发票
            "customerId": "76fc5f07fcef421a9cd4b9cb17ca1f27",             // 用户id
            "invoiceId": "4ec418ce99544c619bdfbb0a7ce9a9d8",              // 发票id
            "invoiceType": "N012",                                        // 发票类型 N011-普通发票 N012-增值税发票
            "invoiceHeader": "",
            "companyName": "大连DHC",                                     // 公司名称
            "taxpayerRegistrationNumber": "2234332223",                   // 纳税人识别号
            "registerAddress": "辽宁省大连市",                            // 注册地址
            "registerTel": "13478464122",                                 // 注册电话
            "depositBank": "建设银行",                                    // 开户银行
            "accountBank": "324485858493939239383849494393",              // 帐户银行
            "accountLicence": "",                                         // 开户许可证
            "isDefault": null,                                            // 是否默认 0-默认 1-非默认
            "receiveManName": null,                                       // 收票人姓名
            "receiveManTel": null,                                        // 收票人电话
            "receiveManProvince": null,                                   // 收票人省份
            "receiveManAddress": null                                     // 收票人详细地址
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.invoice.InvoiceListResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class getInvoiceList(unittest.TestCase):

    UserDealMgr = wsData('DealMager')
    UserShop2 = wsData('TmlShop2')


    # S1.有发票时获取发票列表
    def test_getInvList_invoice(self):
        ws = webservice()
        ws.login(self.UserDealMgr.username, self.UserDealMgr.password)
        gilInvoice = ws.getInvoiceList()
        invoiceNormal = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserDealMgr.userId, 'N011')
        invocieVat = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserDealMgr.userId, 'N012')
        self.assertGetNormalSuccess(gilInvoice, invoiceNormal)
        self.assertGetVatSuccess(gilInvoice, invocieVat)

    # S2.无发票时获取发票列表
    def test_getInvList_null(self):
        ws2 = webservice()
        dlShop2 = ws2.login(self.UserShop2.username, self.UserShop2.password)
        gilTnull = ws2.getInvoiceList()
        self.assertEqual(gilTnull.model['success'], '0')
        self.assertEqual(gilTnull.model['normalInvoiceList'], [])
        self.assertIsNone(gilTnull.model['vatInvoice'])

    # S3.发票数量最大时获取发票列表
    def test_getInvoice_Max(self):
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
        ws.addInvoice(invoiceType = 'N012', companyName =self.UserShop2.companyName, taxpayerRegistrationNumber =self.UserShop2.taxpayerRegistrationNumber, registerAddress =self.UserShop2.registerAddress,
                                  registerTel = self.UserShop2.registerTel, depositBank =self.UserShop2.depositBank, accountBank =self.UserShop2.accountBank,
                                  receiveManName =self.UserShop2.receiveManName, receiveManTel =self.UserShop2.receiveManTel, receiveManProvince = self.UserShop2.receiveManProvince,
                                  receiveManAddress = self.UserShop2.receiveManAddress)
        addInvNormalMoreList = ws.getInvoiceList()
        self.assertEqual(len(addInvNormalMoreList.model['normalInvoiceList']), 15)
        invocieVat = select_one('select * from dlcompany.dl_biz_invoices where user_id = ? and invoice_type = ?', self.UserShop2.userId, 'N012')
        self.assertGetVatSuccess(addInvNormalMoreList, invocieVat)


    def tearDown(self):
        update('delete from dlcompany.dl_biz_invoices where user_id = ?', self.UserShop2.userId)

    # 查询普通发票成功验证方法
    def assertGetNormalSuccess(self, rsp, invoice, code = 200, success = '0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['normalInvoiceList'][0]['invoiceType'], 'N011')
        self.assertEqual(rsp.model['normalInvoiceList'][0]['invoiceHeader'], invoice['invoice_header'])
        self.assertEqual(rsp.model['normalInvoiceList'][0]['isDefault'], self.realDefault(invoice['is_default']))

    # 查询增值发票成功验证方法
    def assertGetVatSuccess(self, rsp, invoice, code = 200, success = '0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['vatInvoice']['invoiceType'], 'N012')
        self.assertEqual(rsp.model['vatInvoice']['companyName'], invoice['company_name'])
        self.assertEqual(rsp.model['vatInvoice']['taxpayerRegistrationNumber'], invoice['taxpayer_reg_no'])
        self.assertEqual(rsp.model['vatInvoice']['registerAddress'], invoice['register_address'])
        self.assertEqual(rsp.model['vatInvoice']['registerTel'], invoice['register_tel'])
        self.assertEqual(rsp.model['vatInvoice']['depositBank'], invoice['deposit_bank'])
        self.assertEqual(rsp.model['vatInvoice']['accountBank'], invoice['account_bank'])
        self.assertEqual(rsp.model['vatInvoice']['isDefault'], self.realDefault(invoice['is_default']))
        self.assertEqual(rsp.model['vatInvoice']['receiveManName'], invoice['receive_man_name'])
        self.assertEqual(rsp.model['vatInvoice']['receiveManTel'], invoice['receive_man_tel'])
        self.assertEqual(rsp.model['vatInvoice']['receiveManProvince'], invoice['receive_man_province'])
        self.assertEqual(rsp.model['vatInvoice']['receiveManAddress'], invoice['receive_man_address'])

    # 数据库中的默认和真实默认不一致，所以需要real一下
    def realDefault(self, is_default):
        if(is_default=='0'):
            return '1'
        elif(is_default=='1'):
            return '0'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getInvoiceList("test_getInvList_invoice"))
    suite.addTest(getInvoiceList("test_getInvList_null"))
    suite.addTest(getInvoiceList("test_getInvoice_Max"))
    return suite


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'suite')