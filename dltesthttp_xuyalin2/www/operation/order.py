#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对订单的相关操作
"""

from www.api.webservice import *
from www.common.database import *
from www.common.model import Shoppingcart


# 提交订单 payWay=1在线支付 payWay=2货到付款
def createOrder(buyer, merch, merchCount='1',payWay='2'):
        ws = webservice()
        ws.login(buyer.username, buyer.password)
        ws.addShoppingcar(merchId=merch.goodsId, merchCount=merchCount, sellerId=merch.seller_store_id, sellerName=merch.sellerName)
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', buyer.userId,  merch.goodsId)
        invoice = {"invoiceId":buyer.invoiceId, "invoiceType":"N011","needInvoice":"0","invoiceHeader":buyer.invoiceHeader}
        deliverAddress = {"deliverAddress":buyer.deliverAddress, "deliverMobile":buyer.deliverMobile, "deliverPerson":buyer.deliverPerson}
        sellerList = []
        sellerList.append({"sellerId":merch.shopcartSellerId,"sellerName":merch.sellerName,"isYijipayAccount":merch.isYijipayAccount,"codFlag":merch.codFlag,
                           "supportVatInvoice":merch.supportVatInvoice,"comment":"createOrderByShoppingcart comment.","merchList":
                               [{"id":shopcart.id,"merchId":merch.goodsId,"merchBarCode":merch.productBarCode}]})
        ws.checkSwitch()
        order = ws.createOrderByShoppingcartNew(payWay=payWay,invoice=invoice, deliverAddress=deliverAddress, sellerList=sellerList)
        if order.model['createOrderInfoModel']['onlinePaymentModelList'] is not None:
                names = ['paymentNo', 'payType', 'totalPrice', 'orderNo', 'ws']
                values = [order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['paymentNo'], order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['payType'],
                          order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['totalPrice'], order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['orderNo'], ws]
                # returnOrder.paymentNo = order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['paymentNo']
                # returnOrder.payType = order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['payType']
                # returnOrder.totalPrice = order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['totalPrice']
                # returnOrder.orderNo = order.model['createOrderInfoModel']['onlinePaymentModelList'][0]['orderNo']
                #returnOrder = Dict(names, values)
        elif order.model['createOrderInfoModel']['cashOnDeliveryModelList'] is not None:
                names = ['paymentNo', 'orderNo', 'price', 'ws']
                values = [order.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo'], order.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo'],
                          order.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price'], ws]
                #
                # returnOrder.paymentNo = order.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['paymentNo']
                # returnOrder.orderNo = order.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['orderNo']
                # returnOrder.price = order.model['createOrderInfoModel']['cashOnDeliveryModelList'][0]['price']
        return Dict(names, values)

# 获取货到付款待发货订单
def createOrderWaitReceive(buyer, merch, merchCount='1',payWay='2'):
    pass


# 联动货到付款支付
def codPay(orderNo, ini_file='../../config/env.ini'):
    import requests
    from www.common.config import config
    httpConfig = config().confighttp
    umpayVShost = httpConfig['umpayhost']
    umpayVSport = httpConfig['umpayport']
    s = requests.Session()
    urldlPay = 'http://'  + httpConfig['dlpayhost'] + ':' + httpConfig['dlpayport']
    url = 'http://' + umpayVShost + ':' + umpayVSport + '/payResult'
    data2 = {'orderNo':orderNo, 'url':urldlPay}
    s.post(url=url, data=data2)

"""
清空订单，传入buyer即清空用户所有订单，传入orderNo即清空单个订单
"""
def cleanOrders(buyerCompanyId=None, orderNo=None):


    if orderNo is not None:
        paymentNo = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', orderNo).pay_no
        update('delete from dlpay.dl_payment_audit_record where pay_no = ?', paymentNo)
        update('delete from dlpay.dl_payment_clean_record where pay_no = ?', paymentNo)
        update('delete from dlpay.dl_payment_clean_result_record where pay_no = ?', paymentNo)
        update('delete from dlpay.dl_payment_exception where pay_no = ?', paymentNo)
        update('delete from dlpay.dl_payment_order where pay_no = ?', paymentNo)
        update('delete from dlpay.dl_payment_record where pay_no = ?', paymentNo)
        update('delete from dlpay.dl_payment_split_order where pay_no = ?', paymentNo)
        update('delete from dlorder.dl_order_orderdetail where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_changeamount_log where  order_no  = ?', orderNo)
        update('delete from dlorder.dl_order_ordercoupon where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_orderinfo where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_orderinvoice where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_orderitem where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_orderlog where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_orderprint_log where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_ordersnapshot where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_promotion_detail where order_no = ?', orderNo)
        update('delete from dlorder.dl_order_seller_detail where order_no = ?', orderNo)

    elif buyerCompanyId is not None:
        #pay_no = select('(select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        #order_no = select('SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?', buyerCompanyId)
        update('delete from dlpay.dl_payment_audit_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        update('delete from dlpay.dl_payment_clean_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        update('delete from dlpay.dl_payment_clean_result_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        update('delete from dlpay.dl_payment_exception where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        update('delete from dlpay.dl_payment_order where payer_id = ?', buyerCompanyId)
        update('delete from dlpay.dl_payment_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        update('delete from dlpay.dl_payment_split_order where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
        update('delete from dlorder.dl_order_changeamount_log where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_ordercoupon where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_orderinvoice where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_orderitem where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_orderlog where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_orderprint_log where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_ordersnapshot where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_promotion_detail where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_seller_detail where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
        update('delete from dlorder.dl_order_orderdetail where buyer_id = ?', buyerCompanyId)

    else:
        raise 'You need to fill in at least orderNo.'



# def cleanOrdersBySnapshot(buyerCompanyId=None):
#     create_engine()
#     print select('select order_no from dlorder.dl_order_ordersnapshot where buyer_detail like ?', '%' + buyerCompanyId + '%')
#     print select_int('select count(*) from dlpay.dl_payment_audit_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no from dlorder.dl_order_ordersnapshot where buyer_detail like ?))', '%' + buyerCompanyId + '%')
#     print select_int('select count(*) from dlorder.dl_order_orderinvoice where order_no in (SELECT order_no FROM dlorder.dl_order_ordersnapshot where buyer_detail like ?)', '%' + buyerCompanyId + '%')
    # update('delete from dlpay.dl_payment_audit_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
    # update('delete from dlpay.dl_payment_clean_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
    # update('delete from dlpay.dl_payment_clean_result_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
    # update('delete from dlpay.dl_payment_exception where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
    # update('delete from dlpay.dl_payment_order where payer_id = ?', buyerCompanyId)
    # update('delete from dlpay.dl_payment_record where pay_no in (select pay_no from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?))', buyerCompanyId)
    # update('delete from dlorder.dl_order_changeamount_log where  order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_ordercoupon where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_orderinfo where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_orderinvoice where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_orderitem where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_orderlog where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_orderprint_log where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_ordersnapshot where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_promotion_detail where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_seller_detail where order_no in (SELECT order_no FROM dlorder.dl_order_orderdetail where buyer_id = ?)', buyerCompanyId)
    # update('delete from dlorder.dl_order_orderdetail where buyer_id = ?', buyerCompanyId)



if __name__ == '__main__':
    #cleanOrders(orderNo='20572364600253')
    #cleanOrdersBySnapshot(buyerCompanyId='6fb850120da449ef98a2c7e641100e02')
    create_engine()

# 取消订单