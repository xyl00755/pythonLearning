#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/Dlordertransfer/toTransferPage.html

request: data form
post
status=1
checkErrorObj=[{"checkErrorContent":["经销商1","经销商2","经销商3"],"checkErrorType":"1"}]
onlinePay=
cashOndelivery=[{"amount":104565,"orderNo":"20630385260027","payNo":"80630385260028","payType":"2"},{"amount":39835,"orderNo":"20630385260029","payNo":"80630385260030","payType":"2"},{"amount":40,"orderNo":"20630385270031","payNo":"80630385270032","payType":"2"}]
companyTransfer=

response:返回页面

"""

class toTransferPage(unittest.TestCase):
    UserShop = eData('WebManager')
    orderBookInfo=eData('orderBook')
    dlservice = dlmall()
    s = dlservice.login(UserShop.buyer_username,UserShop.buyer_password)
    doubleorder =[]

    def orderInfo(self,invoiceType=orderBookInfo.invoiceType,payWay=orderBookInfo.payWay,couponId=orderBookInfo.couponId,goodsId=orderBookInfo.goodsId,dealerBenefitId=orderBookInfo.dealerBenefitId,promotionId=orderBookInfo.promotionId):
        datalist = [
            {
            'name': self.orderBookInfo.name,
            'tel': self.orderBookInfo.tel,
            'address': self.orderBookInfo.address
            },
            {
                'invoiceFlag': self.orderBookInfo.invoiceFlag,
                'invoiceType': invoiceType,
                'invoiceId': self.orderBookInfo.invoiceId,
                'payWay': payWay
            },
            {
                'couponId': couponId,
                'couponAmt': self.orderBookInfo.couponAmt,
                'couponUseAmt': self.orderBookInfo.couponUseAmt
            },
            {
                'businessCompanyId': self.orderBookInfo.businessCompanyId,
                'isCompanySupplyInvoice': self.orderBookInfo.isCompanySupplyInvoice,
                'storeId': self.orderBookInfo.storeId,
                'isStoreCOD': self.orderBookInfo.isStoreCOD,
                'isStorePayOnline': self.orderBookInfo.isStorePayOnline,
                'commtent': self.orderBookInfo.commtent,
                'dealerCoupon': [{
                    'dealerCouponId': self.orderBookInfo.dealerCouponId,
                    'dealerCouponAmt': self.orderBookInfo.dealerCouponAmt,
                    'dealerCouponUseAmt': self.orderBookInfo.dealerCouponUseAmt
                }],
                'goods': [{
                    'id': self.orderBookInfo.id,
                    'goodsId': goodsId,
                    'barCode': self.orderBookInfo.barCode,
                    'ruleId': self.orderBookInfo.ruleId,
                    'promotionId': promotionId,
                    'promotionType': self.orderBookInfo.promotionType,
                    'reductionFlg': self.orderBookInfo.reductionFlg,
                    'promotionDetail': self.orderBookInfo.promotionDetail,
                    'dealerBenefit': {
                        'dealerBenefitId': dealerBenefitId,
                        'dealerBenefitAmt': self.orderBookInfo.dealerBenefitAmt,
                        'dealerBenefitUseAmt': self.orderBookInfo.dealerBenefitUseAmt
                    }

                }]
            }]
        return datalist


    #验证正确返回页面
    def test_toTransferPage_success(self):
        datalist= self.orderInfo()
        status=self.dlservice.toTransferPage(s,status=datalist['status'],onlinePay=datalist['onlinePay'],cashOndelivery=datalist['cashOndelivery'],companyTransfer=datalist['companyTransfer'])
        self.assertEqual(status,200)

