#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlmall import *
from www.common.excel import *
from www.common.database import *

"""
/Dlordersettlement/orderBook.html

request:
post
response:json string
{
    "address": {
        "name": "唐先生",
        "tel": "18133664499",
        "address": "四川-成都市-高新区环球中心E1区"
    },
    "invoiceAndPay": {
        "invoiceFlag": "1",
        "invoiceType": "1",
        "invoiceId": "5482720f5503463aa930a3e373d3efd6",
        "payWay": "1"
    },
    "dlCouponList": [
        {
            "couponId": "114612483200015",
            "couponAmt": 600,
            "couponUseAmt": 600
        }
    ],
    "settlementInfo": [
        {
            "businessCompanyId": "5482720f5503463aa930a3e373d3efd6",
            "isCompanySupplyInvoice": "1",
            "storeId": "2419f617b9e441ba993dbc9c190db379",
            "isStoreCOD": "1",
            "isStorePayOnline": "1",
            "commtent": "给卖家留言",
            "dealerCoupon": [
                {
                    "dealerCouponId": "114612483200015",
                    "dealerCouponAmt": 600,
                    "dealerCouponUseAmt": 600
                }
            ],
            "goods": [
                {
                    "id": "b142d19369ee4fd1b5f34736f51d4f73",
                    "goodsId": "24df3ab5b628496aa0fdded6c4230fec",
                    "barCode": "6902212052300",
                    "ruleId": "fa84e44a29394114a5edfaf413593a6d",
                    "promotionId": "7e41134aaa4a4282a8856a8cdb1e0552",
                    "promotionType": "1",
                    "reductionFlg": "0",
                    "promotionDetail": "每满1瓶，总价减50元",
                    "dealerBenefit": {
                        "dealerBenefitId": "114612483200015",
                        "dealerBenefitAmt": 600,
                        "dealerBenefitUseAmt": 600
                    }
                }
            ]
        }
    ]
}
"""

class orderBook(unittest.TestCase):
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

    def orderBook(self,datalist):
        orderbook = self.dlservice.orderBook(s,datalist[0],datalist[1],datalist[2],datalist[3])
        self.doubleorder.append(orderbook['status'])
        self.assertEqual(self.doubleorder[0]+self.doubleorder[1],1)

    #重复提交，校验失败
    def test_doubleorder(self):
        datalist= self.orderInfo()
        threads = []
        t1 = threading.Thread(target=orderBook,args=(datalist))
        threads.append(t1)
        t2 = threading.Thread(target=orderBook,args=(datalist))
        threads.append(t2)
        for t in threads:
            t.setDaemon(True)
            t.start()

    #终端店开具增值税发票资格发生变化，检查错误返回值是否为1

    def test_invoiceType_change(self):
        datalist=self.orderInfo(invoiceType=0)
        orderbook=self.dlservice.orderBook(s,datalist[0],datalist[1],datalist[2],datalist[3])
        self.assertEqual(orderbook['data']['checkErrorObj']['checkErrorType'],1)

    #支付方式发生变化，检查错误返回值是否为2

    def test_payWay_change(self):
        datalist=self.orderInfo(payWay=2)
        orderbook=self.dlservice.orderBook(s,datalist[0],datalist[1],datalist[2],datalist[3])
        self.assertEqual(orderbook['data']['checkErrorObj']['checkErrorType'],2)

    #商品失效，检查错误返回值为3

    def test_goodsId_change(self):
        datalist=self.orderBook(goodsId=None)
        orderbook=self.dlservice.orderBook(s,datalist[0],datalist[1],datalist[2],datalist[3])
        self.assertEqual(orderbook['data']['checkErrorObj']['checkErrorType'],3)

    #促销活动已失效,检查错误返回值为7

    def test_promotionId_change(self):
        datalist=self.orderBook(promotionId=None)
        orderbook=self.dlservice.orderBook(s,datalist[0],datalist[1],datalist[2],datalist[3])
        self.assertEqual(orderbook['data']['checkErrorObj']['checkErrorType'],7)

    #所选红包状态变动,检查错误返回值为8
        datalist=self.orderBook(couponId=None)
        orderbook=self.dlservice.orderBook(s,datalist[0],datalist[1],datalist[2],datalist[3])
        self.assertEqual(orderbook['data']['checkErrorObj']['checkErrorType'],8)







