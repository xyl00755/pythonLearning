#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
from datetime import datetime
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlmall:
    def __init__(self):
        # 从配置文件中读取接口服务器IP、域名，端口
        from www.common.config import config
        httpConfig = config().confighttp
        self.dlmallhost = httpConfig['dlmallhost']
        self.dlmallport = httpConfig['dlmallport']
        self.ssohost = httpConfig['ssohost']
        self.ssoport = httpConfig['ssoport']

    def login(self, username, password):
        s = requests.Session()

        #GET请求，加载登陆页面，获取到lt、execution,url = 'http://123.57.244.205:9003/main/newLogin.html'
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/main/newLogin.html'
        response = s.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        lt = str(soup.find("input", {"name": "lt"})['value'])
        execution = str(soup.find("input", {"name": "execution"})['value'])

        #GET请求，请求验证码
        url2 = 'http://' + self.ssohost + ':' + str(self.ssoport) + '/validateCode.html'
        s.get(url2)

        #PORT请求，登陆, url3 = 'http://123.57.152.182:9002/login?service=http://123.57.244.205:9003/common/caslogin.html'
        url3 = 'http://' + self.ssohost + ':' + str(self.ssoport) + '/login?service=http://' + self.ssohost + ':' + str(self.ssoport) + '/common/caslogin.html'
        playdata = {'username': username,
                    'password': password,
                    'validateCode': '1111',
                    'lt':lt,
                    'execution':execution,
                    '_eventId': 'submit'}
        s.post(url3, data=playdata,allow_redirects=True)
        return  s

    def getSellerOrdersCount(self,session):
        #http://123.57.244.205:9003/orders/getSellerOrdersCount.html?date=1474532184439
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orders/getSellerOrdersCount.html?date=1474532184439'
        response = session.get(url)
        res=json.loads(response.content)
        return res

    def saveOrderSplitInfo(self,session,status=None,minAmount=None,maxTimes=None):
        #POST /businessInfoModify/saveOrderSplitInfo.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/businessInfoModify/saveOrderSplitInfo.html'
        data={'status':status,
              'minAmount':minAmount,
              'maxTimes':maxTimes
        }
        response = session.post(url,data)
        res=json.loads(response.content)
        return res

    def splitOrder(self,session,orderNo=None):
        #GET /orderSplit/splitOrder.html?orderNo=24324354654656
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orderSplit/splitOrder.html'
        data = {'orderNo':orderNo}
        response = session.get(url,params=data)
        res=json.loads(response.content)
        return res

    def doSplitOrder(self,session,orderNo=None,splitItems=None):
        #POST /orderSplit/doSplitOrder.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orderSplit/doSplitOrder.html'
        data = {
            'orderNo':orderNo,
             'splitItems':splitItems
        }
        response = session.post(url,data)
        res=json.loads(response.content)
        return res

    def getSplitOrderInfo(self,session,orderNo=None):
        #GET /orderSplit/getSplitOrderInfo.html?orderNo=243534545465
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orderSplit/getSplitOrderInfo.html'
        data = {'orderNo':orderNo}
        response = session.get(url,params=data)
        res=json.loads(response.content)
        return res

    def getPayRate(self,session):
        #GET /dealerPayRate/payRate.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealerPayRate/payRate.html'
        data = {}
        response = session.get(url,params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    def setPayRate(self,session,payRate=None):
        #POST :/dealerPayRate/payRate.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealerPayRate/payRate.html'
        data = {'payRate':payRate}
        response = session.post(url,data=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    def getProvince(self,session):
        #POST表单 :/common/getProvince.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/common/getProvince.html'
        data = {}
        response = session.post(url,data = data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    def getCity(self,session,provinceCode):
        #POST表单 :/common/getCity.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/common/getCity.html'
        list={
            "provinceCode":provinceCode
        }
        data = {
            'search':json.dumps(list)
        }
        response = session.post(url,data = data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    def getDistrict(self,session,cityCode):
        #POST表单 :/common/getDistrict.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/common/getDistrict.html'
        list={
            "provinceCode":cityCode
        }
        data = {
            'search':json.dumps(list)
        }
        response = session.post(url,data = data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    # x03终端店已领取红包/优惠券查询:终端店查看已领取的优惠券/红包
    def getReceivedCoupon(self, session,companyId=None, dealerCouponType=None, dealerCouponEntityStatus=None, dealerIdList=None,
                          goodsId=None, pageIndex=None, pageSize=None, sort=None):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealer/getReceivedCoupon.html'
        data = {
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "dealerCouponEntityStatus": dealerCouponEntityStatus,
            "dealerIdList": dealerIdList,
            "goodsId": goodsId,
            "pageIndex": pageIndex,
            "pageSize": pageSize,
            "sort": sort
        }
        response = session.get(url, params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res


    # x05终端店已领取红包/优惠券个数
    def getReceivedCouponSum(self, session,companyId=None, dealerCouponType=None, dealerId=None):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealer/getReceivedCouponSum.html'
        data = {
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "dealerId": dealerId
        }
        response = session.get(url, params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    #x06终端店可领优惠券/红包个数展示
    def getMoreAvailableCouponSum(self, session,companyId=None,dealerCouponType=None,showWay=None,goodsId=None,dealerId=None,getWay=None):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealer/getAvailableCouponSum.html'
        data = {
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "showWay": showWay,
            "goodsId": goodsId,
            "dealerId": dealerId,
            "getWay": getWay
        }
        response = session.get(url,params=data)
        response.connection.close()
        # print url,data,response
        res = json.loads(response.content)
        return res

    #x07终端店可领 优惠券/红包展示
    def getMoreAvailableCoupon(self,session, companyId=None,dealerCouponType=None,dealerId=None,showWay=None,typeCode=None,dealerName=None,
            goodsName=None,goodsId=None,getWay=None,pageIndex=None,pageSize=None,sort=None):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealer/getAvailableCouponOfDealer.html'
        data = {
            "companyId": companyId,
            "dealerCouponType": dealerCouponType,
            "dealerId": dealerId,
            "showWay": showWay,
            "typeCode": typeCode,
            "dealerName": dealerName,
            "goodsName": goodsName,
            "goodsId": goodsId,
            "getWay": getWay,
            "pageIndex": pageIndex,
            "pageSize": pageSize,
            "sort": sort
        }
        response = session.get(url,params=data)
        response.connection.close()
        # print url,data,response.content
        res = json.loads(response.content)
        return res

    def deliveryAddressInsert(self,session,addressDetail,zipcode,deliveryPerson,deliveryMobile,deliveryTel,isDefault,areaCode):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/deliveryAddress/deliveryAddressInsert.html'
        data = {
            'addressDetail': addressDetail,
            'zipcode': zipcode,
            'deliveryPerson': deliveryPerson,
            'deliveryMobile': deliveryMobile,
            'deliveryTel': deliveryTel,
            'isDefault': isDefault,
            'areaCode': areaCode
        }
        response = session.post(url, data= data)
        res = json.loads(response.content)
        return res

    def getAddressList(self,session):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/deliveryAddress/getAddressList.html'
        response = session.post(url)
        res = json.loads(response.content)
        return res

    def deliveryAddressUpdate(self,session,addressId,addressDetail,zipcode,deliveryPerson,deliveryMobile,deliveryTel,isDefault,areaCode):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/deliveryAddress/deliveryAddressUpdate.html'
        data = {
            'addressId': addressId,
            'addressDetail': addressDetail,
            'zipcode': zipcode,
            'deliveryPerson': deliveryPerson,
            'deliveryMobile': deliveryMobile,
            'deliveryTel': deliveryTel,
            'isDefault': isDefault,
            'areaCode': areaCode
        }
        response= session.post(url,data= data)
        res = json.loads(response.content)
        return res

    def deliveryAddressDelete(self,session,addressId):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/deliveryAddress/deliveryAddressDelete.html'
        data = {
            'addressId': addressId
        }
        response = session.post(url,data= data)
        res = json.loads(response.content)
        return res

    def setDeliveryAddrDefault(self,session,addressId):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/deliveryAddress/setDeliveryAddrDefault.html'
        data = {
            'addressId':addressId
        }
        response = session.post(url,json= data)
        res = json.loads(response.content)
        return res

    def normalInvoices(self,session):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/userInvoices/normal.html'
        response = session.get(url)
        res = json.loads(response.content)
        return res

    def setDefaultInvoices(self,session,invoiceId):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/userInvoices/setDefault.html'
        data ={
            'invoiceId':invoiceId
        }
        response = session.post(url,data=data)
        res = json.loads(response.content)
        return res

    def deleteInvoices(self,session,invoiceId):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/userInvoices/delete.html'
        data ={
            'invoiceId':invoiceId
        }
        response = session.post(url,data=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    def modifyInvoices(self,session,invoiceId,invoiceHeader,invoicesType):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/userInvoices/modify.html'
        data = {
            'invoiceId':invoiceId,
            'invoiceHeader':invoiceHeader,
            'invoicesType':invoicesType
        }
        response = session.post(url,data=data)
        res = json.loads(response.content)
        return res

    def addInvoices(self,session,invoiceHeader,invoicesType,isDefault):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/userInvoices/add.html'
        data = {
            'invoiceHeader':invoiceHeader,
            'invoicesType':invoicesType,
            'isDefault': isDefault

        }
        response = session.post(url,json=data)
        res = json.loads(response.content)
        return res

    def isNeedValidate(self, session, couponId, couponAmt, couponUseAmt, length):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/isNeedValidate.html'
        ary =[]
        list = {
            "couponId": couponId,
            "couponAmt": couponAmt,
            "couponUseAmt": couponUseAmt
        }

        for i in range(length):
           ary.append(list)

        data = {
            'couponList':str(ary)
        }
        response = session.post(url, data=data)
        res = json.loads(response.content)
        return res

    def initValidate(self,session):
        url ='http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/init.html'
        response = session.get(url)
        response.connection.close()
        res = json.loads(response.content)

        return res

    def imgValidateCode(self,session):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/init.html?date='+datetime.time()
        response = session.get(url)
        res = response.status_code
        return res

    def validateImgCode(self,session,imgCode):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/validateImgCode.html'
        data = {
            'imgCode':imgCode
        }
        response = session.post(url,data=data)
        res = json.loads(response.content)
        return res

    def sendValidateMessage(self,session,phoneNo):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/sendMessage.html'
        data ={
            'phoneNo':phoneNo
        }
        response=session.post(url,data=data)
        res = response.status_code
        return res

    def validateMessage(self,session,phoneNo,messageCode):
        url ='http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/validateMessage.html'
        data = {
            'phoneNo':phoneNo,
            'messageCode':messageCode
        }
        response=session.post(url,data=data)
        res = json.loads(response.content)
        return res

    def getValidateFormInfo(self,session,phoneNo,messageCode):
        url ='http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/vilidateCode/getFormInfo.html'
        data = {
            'phoneNo':phoneNo,
            'messageCode':messageCode
        }
        response=session.post(url,data=data)
        res = json.loads(response.content)
        return res

    def usableAndUnusableCoupons(self,session,dealers):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealer/usableAndUnusableCoupons.html'
        data = dealers
        response=session.post(url,json=data)
        res = json.loads(response.content)
        return res

    def getUseFulCoupons(self,session,goodsId):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/couponx/getUseFulCoupons.html'
        data = {
            'goodsId':goodsId
        }
        response=session.get(url,params=data)
        res=json.loads(response.content)
        return res

    def orderBook(self,session,address,invoiceAndPay,dlCouponList,settlementInfo):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/Dlordersettlement/orderBook.html'
        data ={
            'address':address,
            'invoiceAndPay':invoiceAndPay,
            'dlCouponList':dlCouponList,
            'settlementInfo':settlementInfo
        }
        response=session.post(url,json=data)
        res=json.loads(response.content)
        return res

    def toTransferPage(self,session,status,checkErrorObj,onlinePay,cashOndelivery,companyTransfer):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/Dlordertransfer/toTransferPage.html '
        data = {
            'status':1,
            'checkErrorObj':checkErrorObj,
            'onlinePay':onlinePay,
            'cashOndelivery':cashOndelivery,
            'companyTransfer':companyTransfer
        }
        response=session.post(url,data=data)
        res=response.status_code
        return res

    def getGoodsCoupon(self,session, goodsIds = None, companyId = None,):
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/dealer/getGoodsCoupon.html'
        data = {
            'goodsIds':goodsIds,
            'companyId':companyId
        }
        response = session.post(url, json = data)
        response.connection.close()
        res = json.loads(response.content)
        return res


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    s = dlmall().login("x_2","123456")
    response = dlmall().getSellerOrdersCount(s)
    print response