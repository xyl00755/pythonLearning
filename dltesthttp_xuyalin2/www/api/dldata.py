#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dldata:
    def __init__(self, ini_file='../../config/env.ini'):
        # 从配置文件中读取接口服务器IP、域名，端口
        configEnv = configparser.ConfigParser()
        configEnv.read(ini_file)
        envName = configEnv['ENV']['env']
        config = configparser.ConfigParser()
        config.read('../../config/http_config.ini')
        self.dldatahost = config[envName]['dldatahost']
        self.dldataport = config[envName]['dldataport']

    # 经销商红包抵扣明细查询接口.提供运营经销商红包抵扣明细列表查询功能
    def queryDealerCouponOnAdmin(self, couponEntityId=None, couponId=None, couponName=None, payerName=None,
                                 sellerName=None, sellerId=None, orderNo=None, couponUseFlg=None, orderStatus=None,
                                 couponUseStartTime=None, couponUseEndTime=None, couponReceiveStartTime=None,
                                 couponReceiveEndTime=None, sort=None, pageIndex=None, pageSize=None):
        # POST http://data.danlu.com/V1/dealer_coupon
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/dealer_coupon'
        data = {
            "couponEntityId" : couponEntityId,
            "couponId" : couponId,
            "couponName" : couponName,
            "payerName" : payerName,
            "sellerName" : sellerName,
            "sellerId" : sellerId,
            "orderNo":orderNo,
            "couponUseFlg" : couponUseFlg,
            "orderStatus" : orderStatus,
            "couponUseStartTime" : couponUseStartTime,
            "couponUseEndTime" : couponUseEndTime,
            "couponReceiveStartTime" : couponReceiveStartTime,
            "couponReceiveEndTime" : couponReceiveEndTime,
            "sort" : sort,
            "pageIndex" : pageIndex,
            "pageSize" : pageSize
        }
        response = requests.post(url, json=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    # 经销商红包抵扣明细查询接口.提供交易平台经销商红包抵扣明细列表查询功能
    def queryDealerCouponOnMall(self, couponEntityId=None, couponId=None, couponName=None, payerName=None,
                                 sellerName=None, sellerId=None, orderNo=None, couponUseFlg=None, orderStatus=None,
                                 couponUseStartTime=None, couponUseEndTime=None, couponReceiveStartTime=None,
                                 couponReceiveEndTime=None, sort=None, pageIndex=None, pageSize=None):
        # GET http://data.danlu.com/V1/cross/dealer_coupon
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/cross/dealer_coupon'
        data = {
            "couponEntityId": couponEntityId,
            "couponId": couponId,
            "couponName": couponName,
            "payerName": payerName,
            "sellerName": sellerName,
            "sellerId": sellerId,   #交易平台调用必选参数
            "couponUseFlg": couponUseFlg,
            "orderStatus": orderStatus,
            "couponUseStartTime": couponUseStartTime,
            "couponUseEndTime": couponUseEndTime,
            "couponReceiveStartTime": couponReceiveStartTime,
            "couponReceiveEndTime": couponReceiveEndTime,
            "sort": sort,
            "pageIndex": pageIndex,
            "pageSize": pageSize
        }
        response = requests.get(url, params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res



    # 提供运营经销商红包抵扣明细发放总金额，抵扣总金额查询功能
    def queryCouponTotalAmtOnAdmin(self, couponEntityId=None,couponId=None,couponName=None,payerName=None,sellerName=None,
                                sellerId=None,orderNo=None,couponUseFlg=None,orderStatus=None,couponUseStartTime=None,
                                couponUseEndTime=None,couponReceiveStartTime=None,couponReceiveEndTime=None):
        # POST http://data.danlu.com/V1/dealer_coupon/total_amt
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/dealer_coupon/total_amt'
        data = {
            "couponEntityId": couponEntityId,
            "couponId": couponId,
            "couponName": couponName,
            "payerName": payerName,
            "sellerName": sellerName,
            "sellerId": sellerId,
            "orderNo": orderNo,
            "couponUseFlg": couponUseFlg,
            "orderStatus": orderStatus,
            "couponUseStartTime": couponUseStartTime,
            "couponUseEndTime": couponUseEndTime,
            "couponReceiveStartTime": couponReceiveStartTime,
            "couponReceiveEndTime": couponReceiveEndTime
        }
        response = requests.post(url, json=data)
        response.connection.close()
        res = json.loads(response.content)
        return res


    # 提供交易经销商红包抵扣明细发放总金额，抵扣总金额查询功能
    def queryCouponTotalAmtOnMall(self, couponEntityId=None,couponId=None,couponName=None,payerName=None,sellerName=None,
                                sellerId=None,orderNo=None,couponUseFlg=None,orderStatus=None,couponUseStartTime=None,
                                couponUseEndTime=None,couponReceiveStartTime=None,couponReceiveEndTime=None):
        # GET http://data.danlu.com/V1/cross/dealer_coupon/total_amt
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/cross/dealer_coupon/total_amt'
        data = {
                "couponEntityId": couponEntityId,
                "couponId": couponId,
                "couponName": couponName,
                "payerName": payerName,
                "sellerName": sellerName,
                "sellerId": sellerId,
                "orderNo": orderNo,
                "couponUseFlg": couponUseFlg,
                "orderStatus": orderStatus,
                "couponUseStartTime": couponUseStartTime,
                "couponUseEndTime": couponUseEndTime,
                "couponReceiveStartTime": couponReceiveStartTime,
                "couponReceiveEndTime": couponReceiveEndTime
            }
        response = requests.get(url, params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res


    #提供运营平台经销商优惠劵抵扣明细列表查询功能
    def queryDealerBenefitUsedOnAdmin(self, couponEntityId=None,couponId=None,couponName=None,payerName=None,
                                  sellerName=None,sellerId=None,orderNo=None,couponUseFlg=None,orderStatus=None,
                                  couponUseStartTime=None,couponUseEndTime=None,couponReceiveStartTime=None,
                                  couponReceiveEndTime=None,sort=None,pageIndex=None,pageSize=None):
        # POST http://data.danlu.com/V1/dealer_benefit
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/dealer_benefit'
        data = {
                "couponEntityId": couponEntityId,
                "couponId": couponId,
                "couponName": couponName,
                "payerName": payerName,
                "sellerName": sellerName,
                "sellerId": sellerId,
                "orderNo": orderNo,
                "couponUseFlg": couponUseFlg,
                "orderStatus": orderStatus,
                "couponUseStartTime": couponUseStartTime,
                "couponUseEndTime": couponUseEndTime,
                "couponReceiveStartTime": couponReceiveStartTime,
                "couponReceiveEndTime": couponReceiveEndTime,
                "sort": sort,
                "pageIndex": pageIndex,
                "pageSize": pageSize
            }
        response = requests.post(url, json=data)
        response.connection.close()
        res = json.loads(response.content)
        return res



    #提供交易平台经销商优惠劵抵扣明细列表查询功能
    def queryDealerBenefitUsedOnMall(self, couponEntityId=None,couponId=None,couponName=None,payerName=None,
                                  sellerName=None,sellerId=None,orderNo=None,couponUseFlg=None,orderStatus=None,
                                  couponUseStartTime=None,couponUseEndTime=None,couponReceiveStartTime=None,
                                  couponReceiveEndTime=None,sort=None,pageIndex=None,pageSize=None):
        # GET http://data.danlu.com/V1/cross/dealer_benefit
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/cross/dealer_benefit'
        data = {
                "couponEntityId": couponEntityId,
                "couponId": couponId,
                "couponName": couponName,
                "payerName": payerName,
                "sellerName": sellerName,
                "sellerId": sellerId,
                "orderNo": orderNo,
                "couponUseFlg": couponUseFlg,
                "orderStatus": orderStatus,
                "couponUseStartTime": couponUseStartTime,
                "couponUseEndTime": couponUseEndTime,
                "couponReceiveStartTime": couponReceiveStartTime,
                "couponReceiveEndTime": couponReceiveEndTime,
                "sort": sort,
                "pageIndex": pageIndex,
                "pageSize": pageSize
            }
        response = requests.get(url, params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    #提供运营平台经销商优惠劵抵扣明细发放总金额，抵扣总金额查询功能
    def queryDealerBenefitTotalAmtOnAdmin(self, couponEntityId=None,couponId=None,couponName=None,payerName=None,
                                     sellerName=None,sellerId=None,orderNo=None,couponUseFlg=None,orderStatus=None,
                                     couponUseStartTime=None,couponUseEndTime=None,couponReceiveStartTime=None,
                                     couponReceiveEndTime=None,):
        #POST http: // data.danlu.com / V1 / dealer_coupon / total_amt
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/dealer_benefit/total_amt'
        data ={
                "couponEntityId": couponEntityId,
                "couponId": couponId,
                "couponName": couponName,
                "payerName": payerName,
                "sellerName": sellerName,
                "sellerId": sellerId,
                "orderNo": orderNo,
                "couponUseFlg": couponUseFlg,
                "orderStatus": orderStatus,
                "couponUseStartTime": couponUseStartTime,
                "couponUseEndTime": couponUseEndTime,
                "couponReceiveStartTime": couponReceiveStartTime,
                "couponReceiveEndTime": couponReceiveEndTime,
            }
        response = requests.post(url, json=data)
        response.connection.close()
        res = json.loads(response.content)
        return res


    #提供运营平台经销商优惠劵抵扣明细发放总金额，抵扣总金额查询功能
    def queryDealerBenefitTotalAmtOnMall(self, couponEntityId=None,couponId=None,couponName=None,payerName=None,
                                     sellerName=None,sellerId=None,orderNo=None,couponUseFlg=None,orderStatus=None,
                                     couponUseStartTime=None,couponUseEndTime=None,couponReceiveStartTime=None,
                                     couponReceiveEndTime=None,):
        #GET http://data.danlu.com/V1/cross/dealer_coupon/total_amt
        url = 'http://' + self.dldatahost + ':' + str(self.dldataport) + '/V1/cross/dealer_benefit/total_amt'
        data ={
                "couponEntityId": couponEntityId,
                "couponId": couponId,
                "couponName": couponName,
                "payerName": payerName,
                "sellerName": sellerName,
                "sellerId": sellerId,
                "orderNo": orderNo,
                "couponUseFlg": couponUseFlg,
                "orderStatus": orderStatus,
                "couponUseStartTime": couponUseStartTime,
                "couponUseEndTime": couponUseEndTime,
                "couponReceiveStartTime": couponReceiveStartTime,
                "couponReceiveEndTime": couponReceiveEndTime,
            }
        response = requests.get(url, params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res

    def setDealer_coupon(self,dealer_coupon=None,couponId=None,couponName=None,payerName=None,sellerName=None,sellerId=None,couponUseFlg=None,orderStatus=None,couponUseStartTime=None,couponUseEndTime=None,couponReceiveStartTime=None,couponReceiveEndTime=None,sort=None,pageIndex=None,pageSize=None,):
        #POST /data.danlu.com/V1/dealer_coupon
        url =  'http://' + self.dldatahost + ':' + str(self.dldataport) + '/data.danlu.com/V1/dealer_coupon'
        data = {'couponEntityId': couponEntityId,
                'couponId': couponId,
                'couponName': couponName,
                'payerName': payerName,
                'sellerName': sellerName,
                'sellerId': sellerId,
                'couponUseFlg': couponUseFlg,
                'orderStatus': orderStatus,
                'couponUseStartTime': couponUseStartTime,
                'couponUseEndTime': couponUseEndTime,
                'couponReceiveStartTime': couponReceiveStartTime,
                'sort': sort,
                'pageIndex': pageIndex,
                'pageSize': pageSize
        }
        response = requests.post(url,data)
        return response.content


