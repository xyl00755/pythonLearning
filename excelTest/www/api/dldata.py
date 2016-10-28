#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dldata:
    def __init__(self, ini_file='../../config/http_config.ini'):
        # 从配置文件中读取接口服务器IP、域名，端口
        config = configparser.ConfigParser()
        config.read(ini_file)
        self.dldatahost = config['HTTP']['dldatahost']
        self.dldataport = config['HTTP']['dldataport']

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
        res = json.loads(response.content)
        return res