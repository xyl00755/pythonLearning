#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from www.api.webservice import *
from www.common.database import select_one
from www.common.database import update
from www.common.excel import *
from www.common.model import Shoppingcart


class createOrderTool:
    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')
    coupon2=eData('AvailableCouponsBenfits')

    # 从购物车提交商品的无促销、优惠券、红包的订单
    # payway:支付方式 1-在线支付 2-货到付款 12-混合支付 3-公司转帐
    # needInvoice:0-需要发票 1-不要发票
    # goodsNum：1-一个商品 2-两个商品
    # dealerNum：1-一个经销商 2-两个经销商
    # type：0-提交正常订单 1-提交订单异常
    # reason:0-提交订单正常 1-低于最小起售量 2-商品无价格 3-库存不足 4-商品价格变更 5-配送商支付方式改变 6-商品状态变更
    # goodsStatus：01-已上架,02-已下架,03-锁定,99-删除
    def createOrderNoPromotion(self,payWay=None,orderTotalAmt=None,needInvoice=None,goodsNum=None,dealerNum=None,type=None,reason=None,goodsStatus=None):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        if goodsNum==1:
            ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
            shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch1.goodsId)
        else:
            ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
            shopcart1 = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch1.goodsId)
            if dealerNum==1:
                ws.addShoppingcar(merchId=self.Merch2.goodsId, merchCount='1', sellerId=self.Merch2.seller_store_id, sellerName=self.Merch2.sellerName)
                shopcart2 = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch2.goodsId)
            else:
                ws.addShoppingcar(merchId=self.Merch4.goodsId, merchCount='1', sellerId=self.Merch4.seller_store_id, sellerName=self.Merch4.sellerName)
                shopcart2 = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch4.goodsId)
        ws.checkSwitch()
        if needInvoice=='0':
            invoice = {"invoiceId":self.UserShop.invoiceId, "invoiceType":"N011","needInvoice":needInvoice,"invoiceHeader":self.UserShop.invoiceHeader}
        else:
            invoice = {"needInvoice":needInvoice}
        deliverAddress = {"deliverAddress":self.UserShop.deliverAddress, "deliverMobile":self.UserShop.deliverMobile, "deliverPerson":self.UserShop.deliverPerson}
        sellerList = []
        if goodsNum==1:
            sellerList.append({"sellerId":self.Merch1.shopcartSellerId,"sellerName":self.Merch1.sellerName,"isYijipayAccount":self.Merch1.isYijipayAccount,"paymentFlag":self.Merch1.paymentFlag,"codFlag":self.Merch1.codFlag,
                           "supportVatInvoice":self.Merch1.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","merchList":
                               [{"id":shopcart.id,"merchId":self.Merch1.goodsId,"merchBarCode":self.Merch1.productBarCode}]})
        elif dealerNum==1:
            sellerList.append({"sellerId":self.Merch1.shopcartSellerId,"sellerName":self.Merch1.sellerName,"isYijipayAccount":self.Merch1.isYijipayAccount,"paymentFlag":self.Merch1.paymentFlag,"codFlag":self.Merch1.codFlag,
                           "supportVatInvoice":self.Merch1.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","merchList":
                               [{"id":shopcart1.id,"merchId":self.Merch1.goodsId,"merchBarCode":self.Merch1.productBarCode},
                                {"id":shopcart2.id,"merchId":self.Merch2.goodsId,"merchBarCode":self.Merch2.productBarCode}]})
        else:
            sellerList.append({"sellerId":self.Merch1.shopcartSellerId,"sellerName":self.Merch1.sellerName,"isYijipayAccount":self.Merch1.isYijipayAccount,"paymentFlag":self.Merch1.paymentFlag,"codFlag":self.Merch1.codFlag,
                           "supportVatInvoice":self.Merch1.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","merchList":
                               [{"id":shopcart1.id,"merchId":self.Merch1.goodsId,"merchBarCode":self.Merch1.productBarCode}]})
            sellerList.append({"sellerId":self.Merch4.shopcartSellerId,"sellerName":self.Merch4.sellerName,"isYijipayAccount":self.Merch4.isYijipayAccount,"paymentFlag":self.Merch4.paymentFlag,"codFlag":self.Merch4.codFlag,
                           "supportVatInvoice":self.Merch4.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","merchList":
                               [{"id":shopcart2.id,"merchId":self.Merch4.goodsId,"merchBarCode":self.Merch4.productBarCode}]})
        if type==0:
            order = ws.createOrderByShoppingcart_V3(payWay=payWay,orderTotalAmt=orderTotalAmt,invoice=invoice, deliverAddress=deliverAddress, sellerList=sellerList)
        else:
            #order = 'type=1,提交订单异常情况！'
            if reason==1:
                update('update dlmerchandise.dl_goods_price set init_sale_quantity_s1=? where goods_id=?',10,self.Merch1.goodsId)
            elif reason==2:
                update('update dlmerchandise.dl_goods_price set price_s1=? where goods_id=? and step_type_code=?',None,self.Merch1.goodsId,'S011')
            elif reason==3:
                update('update dlmerchandise.dl_goods set on_hand_inventory=? where goods_id=?',0,self.Merch1.goodsId)
            elif reason==4:
                update('update dlmerchandise.dl_goods_price set price_s1=? where goods_id=? and step_type_code=?',48000,self.Merch1.goodsId,'S011')
            elif reason==5:
                update('update dlcompany.dl_store_base_info set isCOD = ? where store_id = ?', 0,self.Merch1.storeId)
            elif reason==6 and goodsStatus==2:
                update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','02',self.Merch1.goodsId)
            elif reason==6 and goodsStatus==3:
                update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','03',self.Merch1.goodsId)
            elif reason==6 and goodsStatus==99:
                update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','99',self.Merch1.goodsId)
            order = ws.createOrderByShoppingcart_V3(payWay=payWay,orderTotalAmt=orderTotalAmt,invoice=invoice, deliverAddress=deliverAddress, sellerList=sellerList)
        return order

    # 从购物车提交商品带有有促销
    # merchCount:购物车商品数量
    # promotionType：促销类型 0-满赠 1-满减
    # reductionType：满减类型 0-减单价 1-减总额
    def createOrderPromotion(self,orderTotalAmt=None,merchCount=None,promotionType=None,reductionType=None,ruleId=None):
        ws=webservice()
        ws.login(self.UserShop.username,self.UserShop.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop.userId, self.Merch1.goodsId)
        deliverAddress = {"deliverAddress":self.UserShop.deliverAddress, "deliverMobile":self.UserShop.deliverMobile, "deliverPerson":self.UserShop.deliverPerson}
        invoice = {"invoiceId":self.UserShop.invoiceId, "invoiceType":"N011","needInvoice":'0',"invoiceHeader":self.UserShop.invoiceHeader}
        sellerList = []
        if promotionType==1:
            promotionIdSql=select_one('select * from dlpromotion.dl_full_reduction_rule where full_reduction_rule_id=?',ruleId)
            ws.modifyShoppingcartCount(shoppingCartId=shopcart.id,merchId=self.Merch1.goodsId,merchCount=merchCount,sellerId=self.Merch1.sellerId,usePromotion='0',promotionId=promotionIdSql.full_reduction_id,
                                       promotionType='1',reductionType=reductionType,ruleId=ruleId)
            sellerList.append({"sellerId":self.Merch1.shopcartSellerId,"sellerName":self.Merch1.sellerName,"isYijipayAccount":self.Merch1.isYijipayAccount,"paymentFlag":self.Merch1.paymentFlag,"codFlag":self.Merch1.codFlag,
                           "supportVatInvoice":self.Merch1.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","merchList":
                               [{"id":shopcart.id,"merchId":self.Merch1.goodsId,"merchBarCode":self.Merch1.productBarCode,"promotionId":promotionIdSql.full_reduction_id,
                                 "promotionType":'1',"reductionFlg":reductionType,"ruleId":ruleId}]})
        else:
            promotionIdSql=select_one('select * from dlpromotion.dl_full_presentation_rule where full_presentation_rule_id=?',ruleId)
            ws.modifyShoppingcartCount(shoppingCartId=shopcart.id,merchId=self.Merch1.goodsId,merchCount=merchCount,sellerId=self.Merch1.sellerId,usePromotion='0',promotionId=promotionIdSql.full_presentation_id,
                                       promotionType='0',reductionType=reductionType,ruleId=ruleId)
            sellerList.append({"sellerId":self.Merch1.shopcartSellerId,"sellerName":self.Merch1.sellerName,"isYijipayAccount":self.Merch1.isYijipayAccount,"paymentFlag":self.Merch1.paymentFlag,"codFlag":self.Merch1.codFlag,
                           "supportVatInvoice":self.Merch1.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","merchList":
                               [{"id":shopcart.id,"merchId":self.Merch1.goodsId,"merchBarCode":self.Merch1.productBarCode,"promotionId":promotionIdSql.full_presentation_id,
                                 "promotionType":'0',"reductionFlg":reductionType,"ruleId":ruleId}]})
        ws.checkSwitch()
        order = ws.createOrderByShoppingcart_V3(payWay='2',orderTotalAmt=orderTotalAmt,deliverAddress=deliverAddress,invoice=invoice,sellerList=sellerList)
        return order

    def creatOrderCoupon(self,orderTotalAmt=None):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        #领取经销商优惠券
        ws.achieveCoupon(activityId=self.coupon2.benefitActivityId2)
        time.sleep(60)
        getBenefit=ws.getDealerCouponList(couponStatus='01',dealerCouponType='11',page=1,rows=15)
        couponBenefitCode=None
        couponBenefitAmt=None
        for i in range(len(getBenefit.model['couponList'])):
            if getBenefit.model['couponList'][i]['couponName']=='测试自动化优惠券':
                couponBenefitCode=getBenefit.model['couponList'][i]['couponCode']
                couponBenefitAmt=getBenefit.model['couponList'][i]['couponAmt']
        achieve=ws.achieveCoupon(activityId=self.coupon2.couponActivityId2)
        time.sleep(60)
        getCoupon=ws.getDealerCouponList(couponStatus='01',dealerCouponType='10',page=1,rows=15)
        couponCode=None
        couponAmt=None
        for i in range(len(getBenefit.model['couponList'])):
            if getCoupon.model['couponList'][i]['couponName']=='测试自动化配送商02红包':
                couponCode=getCoupon.model['couponList'][i]['couponCode']
                couponAmt=getCoupon.model['couponList'][i]['couponAmt']
        ws.addShoppingcar(merchId=self.Merch4.goodsId, merchCount='1', sellerId=self.Merch4.seller_store_id, sellerName=self.Merch4.sellerName)
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop2.userId, self.Merch4.goodsId)
        deliverAddress = {"deliverAddress":self.UserShop2.deliverAddress, "deliverMobile":self.UserShop2.deliverMobile, "deliverPerson":self.UserShop2.deliverPerson}
        invoice = {"needInvoice":'1'}
        sellerList = []
        sellerList.append({"sellerId":self.Merch4.shopcartSellerId,"sellerName":self.Merch4.sellerName,"isYijipayAccount":self.Merch4.isYijipayAccount,"paymentFlag":self.Merch4.paymentFlag,"codFlag":self.Merch4.codFlag,
                           "supportVatInvoice":self.Merch4.supportVatInvoice,"comment":"createOrderByShoppingcartNew comment.","dealerCouponList":[{"dealerCouponCode":couponCode,"dealerCouponAmt":couponAmt}],
                           "merchList": [{"id":shopcart.id,"merchId":self.Merch4.goodsId,"merchBarCode":self.Merch4.productBarCode,
                                          "dealerBenefit":{"couponCode":couponBenefitCode,"couponAmt":couponBenefitAmt}}]})
        ws.checkSwitch()
        order = ws.createOrderByShoppingcart_V3(payWay='2',orderTotalAmt=orderTotalAmt,deliverAddress=deliverAddress,invoice=invoice,sellerList=sellerList)
        return order








    #恢复涉及的数据库信息
    def resetDataBySql(self):
        update('update dlmerchandise.dl_goods_price set price_s1=? where goods_id=? and step_type_code=?',12000,self.Merch1.goodsId,'S011')
        update('update dlmerchandise.dl_goods set goods_status=? where goods_id=?','01',self.Merch1.goodsId)
        update('update dlmerchandise.dl_goods set on_hand_inventory=? where goods_id=?',self.Merch1.onHandInventory,self.Merch1.goodsId)
        update('update dlmerchandise.dl_goods_price set init_sale_quantity_s1=? where goods_id=?',self.Merch1.saleQuantityS1,self.Merch1.goodsId)
        update('update dlcompany.dl_store_base_info set isCOD = ? where store_id = ?', 1,self.Merch1.storeId)
        update('delete from danlu_cd_database.dl_shoppingcart where user_id=?',self.UserShop.userId)


