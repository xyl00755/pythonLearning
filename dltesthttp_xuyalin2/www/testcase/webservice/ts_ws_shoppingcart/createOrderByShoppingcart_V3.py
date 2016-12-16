#!/usr/bin/env python
# -*- coding: utf-8 -*-

from www.common.database import *
from www.operation.createOrderTool import *
"""
WQ06.生成订单(修改接口)
http://127.0.0.1:8080/mallws/shoppingcart/createOrderByShoppingcart_V3.json
{
    "token": "e54d8c0d993543558062e52195c5c8d4",                        // 必须
    "verfyCode":"1111",                                                 // 短信验证码
    "couponList": [
        {                                                               // 可选优惠券
            "couponCode":"",                                            // 优惠券劵号
            "couponAmt":"",                                             // 优惠劵金额
            "couponUseAmt":"",                                          // 优惠券抵扣金额
        }
    ],
    "deliverAddress": {                                                 // 收货地址模型
        "deliverAddress": "",                                           // 必须 收货地址
        "deliverMobile": "",                                            // 必须 电话
        "deliverPerson": ""                                             // 必须 收货人
    },
    "invoice": {                                                        // 发票模型
        "invoiceId": "",                                                // needInvoice-0 必须 needInvoice-1 不传
        "invoiceType": "",                                              // needInvoice-0 必须 needInvoice-1 不传 N011-普通发票 N012-增值税发票
        "needInvoice": ""                                               // 必须 0-需要发票 1-不要发票
        "invoiceHeader": ""                                             // 普通发票-必须 增值税发票-不需要
    },
    "payWay": "",                                                       // 必须 支付方式 1-在线支付 2-货到付款 12-混合支付 3-公司转帐
    "sellerList": [                                                     // 卖家模型
        {
            "sellerId": "7b632e29789d406595e93246fdb50fa4",             // 必须 卖家id
            "sellerName":"123",                                         // 必须 卖家名
            "isYijipayAccount": "0",                                    // 必须 卖家是否是易极付账户 0-是 1-不是
            "paymentFlag": "0",                                         // 必须 购物车接口的 paymentFlag
            "codFlag": "0",                                             // 必须 购物车接口的 codFlag
            "supportVatInvoice": "0",                                   // 必须 购物车接口的 supportVatInvoice
            "comment":"",                                               // 可选 留言
			"dealerCouponList":[                                        // 可选 经销商红包列表(New)
				{
					"dealerCouponCode":"",                              // 经销商红包编号
					"dealerCouponAmt":"",                               // 经销商红包金额
					"dealerCouponUseAmt":"",                            // 经销商红包抵扣金额
				}
			],
            "merchList": [                                              // 商品列表模型
                {
                    "id": "b8d8f93a5eae48b4a8918f741982d405",           // 必须 购物车主键
                    "merchId": "67d4cb03595348cdacd61000bc96ba03",      // 必须 商品id
                    "merchBarCode": "TM003",                            // 必须 商品条码
                    "promotionId": "",                                  // 可选 促销id
                    "promotionType":"",                                 // 可选 促销类型 0-满赠 1-满减
                    "reductionFlg":"",                                  // 可选 满减类型 0-减单价 1-减总额
                    "promotionDetail":"",                               // 可选 促销详情
                    "ruleId":"123",                                     // 可选 规则
					"dealerBenefit":{	                            // 可选 经销商优惠券列表(New)
						"couponCode":"",								// 经销商优惠券编号
						"couponAmt":"",									// 经销商优惠券金额
						"couponUseAmt":"",								// 经销商优惠券使用金额
					}
                }
            ]
        }
    ]
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success":"0"                                       // 成功 0-成功 1-重复提交订单 2-校验失败 3-下单失败
        "validateResult":"0",                               // 成功 0-验证成功  1-验证失败 2-验证码为空  5-验证码失效  4-不需要验证码
        "failedReasons": {                                  // 去结算失败 返回的失败原因
            "lessThanMiniStartSaleQuantityList": [          // 商品数量小于最小起售量 提示："以上商品最小起购量发生变化，请先查看最新信息"
                "商品名"
            ],
            "invalidList": [                                // 无售卖权或无价格 提示："以上商品已失效，无法购买"
                "商品名"
            ],
            "noOnHandInventoryList": [                      // 有库存但不足 提示："以上商品库存不足，请修改购买数量"
                "商品名"
            ],
            "noSupplyInvoicList": [                         // 选择需要结算的商品对应的配送商如果由支持"开增值税发票"变为不支持 提示："以上配送商不再支持开增值税票，请查看最新信息"
                "店铺名"
            ],
            "priceChangedList": [                           // 价格变动 提示："以上商品价格变动，请先查看最新价格"
                "商品名"
            ],
            "supplyCodPaymentChangedList": [                // 支付方式变化（增加或取消货到付款） 提示："以上配送商支付方式发生变动，请先查看最新信息"
                "店铺名"
            ],
            "goodsPromotionValidateFailList": [             // 促销活动已失效 提示："所选择促销活动已失效，请查看最新信息！"
                "商品名"
            ],
            "couponErrorMessage": "红包状态异常"

        },
        "createOrderInfoModel": {                               // 数据验证成功模型
            "leftShoppingcartSize":"0",                         // 购物车剩余商品类型数量
            "onlinePaymentModel": {                             // 在线支付订单模型
                "paymentNo":"123",                              // 大订单号
                "payType":"123",                                // 支付类型
                "totalPrice":"123",                             // 总价
                "orderNoList": [                                // 子订单号列表
                    "123"
                ]
            },
            "cashOnDeliveryModelList": [                        // 货到付款订单模型
                {
                    "paymentNo":"123",                          // 大订单号
                    "orderNo":"123",                            // 子订单号
                    "price":"123"                               // 总价
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.createOrderByShoppingcartNewResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
param说明:
    发票模型中 如果开发票 则needInvoice为0 invoiceId/invoiceType必传 如果不开发票 needInvoice为1 invoiceId/invoiceType不传
result说明:
    当success字段为0时 createOrderInfoModel模型有值 当success字段为1时 两个大模型都没有值 当success为2时 failedReasons模型有值 当success为3时 下单失败
    onlinePaymentModel/cashOnDeliveryModelList如果无值 返回null

"""

import unittest

class createOrderByShoppingcart_V3(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')
    orderTool = createOrderTool()

    def setUp(self):
        self.orderTool.resetDataBySql()

    #从购物车提交一个商品无促销、优惠券、红包、发票的货到付款的订单(不开发票)
    def creatOrderCashOneNoInvoice(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='1',goodsNum=1,dealerNum=1,type=0)
        self.assertEqual(createOrder.model['success'],'0')
        self.assertEqual(createOrder.model['validateResult'],'4')
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

        # 校验收货地址是否是提交的收货地址
        orderDetailDb = select_one('select * from dlorder.dl_order_orderdetail where order_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderDetailDb.buyer_id, self.UserShop.companyId)
        self.assertEqual(orderDetailDb.receive_person, self.UserShop.deliverPerson)
        self.assertEqual(orderDetailDb.receive_tel, self.UserShop.deliverMobile)
        self.assertEqual(orderDetailDb.receive_address, self.UserShop.deliverAddress)

        # 校验商品是否是提交的商品
        orderItemDb = select_one('select * from dlorder.dl_order_orderitem where order_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderItemDb.merchandise_id, self.Merch1.goodsId)
        self.assertNotEqual(orderItemDb.num, 0)

    #从购物车提交一个经销商下的两个商品无促销、优惠券、红包的货到付款的订单（开发票）
    def creatOrderCashTwoGoodsOneDeliver(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=2,dealerNum=1,type=0)
        self.assertEqual(createOrder.model['success'],'0')
        self.assertEqual(createOrder.model['validateResult'],'4')
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))
        # 校验发票是否是提交的发票
        orderInvoiceDb = select_one('select * from dlorder.dl_order_orderinvoice where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        self.assertEqual(orderInvoiceDb.invoice_header,self.UserShop.invoiceHeader )
        #校验是否是提交了两个商品
        orderItemDb = select_int('select count(*) from dlorder.dl_order_orderitem where order_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderItemDb,2)

    #从购物车提交两个经销商的两个商品的无促销、优惠券、红包的货到付款的订单
    def creatOrderCashTwoGoodsTwoDeliver(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=2,dealerNum=2,type=0)
        self.assertEqual(createOrder.model['success'],'0')
        self.assertEqual(createOrder.model['validateResult'],'4')
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][1]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][1]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][1]['price']))

    #从购物车提交一个商品无促销、优惠券、红包的在线支付订单
    def creatOrderOnLineOne(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='1',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=0)
        self.assertEqual(createOrder.model['success'],'0')
        self.assertEqual(createOrder.model['validateResult'],'4')
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['onlinePaymentModelList'][0]['paymentNo'])
        # 支付方式为在线支付
        self.assertEqual(orderInfoDb.pay_type, '1')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['onlinePaymentModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['onlinePaymentModelList'][0]['totalPrice']))

        # 校验发票是否是提交的发票
        orderInvoiceDb = select_one('select * from dlorder.dl_order_orderinvoice where pay_no = ?', createOrder.model['createOrderInfoModel']['onlinePaymentModelList'][0]['paymentNo'])
        self.assertEqual(orderInvoiceDb.invoice_header, self.UserShop.invoiceHeader)

        # 校验收货地址是否是提交的收货地址
        orderDetailDb = select_one('select * from dlorder.dl_order_orderdetail where order_no = ?', createOrder.model['createOrderInfoModel']['onlinePaymentModelList'][0]['orderNo'])
        self.assertEqual(orderDetailDb.buyer_id, self.UserShop.companyId)
        self.assertEqual(orderDetailDb.receive_person, self.UserShop.deliverPerson)
        self.assertEqual(orderDetailDb.receive_tel, self.UserShop.deliverMobile)
        self.assertEqual(orderDetailDb.receive_address, self.UserShop.deliverAddress)

        # 校验商品是否是提交的商品
        orderItemDb = select_one('select * from dlorder.dl_order_orderitem where order_no = ?', createOrder.model['createOrderInfoModel']['onlinePaymentModelList'][0]['orderNo'])
        self.assertEqual(orderItemDb.merchandise_id, self.Merch1.goodsId)
        self.assertNotEqual(orderItemDb.num, 0)

    #低于起售量提交订单
    def creatOrderInitQuantity(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=1,goodsStatus=01)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['lessThanMiniStartSaleQuantityList'][0],self.Merch1.fullName)

    #商品无价格
    def creatOrderNoPrice(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=2,goodsStatus=01)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['invalidList'][0],self.Merch1.fullName)

    #商品库存不足
    def creatOrderNoInventory(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=3,goodsStatus=01)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['invalidList'][0],self.Merch1.fullName)

    #商品价格变更
    def creatOrderChangePrice(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=4,goodsStatus=01)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['priceChangedList'][0],self.Merch1.fullName)

    #配送商支付方式变更
    def creatOrderChangePayWay(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=5,goodsStatus=01)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['supplyCodPaymentChangedList'][0],self.Merch1.sellerName)

    #商品已下架
    def creatOrderGoodsUnder(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=6,goodsStatus=2)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['invalidList'][0],self.Merch1.fullName)

    #商品已锁定
    def creatOrderGoodsLock(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=6,goodsStatus=3)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['invalidList'][0],self.Merch1.fullName)

    #商品已删除
    def creatOrderGoodsDelete(self):
        createOrder=self.orderTool.createOrderNoPromotion(payWay='2',orderTotalAmt='120',needInvoice='0',goodsNum=1,dealerNum=1,type=1,reason=6,goodsStatus=99)
        self.assertEqual(createOrder.model['success'],'2')
        self.assertEqual(createOrder.model['failedReasons']['invalidList'][0],self.Merch1.fullName)

    #提交使用满减减单价的促销商品的订单
    def creatOrderReduction01(self):
        createOrder=self.orderTool.createOrderPromotion(merchCount='1',orderTotalAmt='120',promotionType=1,reductionType='0',ruleId=self.Merch1.ruleId3)
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    #提交使用满减减总价的促销商品的订单
    def creatOrderReduction02(self):
        createOrder=self.orderTool.createOrderPromotion(merchCount='1',orderTotalAmt='120',promotionType=1,reductionType='1',ruleId=self.Merch1.ruleId4)
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    #提交使用每满减减单价的促销商品的订单
    def creatOrderReduction03(self):
        createOrder=self.orderTool.createOrderPromotion(merchCount='3',orderTotalAmt='120',promotionType=1,reductionType='0',ruleId=self.Merch1.ruleId1)
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    #提交使用每满减减总价的促销商品的订单
    def creatOrderReduction04(self):
        createOrder=self.orderTool.createOrderPromotion(merchCount='3',orderTotalAmt='120',promotionType=1,reductionType='1',ruleId=self.Merch1.ruleId2)
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    #提交使用满赠的促销商品的订单
    def creatOrderReduction05(self):
        createOrder=self.orderTool.createOrderPromotion(merchCount='1',orderTotalAmt='120',promotionType=0,reductionType='-1',ruleId=self.Merch1.ruleId5)
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    #提交使用每满赠的促销商品的订单
    def creatOrderReduction06(self):
        createOrder=self.orderTool.createOrderPromotion(merchCount='2',orderTotalAmt='120',promotionType=0,reductionType='-1',ruleId=self.Merch1.ruleId6)
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(createOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    #提交使用经销商红包以及优惠券的订单
    def creatOrderCoupon(self):
        creatOrder=self.orderTool.creatOrderCoupon(orderTotalAmt='120')
        # 校验订单号和交易号是否匹配
        orderInfoDb = select_one('select * from dlorder.dl_order_orderinfo where pay_no = ?', creatOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'])
        # 支付方式为货到付款
        self.assertEqual(orderInfoDb.pay_type, '2')
        self.assertEqual(orderInfoDb.order_no, creatOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'])
        self.assertEqual(orderInfoDb.order_amount, int(creatOrder.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']))

    def tearDown(self):
        self.orderTool.resetDataBySql()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(createOrderByShoppingcart_V3("creatOrderCashOneNoInvoice"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderCashTwoGoodsOneDeliver"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderCashTwoGoodsTwoDeliver"))
    #suite.addTest(createOrderByShoppingcart_V3("creatOrderOnLineOne"))

    #suite.addTest(createOrderByShoppingcart_V3("creatOrderInitQuantity"))
    #suite.addTest(createOrderByShoppingcart_V3("creatOrderNoPrice"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderNoInventory"))
    #suite.addTest(createOrderByShoppingcart_V3("creatOrderChangePrice"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderChangePayWay"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderGoodsUnder"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderGoodsLock"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderGoodsDelete"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderReduction01"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderReduction02"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderReduction03"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderReduction04"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderReduction05"))
    suite.addTest(createOrderByShoppingcart_V3("creatOrderReduction06"))
    #suite.addTest(createOrderByShoppingcart_V3("creatOrderCoupon"))


    return suite



