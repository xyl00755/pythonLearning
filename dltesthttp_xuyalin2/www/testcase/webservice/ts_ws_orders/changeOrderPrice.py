#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import select_one
from www.common.database import update
from www.common.excel import wsData

"""
0186.订单改价操作
http://127.0.0.1:8280/mallws/orders/oper/changeOrderPrice.json
{
	"token":"123"					//必须
	"orderNo":"123456",				//必须 订单号
	"orderDiscountAmount":"100",	//必须 订单改价折扣金额 0-未改价 其他-改价金额 加价在金额前面加负号
	"orderChangeAmount":"900",		//必须 订单改价后金额
	"orderStatus":"C011"			//必须 订单状态
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                      // 0-成功 1-订单状态改变(失败)
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
参数说明:
	orderStatus用于改价前判断订单状态是否发生改变，决定改价操作是否执行
	订单状态 C011-待付款 C020-待发货 C017-待收货 C019-已完成 C012-已取消 C015-已退款
"""
class changeOrderPrice(unittest.TestCase):
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')

    #货到付款订单减价
    def test_ReduceChangeOrderPrice_cashondelivery(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderNo)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        # 货到付款订单减价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceNotfinish.orderNo,orderDiscountAmount='100', orderChangeAmount=str(
            int(RstDb.order_retail_amount) - 100),orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单减价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount - 100)
        update('update dlorder.dl_order_orderinfo set order_amount = ? where order_no = ?',RstDb.order_retail_amount, self.UserShop.orderChangePirceNotfinish.orderNo)

    #货到付款订单加价
    def test_AddChangeOrderPrice_cashondelivery(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        # 货到付款订单加价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceNotfinish.orderNo, orderDiscountAmount='-100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) +100), orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单加价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount + 100)
        update('update dlorder.dl_order_orderinfo set order_amount = ? where order_no = ?', RstDb.order_retail_amount,self.UserShop.orderChangePirceNotfinish.orderNo)

    #货到付款订单改价(减价后再加价)
    def test_changeOrderPrice_cashondelivery(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        # 货到付款订单减价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceNotfinish.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单减价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount - 100)

        #货到付款订单加价
        ChangePriceRst1 = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceNotfinish.orderNo, orderDiscountAmount='-200',orderChangeAmount=str(RstDb1.order_retail_amount+200),
                            orderStatus=RstDb1.order_status)

        self.assertEquals(ChangePriceRst1.code, 200)
        self.assertEquals(ChangePriceRst1.model['success'], '0')

        #检验订单加价
        RstDb2 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceNotfinish.orderNo)
        self.assertEquals(RstDb2.order_amount, RstDb.order_amount +200)
        update('update dlorder.dl_order_orderinfo set order_amount = ? where order_no = ?', RstDb.order_retail_amount,self.UserShop.orderChangePirceNotfinish.orderNo)

    #货到付款(已完成)订单改价
    def test_AlreadypaidChangeOrderPrice_cashondelivery(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceFinish.orderNo)

        # # 从数据库中修改订单状态为已完成(C019)
        # update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C019',self.UserShop.orderNo)
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceFinish.orderNo, orderDiscountAmount='100',orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)

        #校验已完成的订单改价失败
        self.assertEquals(ChangePriceRst.model['success'], '1')
        # update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C020',self.UserShop.orderNo)

    #货到付款(已取消)订单改价
    def test_AlreadCancelChangeOrderPrice_cashondelivery(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop.orderChangePirceCancel.orderNo)

        # # 从数据库中修改订单状态为已取消(C012)
        # update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C012',self.UserShop.orderNo)
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceCancel.orderNo, orderDiscountAmount='100',orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)

        #校验已取消的订单改价失败
        self.assertEquals(ChangePriceRst.model['success'], '1')
        # update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C020',self.UserShop.orderNo)

    #货到付款订单减价后恢复原价
    def test_RestoreOriginalPrice_cashondelivery(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?',self.UserShop.orderChangePirceNotfinish.orderNo)
        # 货到付款订单减价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceNotfinish.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单减价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?',self.UserShop.orderChangePirceNotfinish.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount - 100)

        #减价后恢复原价
        ChangePriceRst1 = ws.changeOrderPrice(orderNo=self.UserShop.orderChangePirceNotfinish.orderNo,orderDiscountAmount='0', orderChangeAmount=str(RstDb1.order_retail_amount),orderStatus=RstDb1.order_status)
        self.assertEquals(ChangePriceRst1.code,200)
        self.assertEquals(ChangePriceRst1.model['success'], '0')
        #检验是否恢复原价
        RstDb2 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?',self.UserShop.orderChangePirceNotfinish.orderNo)
        self.assertEquals(RstDb2.order_amount,RstDb.order_amount)

    #在线支付(未付款)订单减价
    def test_ReduceChangeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        # 在线支付订单减价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单减价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount - 100)
        update('update dlorder.dl_order_orderinfo set order_amount = ? where order_no = ?', RstDb.order_retail_amount,self.UserShop2.orderNo)

    #在线支付(未付款)订单加价
    def test_AddChangeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',
               self.UserShop2.orderNo)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        # 在线支付订单加价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='-100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) + 100), orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单加价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount + 100)
        update('update dlorder.dl_order_orderinfo set order_amount = ? where order_no = ?', RstDb.order_retail_amount,self.UserShop2.orderNo)

    #在线支付(未付款)订单改价（减价后再加价）
    def test_changeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',self.UserShop2.orderNo)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        # 在线支付订单减价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(int(RstDb.order_retail_amount) - 100),
                                             orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单减价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount - 100)

        # 在线支付订单加价
        ChangePriceRst1 = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='-200',
                                              orderChangeAmount=str(RstDb1.order_retail_amount + 200),
                                              orderStatus=RstDb1.order_status)

        self.assertEquals(ChangePriceRst1.code, 200)
        self.assertEquals(ChangePriceRst1.model['success'], '0')

        # 检验订单加价
        RstDb2 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        self.assertEquals(RstDb2.order_amount, RstDb.order_amount + 200)
        update('update dlorder.dl_order_orderinfo set order_amount = ? where order_no = ?', RstDb.order_retail_amount,
               self.UserShop2.orderNo)

    #在线支付(交易已完成)订单改价
    def  test_AlreadypaidChangeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',
               self.UserShop2.orderNo)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)

        # 从数据库中修改订单状态为已付款(C019)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C019',
               self.UserShop2.orderNo)
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)

        # 校验已完成的订单改价失败
        self.assertEquals(ChangePriceRst.model['success'], '1')
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',self.UserShop2.orderNo)

     #在线支付(待发货)订单改价
    def test_DeliverGoodsChangeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)

        # 从数据库中修改订单状态为待发货(C020)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C020',
               self.UserShop2.orderNo)
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)

        # 校验待发货的订单改价失败
        self.assertEquals(ChangePriceRst.model['success'], '1')
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',
               self.UserShop2.orderNo)

    #在线支付（待收货）订单改价
    def test_ReceivedGoodsChangeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)

        # 从数据库中修改订单状态为待收货(C017)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C017',
               self.UserShop2.orderNo)
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)

        # 校验待收货的订单改价失败
        self.assertEquals(ChangePriceRst.model['success'], '1')
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',
               self.UserShop2.orderNo)

    #在线支付(已取消)订单改价
    def test_AlreadCancelChangeOrderPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)

        # 从数据库中修改订单状态为已取消(C012)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C012',
               self.UserShop2.orderNo)
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)

        # 校验已取消的订单改价失败
        self.assertEquals(ChangePriceRst.model['success'], '1')
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',
               self.UserShop2.orderNo)

    #在线支付(未付款)减价后恢复原价
    def test_RestoreOriginalPrice_Onlinepayment(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',
               self.UserShop2.orderNo)
        RstDb = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        # 在线支付订单减价调用接口
        ChangePriceRst = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='100',
                                             orderChangeAmount=str(
                                                 int(RstDb.order_retail_amount) - 100), orderStatus=RstDb.order_status)
        self.assertEquals(ChangePriceRst.code, 200)
        self.assertEquals(ChangePriceRst.model['success'], '0')

        # 检验订单减价后是否修改成功
        RstDb1 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        self.assertEquals(RstDb1.order_amount, RstDb.order_retail_amount - 100)

        # 减价后恢复原价
        ChangePriceRst1 = ws.changeOrderPrice(orderNo=self.UserShop2.orderNo, orderDiscountAmount='0',
                                              orderChangeAmount=str(RstDb1.order_retail_amount),
                                              orderStatus=RstDb1.order_status)
        self.assertEquals(ChangePriceRst1.code, 200)
        self.assertEquals(ChangePriceRst1.model['success'], '0')
        # 检验是否恢复原价
        RstDb2 = select_one('select * from dlorder.dl_order_orderinfo where order_no = ?', self.UserShop2.orderNo)
        self.assertEquals(RstDb2.order_amount, RstDb.order_amount)


def tearDown(self):
    update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C020', self.UserShop.orderNo)
    update('update dlorder.dl_order_orderinfo set order_status = ? where order_no = ?', 'C011',self.UserShop2.orderNo)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(changeOrderPrice('test_AddChangeOrderPrice_cashondelivery'))
    suite.addTest(changeOrderPrice('test_ReduceChangeOrderPrice_cashondelivery'))
    suite.addTest(changeOrderPrice('test_changeOrderPrice_cashondelivery'))
    suite.addTest(changeOrderPrice('test_AlreadypaidChangeOrderPrice_cashondelivery'))
    suite.addTest(changeOrderPrice('test_AlreadCancelChangeOrderPrice_cashondelivery'))
    suite.addTest(changeOrderPrice('test_RestoreOriginalPrice_cashondelivery'))
    suite.addTest(changeOrderPrice('test_AddChangeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_ReduceChangeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_changeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_AlreadypaidChangeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_DeliverGoodsChangeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_ReceivedGoodsChangeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_AlreadCancelChangeOrderPrice_Onlinepayment'))
    suite.addTest(changeOrderPrice('test_RestoreOriginalPrice_Onlinepayment'))
    return suite

