#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GJ03.拆分订单（新增）
http://127.0.0.1:8080/mallws/orders/separateOrder.json
{
    "token":"123",                          // 必须
    "orderNo":"10621581690013",                  // 必须 订单号
    "separateOrderAmount":[                 // 每个子订单的拆分金额（单位：分）
        "50000",
        "200000",
        "5000"
        ]
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                     // 成功 0-成功      1-不成功    2-您还有剩余金额未拆分    3-该订单状态不支持拆分  4-订单限定金额发生变化 5-订单拆分次数发生变化
        "orderNo":"123123123",                              // 订单号
        "paymentList":[
            {
                "separatePaymentNo":"201510021725-A-01",    // 拆分后的支付单号
                "separateOrderAmount":"50000"               // 拆分后的子订单号对应的支付金额(单位：分)
            }
        ]
     },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.SeparateOrderResponse"
    }
}
"""

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *
from www.operation.order import createOrder

class separateOrder(unittest.TestCase):
    UserShop = wsData('TmlShop')
    DealMager = wsData('DealMager')
    DealMager2 = wsData('DealMager2')
    Merch = wsData('Merch1')

    wsDealMager = webservice()
    wsDealMager.login(DealMager.username, DealMager.password)


    # S1.货到付款待发货订单拆分订单(2单)
    def test_separateOrder_separat(self):
        order = createOrder(self.UserShop, self.Merch)
        amount= [str(int(order.price)-100),'100']
        sepOrder = self.wsDealMager.separateOrder(orderNo=order.orderNo, separateOrderAmount=amount)
        self.assertSepOrder(sepOrder, order, amount)

    # S2.货到付款待收货订单拆分订单(10单)
    def test_separateOrder_separatTen(self):
        update('update dlcompany.dl_payment_split_info set max_times= ? where company_id= ?', 10, self.DealMager.companyId)
        order = createOrder(self.UserShop, self.Merch)
        self.wsDealMager.deliver(orderNo=order.orderNo)
        amount = [str(int(order.price)/10),str(int(order.price)/10),str(int(order.price)/10),str(int(order.price)/10),
                str(int(order.price)/10),str(int(order.price)/10),str(int(order.price)/10),str(int(order.price)/10),str(int(order.price)/10),str(int(order.price)/10)]
        sepOrder = self.wsDealMager.separateOrder(orderNo=order.orderNo, separateOrderAmount=amount)
        self.assertSepOrder(sepOrder, order, amount)

    # S3.只拆分一个订单
    def test_separateOrder_separatOne(self):
        order = createOrder(self.UserShop, self.Merch)
        amount = [order.price]
        sepOrder = self.wsDealMager.separateOrder(orderNo=order.orderNo, separateOrderAmount=amount)
        self.assertSepOrder(sepOrder, order, amount)

    # S4.还有未拆分的金额
    def test_separateOrder_separatAmountLess(self):
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitDeliver.price)-100),'99'])
        self.assertEqual(sepOrder.model['success'], '2')


    # S5.订单已取消
    def test_separateOrder_separatCancelOrder(self):
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodCancel.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodCancel.price)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '3')

    # S6.订单已拆分
    def test_separateOrder_separatSepratedOrder(self):
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitReceiveSeparat.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitReceiveSeparat.price)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '1')

    # S7.订单已收货
    def test_separateOrder_separatCompleteOrder(self):
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodComplete.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodComplete.price)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '3')

    # S8.拆分开关关闭
    def test_separateOrder_separatCannot(self):
        update('update dlcompany.dl_payment_split_info set status= ? where company_id= ?', 0, self.DealMager.companyId)
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitDeliver.price)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '1')

    # S9.拆分金额小于门槛
    def test_separateOrder_separatLessAmount(self):
        update('update dlcompany.dl_payment_split_info set min_amount = ? where company_id= ?', 99999999, self.DealMager.companyId)
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitDeliver.price)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '4')

    # S10.拆单次数超过最大次数
    def test_separateOrder_separatMoreTime(self):
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitDeliver.price)/6),str(int(self.UserShop.orderCodWaitDeliver.price)/6),str(int(self.UserShop.orderCodWaitDeliver.price)/6),str(int(self.UserShop.orderCodWaitDeliver.price)/6),
                                                                                              str(int(self.UserShop.orderCodWaitDeliver.price)/6),str(int(self.UserShop.orderCodWaitDeliver.price)/6)])
        self.assertEqual(sepOrder.model['success'], '5')


    # S11.不支持货到付款——不做判断
    def test_separateOrder_separatNoCod(self):
        update('update dlcompany.dl_biz_base_info set isCod = ? where company_id= ?', '0', self.DealMager.companyId)
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitDeliver.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitDeliver.price)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '1')


    # S12.在线支付订单
    def test_separateOrder_separatOnline(self):
        sepOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderOnlineWaitPay.orderNo, separateOrderAmount=[str(int(self.UserShop.orderOnlineWaitPay.totalPrice)-100),'100'])
        self.assertEqual(sepOrder.model['success'], '1')

    # S13.订单改价后拆单
    def test_separateOrder_priceChange(self):
        order = createOrder(self.UserShop, self.Merch)
        self.wsDealMager.changeOrderPrice(orderNo=order.orderNo, orderDiscountAmount='100', orderChangeAmount=str(int(order.price)-100), orderStatus='C020')
        amount= [str(int(order.price)-200),'100']
        sepOrder = self.wsDealMager.separateOrder(orderNo=order.orderNo, separateOrderAmount=amount)
        self.assertSepOrder(sepOrder, order, amount)

    # S14.订单拆单后不允许改价
    def test_separateOrder_separateChangePrice(self):
        changeOrder = self.wsDealMager.changeOrderPrice(orderNo=self.UserShop.orderCodWaitDeliverSeparat.orderNo, orderDiscountAmount='100', orderChangeAmount=str(int(self.UserShop.orderCodWaitDeliverSeparat.price)-100), orderStatus='C020')
        # changeOrder = self.wsDealMager.separateOrder(orderNo=self.UserShop.orderCodWaitDeliverSeparat.orderNo, separateOrderAmount=[str(int(self.UserShop.orderCodWaitDeliverSeparat.price)-100),'100'])
        self.assertEqual(changeOrder.model['success'], '1')

    def tearDown(self):
        update('update dlcompany.dl_payment_split_info set status= ?, max_times= ?, min_amount= ? where company_id= ?', 1, self.DealMager.separateOrderTimes, self.DealMager.separateMinAmount, self.DealMager.companyId)
        update('update dlcompany.dl_biz_base_info set isCod = ? where company_id= ?', '1', self.DealMager.companyId)

    def assertSepOrder(self, rsp, order, amount):
        orderDB = select('select * FROM dlpay.dl_payment_split_order where pay_no = ?', order.paymentNo)

        self.assertEqual(rsp.model['success'], '0')
        self.assertEqual(rsp.model['orderNo'], order.orderNo)
        self.assertEqual(len(rsp.model['paymentList']), len(orderDB))
        for i in range(0, len(rsp.model['paymentList'])):
            for j in range(0, len(orderDB)):
                if rsp.model['paymentList'][i]['separatePaymentNo'] == orderDB[j]['pay_order_no']:
                    for k in range(0, len(amount)):
                        if rsp.model['paymentList'][i]['separateOrderAmount']==amount[k]:
                            amount.remove(amount[k])
                            break
                    break
        self.assertEqual(amount, [])




def suite():
    suite=unittest.TestSuite()
    suite.addTest(separateOrder('test_separateOrder_separat'))
    suite.addTest(separateOrder('test_separateOrder_separatTen'))
    suite.addTest(separateOrder('test_separateOrder_separatOne'))
    suite.addTest(separateOrder('test_separateOrder_separatAmountLess'))
    suite.addTest(separateOrder('test_separateOrder_separatCancelOrder'))
    suite.addTest(separateOrder('test_separateOrder_separatSepratedOrder'))
    suite.addTest(separateOrder('test_separateOrder_separatCompleteOrder'))
    suite.addTest(separateOrder('test_separateOrder_separatCannot'))
    suite.addTest(separateOrder('test_separateOrder_separatLessAmount'))
    suite.addTest(separateOrder('test_separateOrder_separatMoreTime'))
    # 货到付款不做校验
    # suite.addTest(separateOrder('test_separateOrder_separatNoCod'))
    suite.addTest(separateOrder('test_separateOrder_separatOnline'))
    suite.addTest(separateOrder('test_separateOrder_priceChange'))
    suite.addTest(separateOrder('test_separateOrder_separateChangePrice'))
    return suite