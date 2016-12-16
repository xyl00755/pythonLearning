#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from www.api.webservice import *
from www.common.database import select_one, select, update
from www.common.excel import wsData

"""
LB06 订单详情：新增优惠券折扣信息, getSellerOrderDetail修改类似
http://127.0.0.1:8280/mallws/orders/getBuyerOrderDetail.json
http://127.0.0.1:8280/mallws/orders/getSellerOrderDetail.json
{
    "token":"123",                                                 // 必须
    "orderPk":"123123123",                                         // 非必须 小订单主键
    "orderNo":"123123123"                                          // 必须 小订单号
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                             // 成功 0-成功
        "orderDetail": {                                            // 订单详情模型
            "orderId": null,                                        // 子订单主键
            "orderNo": "20151005483387961",                         // 子订单号
            "paymentNo": "20151005483387963",                       // 大订单号
            "placeOrderTime": "2015-10-26 11:19:00",                // 下单时间
            "sellerId":"123",                                       // 卖家id
            "sellerName": "湖南同州",                               // 卖家名
            "buyerId":"123",                                        // 买家id
            "buyerName":"123",                                      // 买家名
            "payType": "1",                                         // 支付方式 1-在线支付 2-货到付款 3-公司转帐
            "payTime": null,                                        // 支付时间
            "payChannel":"123",                                     // 支付渠道
            "comment": "加急!!",                                    // 留言
            "buttomList":"010101010",                               // 详见解释
            "orderStatus": null,                                    // 小订单状态 C011-待付款 C020-待发货 C017-待收货 C019-已完成 C012-已取消 C015-已退款
            "cancelStatus":"0",                                     // 取消状态 0-正常状态 1-取消中状态 2-已同意取消状态 3-已拒绝取消状态
            "errorStatus":"0",                                      // 异常状态 0-交易异常 1-交易正常
            "receiveStatus":"0",                                    // 收货状态 0-未收货 1-已收货
            "totalPrice": "317970",                                 // 总价/分
            "orderMerchCount":"123",                                // 商品数量
            "isUseCoupon": "1",                                     // 是否使用优惠券 0-使用 1-未使用
            "couponFeeCount": "0",                                  // 优惠券优惠金额
			"totalMerchAmt": "0",                                   // 商品金额（New）
			"totalDiscountAmt": "0",                                // 促销优惠金额（New）
			"dealerBenefitUseAmt": "0",                             // 经销商优惠券抵扣金额（New）
			"dealerCouponUseAmt": "0",                              // 经销商红包抵扣金额（New）
	        "couponUseAmt": "0",                                    // 丹露红包抵扣金额
			"orderDiscountAmount": "",                              // 订单改价 0-未改价 其他-改价金额
            "invoice": {
                "invoiceType": "N011",                              // 发票类型 N011-普通发票 N012-增值税发票
                "invoiceHeader": null,                              // 发票抬头
                "companyName": "上海丹露科技有限公司",              // 公司名称
                "taxpayerRegistrationNumber": "3302325232522325",   // 纳税人识别号
            },
            "deliverAddress": {                                     // 收货地址模型
                "deliverPerson": "李明",                            // 收货人
                "deliverAddress": "辽宁省大连市高新区华信软件大厦", // 收货地址
                "deliverMobile": "13512345567"                      // 收货电话
            },
            "promotionList": [                                      // 促销列表模型
                {
                    "promotionType": "0",                           // 促销类型 0-满增 1-满降
                    "promotionDetail": "123123123",                 // 促销详情
                    "reduceValue":"123"                             // 满减优惠
                    "reduceType":"1",                               // 满减类型 0-减单 1-减总
                }
            ],
            "merchList": [                                          // 商品列表模型
                {
                    "merchId": "1235",                              // 商品主键
                    "merchName": "汤沉一品大红袍 250g",             // 商品名
                    "merchBarCode": null,                           // 商品条码
                    "merchCount": "530",                            // 商品数量
                    "picUrl": null,                                 // 图片URL
                    "merchSpec": "盒",                              // 商品规格
                    "costPrice": null,                              // 原价 (上面划线的那个)
                    "unitPrice": "100",                             // 单价
                    "promotionType":"1"                             // 促销类型 -1-没有 0-满增 1-满降
                }
            ],
            "log": [
                {
                  "operationTime": "2015-10-30 16:19:43",           // 操作时间
                  "operationDesc": "提交订单"                       // 操作描述
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.OrderDetailResponse"
    }
}

参数校验:
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    一个订单有多少个促销(满降满赠) 都放在promotionList中
    1. 如果是满赠 则promotionDetail有一句话 而且商品的costPrice和unitPrice相等
    2. 如果使满降 减总额 则promotionDetail有一句话 reduceValue有减去的总价 而且商品的costPrice和unitPrice相等
    3. 如果使满降 减单价 则promotionDetail有一句话 而且商品的costPrice和unitPrice不相等
    如果是否使用优惠券isUseCoupon为1 则没有使用优惠券 优惠券金额couponFeeCount没有
    所有金额相关单位均为分

    buttomList 为买家/卖家小订单下应该有的按钮列表 结构为 0101010 一共六位数
    第一位 0-没有付款按钮 1-有付款按钮
    第二位 0-没有发货按钮 1-有发货按钮
    第三位 0-没有收货按钮 1-有收货按钮
    第四位 0-没有取消按钮 1-有在线支付还未发货订单取消按钮 2-有货到付款未发货订单取消按钮 3-有货到付款已发货订单取消按钮 4-有交易取消中标签 5-有在线支付已付款订单/待收货订单取消按钮
    第五位 0-没有接受/拒绝取消按钮 1-有接受/拒绝取消按钮
	第六位【追加】0-没有订单跟踪按钮 1-有订单跟踪按钮
    第七位【追加】0-没有订单改价按钮 1-有订单改价按钮
	第八位【追加】0-没有订单拆分按钮 1-有订单拆分按钮
    第九位【追加】0-没有查看拆分按钮 1-有查看拆分按钮
    各个子订单的状态根据子订单的orderStatus来判断 是否是正在取消中订单通过cancelStatus来判断 是否是异常订单通过errorStatus来判断
    """


class getBuyerOrderDetail(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch4 = wsData('Merch4')

    wsUserShop = webservice()
    wsUserShop.login(UserShop.username, UserShop.password)

    # S1.获取终端店货到付款待发货买家订单详情
    def test_getBuyerOrderDetail_codWaitDeliver(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodWaitDeliver.paymentNo, orderNo=self.UserShop.orderCodWaitDeliver['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodWaitDeliver, self.UserShop, self.Merch1)

    # S2.获取终端店货到付款待收货买家订单详情
    def test_getBuyerOrderDetail_codWaitReceive(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodWaitReceive.paymentNo, orderNo=self.UserShop.orderCodWaitReceive['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodWaitReceive, self.UserShop, self.Merch1)

    # S3.获取终端店货到付款待收货买家订单详情
    def test_getBuyerOrderDetail_codCancel(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodCancel.paymentNo, orderNo=self.UserShop.orderCodCancel['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodCancel, self.UserShop, self.Merch1)

    # S4.获取终端店货到付款交易完成买家订单详情
    def test_getBuyerOrderDetail_codComplete(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodComplete.paymentNo, orderNo=self.UserShop.orderCodComplete['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodComplete, self.UserShop, self.Merch1)

    # S5.获取终端店在线支付待付款买家订单详情
    def test_getBuyerOrderDetail_onlineWaitPay(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderOnlineWaitPay.paymentNo, orderNo=self.UserShop.orderOnlineWaitPay['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderOnlineWaitPay, self.UserShop, self.Merch1)

    # S6.获取终端店在线支付待发货买家订单详情

    # S7.获取终端店在线支付待收货买家订单详情

    # S8.获取终端店在线支付交易完成买家订单详情

    # S9.获取终端店在线支付已取消买家订单详情
    def test_getBuyerOrderDetail_onlineCancel(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderOnlienCancel.paymentNo, orderNo=self.UserShop.orderOnlienCancel['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderOnlienCancel, self.UserShop, self.Merch1)

    # S11.获取货到付款订单拆单订单详情（交易中）
    def test_getBuyerOrderDetail_codPayingSeparat(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodPayingSeparat.paymentNo, orderNo=self.UserShop.orderCodPayingSeparat['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodPayingSeparat, self.UserShop, self.Merch1, '000001001')

    # S12.获取货到付款订单拆单订单详情（交易完成）
    def test_getBuyerOrderDetail_codCompleteSeparat(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodCompleteSeparat.paymentNo, orderNo=self.UserShop.orderCodCompleteSeparat['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodCompleteSeparat, self.UserShop, self.Merch1, '000001001')

    # 新增用例
    # 获取终端店货到付款待发货的订单，含有经销商红包、经销商优惠券
    def test_getBuyerOrderDetail_orderNoUseCoupon(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop2.orderNoUseCoupon.paymentNo, orderNo=self.UserShop2.orderNoUseCoupon['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop2.orderNoUseCoupon, self.UserShop2, self.Merch4)

      # 获取终端店货到付款待发货的订单，含有满赠促销
    def test_getBuyerOrderDetail_codWaitDeliverFullAdd(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodWaitDeliverFullAdd.paymentNo, orderNo=self.UserShop.orderCodWaitDeliverFullAdd['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodWaitDeliverFullAdd, self.UserShop, self.Merch1)

    # 获取终端店货到付款待发货的订单，含有满减减单价促销
    def test_getBuyerOrderDetail_codWaitDeliverUnitDown(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodWaitDeliverUnitDown.paymentNo, orderNo=self.UserShop.orderCodWaitDeliverUnitDown['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodWaitDeliverUnitDown, self.UserShop, self.Merch1)

    #获取终端店货到付款待发货的订单，含有满减减总价促销
    def test_getBuyerOrderDetail_codWaitDeliverFullDown(self):
        orderDetail = self.wsUserShop.getBuyerOrderDetail(orderPk=self.UserShop.orderCodWaitDeliverFullDown.paymentNo, orderNo=self.UserShop.orderCodWaitDeliverFullDown['orderNo'])
        self.assertEqual(orderDetail.model['success'], '0')
        self.assertOrderDetail(orderDetail, self.UserShop.orderCodWaitDeliverFullDown, self.UserShop, self.Merch1)


    #验证订单返回数据的正确性
    def assertOrderDetail(self, rsq, order, buyer, merch, buttomList='00000100'):
        paymentOrder = select_one('select * from dlpay.dl_payment_order where pay_no = ?', order.paymentNo)
        orderDetail = select_one('select * from dlorder.dl_order_orderdetail where order_no = ?', order.orderNo)
        orderInfo = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', order.orderNo)
        orderItem = select_one('select * from dlorder.dl_order_orderitem where order_no = ?', order.orderNo)
        self.assertEqual(rsq.model['orderDetail']['orderId'], orderInfo.id)
        self.assertEqual(rsq.model['orderDetail']['orderNo'], orderInfo.order_no)
        self.assertEqual(rsq.model['orderDetail']['paymentNo'], orderInfo.pay_no)
        self.assertEqual(rsq.model['orderDetail']['placeOrderTime'], str(orderInfo.gmt_created))
        #self.assertEqual(rsq.model['orderDetail']['orderId'], orderInfo.id)
        self.assertEqual(rsq.model['orderDetail']['orderStatus'], orderInfo.order_status)
        self.assertEqual(rsq.model['orderDetail']['payType'], orderInfo.pay_type)
        if rsq.model['orderDetail']['payTime'] is None:
            self.assertEqual(rsq.model['orderDetail']['payTime'], None)
        else:
            self.assertEqual(rsq.model['orderDetail']['payTime'], orderDetail.pay_date.strftime('%Y/%m/%d %H:%M:%S'))
        if rsq.model['orderDetail']['payChannel'] is None:
            self.assertEqual(rsq.model['orderDetail']['payChannel'], None)
        else:
            self.assertEqual(rsq.model['orderDetail']['payChannel'], paymentOrder.pay_channel)
        self.assertEqual(rsq.model['orderDetail']['sellerId'], merch.sellerId)
        self.assertEqual(rsq.model['orderDetail']['sellerName'], merch.sellerName)
        self.assertEqual(rsq.model['orderDetail']['buyerId'], buyer.companyId)
        self.assertEqual(rsq.model['orderDetail']['buyerName'], buyer.fullName)
        self.assertEqual(rsq.model['orderDetail']['errorStatus'], '1')
        if orderInfo.cancel_status == 'normal':
            self.assertEqual(rsq.model['orderDetail']['cancelStatus'], '0')
        else:
            self.assertEqual(rsq.model['orderDetail']['cancelStatus'], '1')
        if orderInfo.confirm_status == 'unreceive':
            self.assertEqual(rsq.model['orderDetail']['receiveStatus'], '0')
        else:
            self.assertEqual(rsq.model['orderDetail']['receiveStatus'], '1')
        self.assertEqual(rsq.model['orderDetail']['orderMerchCount'], str(orderItem.num))
        self.assertEqual(rsq.model['orderDetail']['comment'], orderDetail.remarks)
        self.assertEqual(rsq.model['orderDetail']['totalPrice'], str(orderDetail.total_amount))

        #新增totalMerchAmt（商品金额）的校验
        self.assertNotEqual(rsq.model['orderDetail']['orderMerchCount'],'0')

        #新增totalDiscountAmt（促销优惠金额）的校验
        if orderInfo.ispromotion == 0:
            self.assertEqual(rsq.model['orderDetail']['totalDiscountAmt'],'0')
        else:
            orderPromotion=select_one('select * from dlorder.dl_order_promotion_detail where order_no=?',order.orderNo)
            proType=orderPromotion.promotion_type
            if proType == 'fulladd':
                self.assertEqual(rsq.model['orderDetail']['totalDiscountAmt'],'0')
            else:
                self.assertNotEqual(rsq.model['orderDetail']['totalDiscountAmt'],'0')

        #新增dealerBenefitUseAmt&dealerCouponUseAmt的校验
        couponUseSql=select_one('select * from dlorder.dl_order_ordercoupon where order_no=?',order.orderNo)
        if couponUseSql is None:
            self.assertEqual(rsq.model['orderDetail']['dealerBenefitUseAmt'],'0')
            self.assertEqual(rsq.model['orderDetail']['dealerCouponUseAmt'],'0')
            self.assertEqual(rsq.model['orderDetail']['isUseCoupon'], '1')
        else:
            couponUse=couponUseSql.coupon_info
            couponUse=json.loads(couponUse)
            num=len(couponUse)
            for i in range(len(couponUse)):
                if couponUse[i]['couponTypeId'] == '10':
                    self.assertEqual(couponUse[i]['discountAmt'],int(rsq.model['orderDetail']['dealerCouponUseAmt']))
                else:
                    self.assertEqual(couponUse[i]['discountAmt'],int(rsq.model['orderDetail']['dealerBenefitUseAmt']))
            self.assertEqual(rsq.model['orderDetail']['isUseCoupon'], '0')



        if orderInfo.order_coupon_amount == 0:
            #self.assertEqual(rsq.model['orderDetail']['isUseCoupon'], '1')
            self.assertEqual(rsq.model['orderDetail']['couponFeeCount'], '0')
            self.assertEqual(rsq.model['orderDetail']['couponUseAmt'], '0')
        else:
            #self.assertEqual(rsq.model['orderDetail']['isUseCoupon'], '0')
            orderCoupon = select_one('select * from dlorder.dl_order_ordercoupon where order_no =', order.orderNo)
            self.assertEqual(rsq.model['orderDetail']['couponFeeCount'], '0')
            self.assertEqual(rsq.model['orderDetail']['couponUseAmt'], orderCoupon.coupon_info[0]['couponAmt'])
        self.assertEqual(rsq.model['orderDetail']['buttomList'], buttomList)


        if orderInfo.order_discount_amount is None:
            self.assertEqual(rsq.model['orderDetail']['orderDiscountAmount'], '0')
        else:
            self.assertEqual(rsq.model['orderDetail']['orderDiscountAmount'], orderInfo.order_discount_amount)

        # 商品列表
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['merchId'], merch.goodsId)
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['merchName'], merch.fullName)
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['merchBarCode'], merch.productBarCode)
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['merchCount'], str(orderItem.num))
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['picUrl'], merch.albumPicUrl)
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['merchSpec'], merch[u'包装规格'])
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['costPrice'], str(orderItem.cost_price))
        self.assertEqual(rsq.model['orderDetail']['merchList'][0]['unitPrice'], str(orderItem.unit_price))

        # 促销列表
        if orderInfo.ispromotion == 0:
            self.assertEqual(rsq.model['orderDetail']['merchList'][0]['promotionType'], '-1')
            self.assertEqual(rsq.model['orderDetail']['promotionList'], [])
        else :
            orderPromotion = select_one('select * from dlorder.dl_order_promotion_detail where order_no =?', order.orderNo)
            if orderPromotion.promotion_type == 'fulladd':
                self.assertEqual(rsq.model['orderDetail']['merchList']['promotionType'], '1')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['promotionType'], '0')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['promotionDetail'], orderPromotion.promotion_detail)
                self.assertEqual(rsq.model['orderDetail']['promotionList']['reduceValue'], '0')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['reduceType'], '')
            if orderPromotion.promotion_type == 'unitdown':
                self.assertEqual(rsq.model['orderDetail']['merchList']['promotionType'], '2')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['promotionType'], '1')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['promotionDetail'], orderPromotion.promotion_detail)
                self.assertEqual(rsq.model['orderDetail']['promotionList']['reduceValue'], orderPromotion.amount)
                self.assertEqual(rsq.model['orderDetail']['promotionList']['reduceType'], '0')
            if orderPromotion.promotion_type == 'fulldown':
                self.assertEqual(rsq.model['orderDetail']['merchList']['promotionType'], '2')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['promotionType'], '1')
                self.assertEqual(rsq.model['orderDetail']['promotionList']['promotionDetail'], orderPromotion.promotion_detail)
                self.assertEqual(rsq.model['orderDetail']['promotionList']['reduceValue'], orderPromotion.amount)
                self.assertEqual(rsq.model['orderDetail']['promotionList']['reduceType'], '1')

        # 收货地址
        self.assertEqual(rsq.model['orderDetail']['deliverAddress']['deliverPerson'], orderDetail.receive_person)
        self.assertEqual(rsq.model['orderDetail']['deliverAddress']['deliverAddress'], orderDetail.receive_address)
        self.assertEqual(rsq.model['orderDetail']['deliverAddress']['deliverMobile'], orderDetail.receive_tel)

        # 发票
        orderInvoice = select_one('select * from dlorder.dl_order_orderinvoice where order_no = ?', order.orderNo)
        if orderInvoice is None:
            self.assertEqual(rsq.model['orderDetail']['invoice']['invoiceType'], None)
            self.assertEqual(rsq.model['orderDetail']['invoice']['invoiceHeader'], None)
            self.assertEqual(rsq.model['orderDetail']['invoice']['companyName'],None)
            self.assertEqual(rsq.model['orderDetail']['invoice']['taxpayerRegistrationNumber'], None)
        else:
            self.assertEqual(rsq.model['orderDetail']['invoice']['invoiceType'], orderInvoice.invoice_type)
            self.assertEqual(rsq.model['orderDetail']['invoice']['invoiceHeader'], orderInvoice.invoice_header)
            self.assertEqual(rsq.model['orderDetail']['invoice']['companyName'], orderInvoice.company_name)
            self.assertEqual(rsq.model['orderDetail']['invoice']['taxpayerRegistrationNumber'], orderInvoice.invoice_number)

        # 订单跟踪
        orderLog = select('select * from dlorder.dl_order_orderlog where order_no = ?', order.orderNo)
        self.assertEqual(len(rsq.model['orderDetail']['log']), len(orderLog))
        if len(rsq.model['orderDetail']['log']) == 1:
            self.assertIsNotNone(rsq.model['orderDetail']['log'][0]['operationTime'])
            self.assertEqual(rsq.model['orderDetail']['log'][0]['operationDesc'], orderLog[0]['deal_descrip'])

    def tearDown(self):
        # 清空购物车、恢复库存
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop.userId)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codWaitDeliver"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codWaitReceive"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codCancel"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codComplete"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_onlineWaitPay"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_onlineCancel"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_onlineWaitPay"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_onlineCancel"))
    #suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codWaitDeliverFullAdd"))
    # suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codWaitDeliverUnitDown"))
    #suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_codWaitDeliverFullDown"))
    suite.addTest(getBuyerOrderDetail("test_getBuyerOrderDetail_orderNoUseCoupon"))
    return suite