#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
初始化基础数据
"""

from www.api.webservice import *
from www.common.database import create_engine, update
from www.common.excel import wsData, write_excel
from www.operation.order import createOrder, codPay


def initOrder():
    UserShop = wsData('TmlShop')
    Merch = wsData('Merch1')
    DealMgr = wsData('DealMager')

    ws = webservice()
    ws.login(DealMgr.username, DealMgr.password)

    #在线支付待付款订单(C011)
    orderOnlineWaitPay = createOrder(UserShop, Merch, payWay='1')
    orderOnlineWaitPay.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderOnlineWaitPay', rowvalue=str(orderOnlineWaitPay))
    import datetime
    update('update dlorder.dl_order_orderinfo SET gmt_created = ? WHERE order_no = ?', datetime.datetime.strptime('2099-01-01 00:00:00', "%Y-%m-%d %H:%M:%S"), orderOnlineWaitPay.orderNo)

    #在线支付待发货订单
    #在线支付待收货订单
    #在线支付交易完成订单

    #在线支付已取消订单（C012）
    orderOnlienCancel = createOrder(UserShop, Merch, payWay='1')
    orderOnlienCancelWS = orderOnlienCancel.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderOnlienCancel', rowvalue=str(orderOnlienCancel))
    orderOnlienCancelWS.cancel(paymentNo=orderOnlienCancel.paymentNo, payType='1', cancelType='1')

    #货到付款待发货订单（C020）
    orderCodWaitDeliver = createOrder(UserShop, Merch)
    orderCodWaitDeliver.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodWaitDeliver', rowvalue=str(orderCodWaitDeliver))

    #货到付款待收货订单（C017）
    orderCodWaitReceive = createOrder(UserShop, Merch)
    orderCodWaitReceive.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodWaitReceive', rowvalue=str(orderCodWaitReceive))
    ws.deliver(orderNo=orderCodWaitReceive.orderNo)

    #货到付款已完成订单(C019)
    orderCodComplete = createOrder(UserShop, Merch)
    orderCodComplete.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodComplete', rowvalue=str(orderCodComplete))
    ws.deliver(orderNo=orderCodComplete.orderNo)
    codPay(orderNo=orderCodComplete.orderNo)

    #货到付款已取消订单（C012）
    orderCodCancel = createOrder(UserShop, Merch)
    orderCodCancelWS = orderCodCancel.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodCancel', rowvalue=str(orderCodCancel))
    orderCodCancelWS.cancel(paymentNo=orderCodCancel.paymentNo)

    #——————————————————拆单————————————————————————————
    #货到付款待发货拆单订单
    orderCodWaitDeliverSeparat = createOrder(UserShop, Merch)
    orderCodWaitDeliverSeparat.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodWaitDeliverSeparat', rowvalue=str(orderCodWaitDeliverSeparat))
    orderCodWaitDeliverSeparatAmount= [str(int(orderCodWaitDeliverSeparat.price)/5), str(int(orderCodWaitDeliverSeparat.price)/5), str(int(orderCodWaitDeliverSeparat.price)/5), str(int(orderCodWaitDeliverSeparat.price)/5), str(int(orderCodWaitDeliverSeparat.price)/5)]
    ws.separateOrder(orderNo=orderCodWaitDeliverSeparat.orderNo, separateOrderAmount=orderCodWaitDeliverSeparatAmount).model['paymentList']
    orderCodWaitDeliverSeparatList = ws.getSeparateOrderList(orderNo=orderCodWaitDeliverSeparat.orderNo).model['paymentInfoList']
    write_excel(sheetname='TmlShop', rowkey='orderCodWaitDeliverSeparatSub', rowvalue=str(orderCodWaitDeliverSeparatList))

    #货到付款待收货拆单订单
    orderCodWaitReceiveSeparat = createOrder(UserShop, Merch)
    orderCodWaitReceiveSeparat.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodWaitReceiveSeparat', rowvalue=str(orderCodWaitReceiveSeparat))
    ws.deliver(orderNo=orderCodWaitReceiveSeparat.orderNo)
    orderCodWaitReceiveSeparatAmount= [str(int(orderCodWaitReceiveSeparat.price))]
    ws.separateOrder(orderNo=orderCodWaitReceiveSeparat.orderNo, separateOrderAmount=orderCodWaitReceiveSeparatAmount).model['paymentList']
    orderCodWaitReceiveSeparatList = ws.getSeparateOrderList(orderNo=orderCodWaitReceiveSeparat.orderNo).model['paymentInfoList']
    write_excel(sheetname='TmlShop', rowkey='orderCodWaitReceiveSeparatSub', rowvalue=str(orderCodWaitReceiveSeparatList))

    #货到付款支付中订单
    orderCodPayingSeparat = createOrder(UserShop, Merch)
    orderCodPayingSeparat.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodPayingSeparat', rowvalue=str(orderCodPayingSeparat))
    ws.deliver(orderNo=orderCodPayingSeparat.orderNo)
    orderCodPayingSeparatAmount = [str(int(orderCodPayingSeparat.price)-600),'100', '500']
    orderCodPayingSeparatSub = ws.separateOrder(orderNo=orderCodPayingSeparat.orderNo, separateOrderAmount=orderCodPayingSeparatAmount).model['paymentList']
    codPay(orderNo=orderCodPayingSeparatSub[0]['separatePaymentNo'])
    orderCodPayingSeparatList = ws.getSeparateOrderList(orderNo=orderCodPayingSeparat.orderNo).model['paymentInfoList']
    write_excel(sheetname='TmlShop', rowkey='orderCodPayingSeparatSub', rowvalue=str(orderCodPayingSeparatList))

    #货到付款交易完成拆单订单
    orderCodCompleteSeparat = createOrder(UserShop, Merch)
    orderCodCompleteSeparat.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodCompleteSeparat', rowvalue=str(orderCodCompleteSeparat))
    orderCodCompleteSeparatAmount= [str(int(orderCodCompleteSeparat.price)-600),'100', '500']
    orderCodCompleteSeparatSub = ws.separateOrder(orderNo=orderCodCompleteSeparat.orderNo, separateOrderAmount=orderCodCompleteSeparatAmount).model['paymentList']
    ws.deliver(orderNo=orderCodCompleteSeparat.orderNo)
    for i in range(0, len(orderCodCompleteSeparatSub)):
        codPay(orderNo=orderCodCompleteSeparatSub[i]['separatePaymentNo'])
    orderCodCompleteSeparatList = ws.getSeparateOrderList(orderNo=orderCodCompleteSeparat.orderNo).model['paymentInfoList']
    write_excel(sheetname='TmlShop', rowkey='orderCodCompleteSeparatSub', rowvalue=str(orderCodCompleteSeparatList))

    #货到付款交易取消拆单订单
    orderCodCancelSeparat = createOrder(UserShop, Merch)
    orderCodCancelSeparatWS = orderCodCancelSeparat.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderCodCancelSeparat', rowvalue=str(orderCodCancelSeparat))
    orderCodCancelSeparatAmount= [str(int(orderCodCancelSeparat.price)-600),'100', '500']
    ws.separateOrder(orderNo=orderCodCancelSeparat.orderNo, separateOrderAmount=orderCodCancelSeparatAmount).model['paymentList']
    orderCodCancelSeparatWS.cancel(paymentNo=orderCodCancelSeparat.paymentNo)
    orderCodCancelSeparatList = ws.getSeparateOrderList(orderNo=orderCodCancelSeparat.orderNo).model['paymentInfoList']
    write_excel(sheetname='TmlShop', rowkey='orderCodCancelSeparatSub', rowvalue=str(orderCodCancelSeparatList))

    #——————————————————————————————改价————————————————————————————————
    #

    #经销商管理员下货到付款订单待发货
    # orderDealCodWaitDeliver = createOrder(DealMgr, Merch4, payWay='1')
    # write_excel(sheetname='DealMager', rowkey='orderCodWaitDeliver', rowvalue=str(orderDealCodWaitDeliver))


	#——————————————————————————————订单改价订单基础数据————————————————————————————————

    #货到付款交易未完成的订单号
    orderChangePirceNotfinish = createOrder(UserShop, Merch)
    orderChangePirceNotfinish.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderChangePirceNotfinish', rowvalue=str(orderChangePirceNotfinish))

    #货到付款交易完成的订单号
    orderChangePirceFinish = createOrder(UserShop, Merch)
    orderChangePirceFinish.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderChangePirceFinish', rowvalue=str(orderChangePirceFinish))
    ws.deliver(orderNo=orderChangePirceFinish.orderNo)
    codPay(orderNo=orderChangePirceFinish.orderNo)

    #货到付款交易已取消的订单号
    orderChangePirceCancel = createOrder(UserShop, Merch)
    orderChangePirceCancelWS = orderChangePirceCancel.pop('ws')
    write_excel(sheetname='TmlShop', rowkey='orderChangePirceCancel', rowvalue=str(orderChangePirceCancel))
    orderChangePirceCancelWS.cancel(paymentNo=orderChangePirceCancel .paymentNo)

    #在线支付未付款的订单号
    #在线支付待发货的订单号
    #在线支付待收货的订单号
    #在线支付已取消的订单号

if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/../..')
    create_engine()
    initOrder()