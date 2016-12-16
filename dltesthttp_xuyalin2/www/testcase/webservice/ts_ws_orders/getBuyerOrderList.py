#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0041.获取买家订单列表
http://127.0.0.1:8280/mallws/orders/getBuyerOrderList.json
{
    "token":"123",                          // 必须
    "orderStatus":"???",                    // 必须 订单状态 0-全部 C011-待付款 C020-待发货 C017-待收货 C019-已完成 C012-已取消
    "startTime":"2015-09-09",               // 可选 起始时间 yyyy-MM-dd 格式
    "endTime":"2015-12-12",                 // 可选 结束时间 yyyy-MM-dd 格式
    "page":1,                               // 必须
    "rows":15                               // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                     // 成功 0-成功
        "paymentOrderList": [                               // 大订单列表
            {
                "paymentNo": "201510021725-A",              // 大订单号
                "placeOrderTime":"",                        // 下单时间
                "payType":"1",                              // 支付类型 1-在线支付 2-货到付款 3-公司转帐
                "paymentOrderMerchCount":"123",             // 大订单商品总数
                "paymentOrderTotalPrice":"123",             // 大订单总价
                "paymentOrderButtomList":"123",             // 详见解释
				"paymentPayStatus": "123"                   // 订单状态
				"payStatus2Middle": "123"					// 订单状态 P012-支付结果确认中 P009-退款结果确认中
                "orderList": [                              // 小订单列表
                    {
                        "orderId": null,                    // 小订单主键
                        "orderNo": "201510021725-A-01",     // 小订单号
                        "paymentNo": "201510021725-A",      // 大订单号
						"payWay": "00",                     // 支付通道
                        "orderStatus": "C011",              // 小订单状态 C011-待付款 C020-待发货 C017-待收货 C019-已完成 C012-已取消 C015-已退款
                        "cancelStatus":"0",                 // 取消状态 0-正常状态 1-取消中状态 2-已同意取消状态 3-已拒绝取消状态
                        "errorStatus":"0",                  // 异常状态 0-交易异常 1-交易正常
                        "receiveStatus":"0",                // 收货状态 0-未收货 1-已收货
                        "payType":"1",                      // 支付方式 1-在线支付 2-货到付款 3-公司转帐
                        "totalPrice": "1595000",            // 小订单总价
						"orderRetailAmount":"1000",			//订单原始金额 add by zhangwanquan
                        "isUseCoupon": "1",                 // 是否使用优惠券 0-使用 1-未使用
                        "couponFeeCount": "0",              // 优惠券优惠总额
                        "orderMerchCount":"123",            // 小订单商品总数
						"sellerId": "123",                  // 卖家id
						"sellerName": "123",                // 卖家名
						"isYijipayAccount": "0",            // 卖家是否支持易极付 "0"-支持 "1"-不支持
                        "buttomList":"123",                 // 详见解释
                        "promotionList": [                  // 促销列表
                            {
                                "promotionType": "0",       // 促销类型 0-满增 1-满降
                                "promotionDetail": "123123123",  // 促销详情
                                "reduceValue":"123"         // 满减优惠
                                "reduceType":"1",           // 满减类型 0-减单 1-减总
                            }
                        ],
                        "merchList": [                      // 商品列表
                            {
                                "merchId": "010555639",     // 商品主键
                                "merchName": "云南泸州老窖100年陈酿500ML特惠",     // 商品名
                                "merchBarCode": null,       // 商品条码
                                "merchCount": "5",          // 商品数量
                                "picUrl": null,             // 图片URL
                                "merchSpec": "2瓶/盒",      // 商品规格
                                "costPrice": null,          // 原价 (上面划掉的那个)
                                "unitPrice": "32000",       // 单价
                                "promotionType":"1"         // 促销类型 -1-没有促销 0-满赠 1-满减【包括满减单、满减总，具体见promotionList】
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.OrderListResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    一个订单有多少个促销(满降满赠) 都放在promotionList中
    1. 如果是满赠 则promotionDetail有一句话 而且商品的costPrice和unitPrice相等
    2. 如果使满降 减总额 则promotionDetail有一句话 reduceValue有减去的总价 而且商品的costPrice和unitPrice相等
    3. 如果使满降 减单价 则promotionDetail有一句话 而且商品的costPrice和unitPrice不相等
    如果是否使用优惠券isUseCoupon为1 则没有使用优惠券 优惠券金额couponFeeCount没有
    所有金额相关单位均为分

    paymentOrderButtomList 为买家大订单下应该有的按钮列表(卖家没有) 结构为 01010 一共五位数
    buttomList 为买家/卖家小订单下应该有的按钮列表 结构为 010101 一共五位数
    第一位 0-没有付款按钮 1-有付款按钮
    第二位 0-没有发货按钮 1-有发货按钮
    第三位 0-没有收货按钮 1-有收货按钮
    第四位 0-没有取消按钮 1-有在线支付未付款订单取消按钮(取消交易) 2-有货到付款未发货订单取消按钮(取消交易) 3-有货到付款已发货订单取消按钮(申请取消) 4-有交易取消中标签(交易取消中) 5-有在线支付已付款订单/待收货订单取消按钮(退款取消)
    第五位 0-没有接受/拒绝取消按钮 1-有接受/拒绝取消按钮
    第六位【追加】0-没有订单跟踪按钮 1-有订单跟踪按钮
    第七位【追加】0-没有订单改价按钮 1-有订单改价按钮
    各个子订单的状态根据子订单的orderStatus来判断 是否是正在取消中订单通过cancelStatus来判断 是否是异常订单通过errorStatus来判断


GJ02.订单列表页（终端店）（修改）
http://127.0.0.1:8080/mallws/orders/getBuyerOrderList.json
{
    "token":"123",                          // 必须
    "orderStatus":"???",                    // 必须 订单状态 0-全部 C011-待付款 C020-待发货 C017-待收货 C019-已完成 C012-已取消   C025-支付中
    "startTime":"2015-09-09",               // 可选 起始时间 yyyy-MM-dd 格式
    "endTime":"2015-12-12",                 // 可选 结束时间 yyyy-MM-dd 格式
    "page":1,                               // 必须
    "rows":15                               // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                     // 成功 0-成功
        "paymentOrderList": [                               // 大订单列表
            {
                "paymentNo": "201510021725-A",              // 大订单号
                "placeOrderTime":"",                        // 下单时间
                "payType":"1",                              // 支付类型 1-在线支付 2-货到付款 3-公司转帐
                "paymentOrderMerchCount":"123",             // 大订单商品总数
                "paymentOrderTotalPrice":"123",             // 大订单总价
                "paymentOrderButtomList":"123",             // 详见解释
                "paymentPayStatus": "123"                   // 订单状态
                "payStatus2Middle": "123"                   // 订单状态 P012-支付结果确认中 P009-退款结果确认中
                "orderList": [                              // 小订单列表
                    {
                        "orderId": null,                    // 小订单主键
                        "orderNo": "201510021725-A-01",     // 小订单号
                        "paymentNo": "201510021725-A",      // 大订单号
                        "payWay": "00",                     // 支付通道
                        "orderStatus": "C011",              // 小订单状态 C011-待付款 C020-待发货 C017-待收货 C019-已完成 C012-已取消 C015-已退款  C025-支付中
                        "cancelStatus":"0",                 // 取消状态 0-正常状态 1-取消中状态 2-已同意取消状态 3-已拒绝取消状态
                        "errorStatus":"0",                  // 异常状态 0-交易异常 1-交易正常
                        "receiveStatus":"0",                // 收货状态 0-未收货 1-已收货
                        "payType":"1",                      // 支付方式 1-在线支付 2-货到付款 3-公司转帐
                        "totalPrice": "1595000",            // 小订单总价
                        "orderRetailAmount":"1000",         //订单原始金额 add by zhangwanquan
                        "isUseCoupon": "1",                 // 是否使用优惠券 0-使用 1-未使用
                        "couponFeeCount": "0",              // 优惠券优惠总额
                        "orderMerchCount":"123",            // 小订单商品总数
                        "sellerId": "123",                  // 卖家id
                        "sellerName": "123",                // 卖家名
                        "isYijipayAccount": "0",            // 卖家是否支持易极付 "0"-支持 "1"-不支持
                        "buttomList":"101001010",           // 详见解释
                        "promotionList": [                  // 促销列表
                            {
                                "promotionType": "0",       // 促销类型 0-满增 1-满降
                                "promotionDetail": "123123123",  // 促销详情
                                "reduceValue":"123"         // 满减优惠
                                "reduceType":"1",           // 满减类型 0-减单 1-减总
                            }
                        ],
                        "merchList": [                      // 商品列表
                            {
                                "merchId": "010555639",     // 商品主键
                                "merchName": "云南泸州老窖100年陈酿500ML特惠",     // 商品名
                                "merchBarCode": null,       // 商品条码
                                "merchCount": "5",          // 商品数量
                                "picUrl": null,             // 图片URL
                                "merchSpec": "2瓶/盒",      // 商品规格
                                "costPrice": null,          // 原价 (上面划掉的那个)
                                "unitPrice": "32000",       // 单价
                                "promotionType":"1"         // 促销类型 -1-没有促销 0-满赠 1-满减【包括满减单、满减总，具体见promotionList】
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.GetBuyerOrderListResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    一个订单有多少个促销(满降满赠) 都放在promotionList中
    1. 如果是满赠 则promotionDetail有一句话 而且商品的costPrice和unitPrice相等
    2. 如果使满降 减总额 则promotionDetail有一句话 reduceValue有减去的总价 而且商品的costPrice和unitPrice相等
    3. 如果使满降 减单价 则promotionDetail有一句话 而且商品的costPrice和unitPrice不相等
    如果是否使用优惠券isUseCoupon为1 则没有使用优惠券 优惠券金额couponFeeCount没有
    所有金额相关单位均为分

    paymentOrderButtomList 为买家大订单下应该有的按钮列表(卖家没有) 结构为 01010 一共五位数
    buttomList 为买家/卖家小订单下应该有的按钮列表 结构为 010101 一共五位数
    第一位 0-没有付款按钮 1-有付款按钮
    第二位 0-没有发货按钮 1-有发货按钮
    第三位 0-没有收货按钮 1-有收货按钮
    第四位 0-没有取消按钮 1-有在线支付未付款订单取消按钮(取消交易) 2-有货到付款未发货订单取消按钮(取消交易) 3-有货到付款已发货订单取消按钮(申请取消) 4-有交易取消中标签(交易取消中) 5-有在线支付已付款订单/待收货订单取消按钮(退款取消)
    第五位 0-没有接受/拒绝取消按钮 1-有接受/拒绝取消按钮
    第六位【追加】0-没有订单跟踪按钮 1-有订单跟踪按钮

    第七位【追加】0-没有订单拆分按钮 1-有订单拆分按钮
    第八位【追加】0-没有查看拆分按钮 1-有查看拆分按钮

    各个子订单的状态根据子订单的orderStatus来判断 是否是正在取消中订单通过cancelStatus来判断 是否是异常订单通过errorStatus来判断

"""

import unittest

from www.api.webservice import *
from www.common.database import select_int,select_one
from www.common.excel import wsData


class getBuyerOrderList(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShopMin = wsData('TmlShopMin')
    DealMgr = wsData('DealMager')
    Merch1 = wsData('Merch1')

    wsUserShop = webservice()
    wsUserShop.login(UserShop.username, UserShop.password)
    wsUserShopMin = webservice()
    wsUserShopMin.login(UserShopMin.username, UserShopMin.password)

    # S1.获取终端店买家全部订单
    def test_getBuyerOrderList_all(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='0', startTime='', endTime='', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderdetail where buyer_id = ?', self.UserShop.companyId)
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderCodWaitDeliver, self.Merch1)

    # S2.订单数量为空时获取订单列表
    def test_getBuyerOrderList_null(self):
        buyerOrderList = self.wsUserShopMin.getBuyerOrderList(orderStatus='0', page=1, rows=999999, endTime='1900-01-01')
        self.assertEqual(buyerOrderList.model['success'], '0')
        self.assertEqual(buyerOrderList.model['paymentOrderList'], [])

    # S3.获取待付款订单列表(C011)
    def test_getBuyerOrderList_waitPay(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='C011', startTime='', endTime='', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?) and order_status = ?', self.UserShop.companyId, 'C011')
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderOnlineWaitPay, self.Merch1, payType='1', paymentOrderButtomList='00010', paymentPayStatus='')

    # S4.获取待发货订单列表（C020）
    def test_getBuyerOrderList_waitDeliver(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='C020', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?) and order_status = ?', self.UserShop.companyId, 'C020')
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderCodWaitDeliver, self.Merch1)

    # S5.获取待收货订单列表（C017）
    def test_getBuyerOrderList_waitReceive(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='C017', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?) and order_status = ?', self.UserShop.companyId, 'C017')
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderCodWaitReceive, self.Merch1, paymentOrderButtomList='00030')

    # S6.获取交易完成订单列表（C019）
    def test_getBuyerOrderList_complete(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='C019', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?) and order_status = ?', self.UserShop.companyId, 'C019')
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderCodComplete, self.Merch1, paymentOrderButtomList='00000', payWay='01', receiveStatus='1')

    # S7.获取交易取消订单列表（C012）
    def test_getBuyerOrderList_cancel(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='C012', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?) and order_status = ?', self.UserShop.companyId, 'C012')
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderCodCancel, self.Merch1, paymentOrderButtomList='00000')

    # S8.根据时间查询订单列表
    def test_getBuyerOrderList_time(self):
        import datetime
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d")
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='0', startTime=nowtime, endTime=nowtime, rows=9999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        for i in range(0, len(buyerOrderList.model['paymentOrderList'])):
            self.assertIn(nowtime, buyerOrderList.model['paymentOrderList'][i]['placeOrderTime'])


    # S9.分页查询订单列表
    def test_getBuyerOrderList_page(self):
        orderCount = select_int('select count(*) from dlorder.dl_order_orderdetail where buyer_id = ?', self.UserShop.companyId)
        page = orderCount/15
        flag = 0
        for i in range(1, page+2):
            buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='0', startTime='', endTime='', page=i, rows=15)
            for j in range(0, len(buyerOrderList.model['paymentOrderList'])):
                if buyerOrderList.model['paymentOrderList'][j]['paymentNo'] == self.UserShop.orderCodWaitDeliver.paymentNo:
                    flag += 1
            if i == page+1:
                self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount%15, "The last page is wrong")
            else:
                self.assertEqual(len(buyerOrderList.model['paymentOrderList']),15,"Every page is wrong")

        self.assertEqual(flag, 1, self.UserShop.orderCodWaitDeliver.paymentNo + ' is not once ')

    # S10.获取经销商管理员买家订单列表

    # S11.获取货到付款支付中订单列表（C025）
    def test_getBuyerOrderList_codPaying(self):
        buyerOrderList = self.wsUserShop.getBuyerOrderList(orderStatus='C025', startTime='', endTime='', page=1, rows=999999)
        self.assertEqual(buyerOrderList.model['success'], '0')
        orderCount = select_int('select count(*) from dlorder.dl_order_orderinfo where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?) and order_status = ?', self.UserShop.companyId, 'C025')
        self.assertEqual(len(buyerOrderList.model['paymentOrderList']), orderCount)
        self.assertOrderList(buyerOrderList, self.UserShop.orderCodPayingSeparat, self.Merch1, buttomList='00000001', paymentOrderButtomList='00000')

    def assertOrderList(self, rsq, order, merch, payType='2', payWay=None, paymentOrderButtomList='00020', paymentPayStatus='normal', buttomList='00000000', receiveStatus='0'):
        #paymentOrder = select('select * from dlpay.dl_payment_order where pay_no = ?', order.paymentNo)
        #orderDetail = select('select * from dlorder.dl_order_orderdetail where order_no =', order.orderNo)
        orderInfo = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', order.orderNo)
        orderItem = select_one('select * from dlorder.dl_order_orderitem where order_no = ?', order.orderNo)
        flag = 0
        for i in range(0, len(rsq.model['paymentOrderList'])):
            if rsq.model['paymentOrderList'][i]['paymentNo'] == order.paymentNo:
                self.assertEqual(rsq.model['paymentOrderList'][i]['placeOrderTime'], str(orderInfo.gmt_created))
                self.assertEqual(rsq.model['paymentOrderList'][i]['payType'], payType)
                self.assertEqual(rsq.model['paymentOrderList'][i]['paymentOrderMerchCount'], str(orderItem.num))
                self.assertEqual(rsq.model['paymentOrderList'][i]['paymentOrderTotalPrice'], str(orderItem.amount))
                self.assertEqual(rsq.model['paymentOrderList'][i]['paymentOrderButtomList'], paymentOrderButtomList)
                self.assertEqual(rsq.model['paymentOrderList'][i]['paymentPayStatus'], paymentPayStatus)
                self.assertEqual(rsq.model['paymentOrderList'][i]['payStatus2Middle'], '')
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['orderId'], orderInfo.id)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['orderNo'], order.orderNo)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['paymentNo'], order.paymentNo)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['payType'], orderInfo.pay_type)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['payWay'], payWay)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['errorStatus'], '1')
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['cancelStatus'], '0')
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['receiveStatus'],receiveStatus)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['buttomList'], buttomList)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['orderStatus'], orderInfo.order_status)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['totalPrice'], str(orderInfo.order_retail_amount))
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['orderRetailAmount'], None)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['isUseCoupon'], '1')
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['couponFeeCount'], '0')
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['orderMerchCount'], str(orderItem.num))
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['sellerId'], merch.sellerId)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['sellerName'], merch.sellerName)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['isYijipayAccount'], merch.isYijipayAccount)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['promotionList'], [])
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['merchId'], orderItem.merchandise_id)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['merchName'], orderItem.merchandise_name)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['merchBarCode'], orderItem.merchandise_barcode)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['merchCount'], str(orderItem.num))
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['picUrl'], merch.picUrl)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['merchSpec'], merch[u'包装规格'])
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['costPrice'], merch.unitPrice)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['unitPrice'], merch.unitPrice)
                self.assertEqual(rsq.model['paymentOrderList'][i]['orderList'][0]['merchList'][0]['promotionType'], '-1')
                flag += 1
        self.assertEqual(flag, 1, 'order is not found or is found twice')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_all"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_null"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_waitPay"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_waitDeliver"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_waitReceive"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_complete"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_cancel"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_time"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_page"))
    suite.addTest(getBuyerOrderList("test_getBuyerOrderList_codPaying"))
    return suite