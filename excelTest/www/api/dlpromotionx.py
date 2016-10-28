#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlpromotionx:
    def __init__(self,ini_file='../../config/http_config.ini'):
        # 从配置文件中读取接口服务器IP、域名，端口
        config = configparser.ConfigParser()
        config.read(ini_file)
        self.dlpromotionxhost = config['HTTP']['dlpromotionxhost']
        self.dlpromotionxport = config['HTTP']['dlpromotionxport']


    #创建推送优惠券和红包
    def createDealerPushActivity(self,couponId1=None,couponTypeId1=None,prizePlaces1=None,createPerson1=None,couponId2=None,couponTypeId2=None,prizePlaces2=None,createPerson2=None,activityName=None,activityType=None,
                      pushList1=None,pushList2=None,pushList3=None,createPersonName=None,createPerson=None,notice=None):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/activity'
        data = {'activityDetailDtos':[
            {
                'couponId':couponId1,
                'couponTypeId':couponTypeId1,
                'prizePlaces':prizePlaces1,
                'createPerson':createPerson1
            },
            {
                'couponId':couponId2,
                'couponTypeId':couponTypeId2,
                'prizePlaces':prizePlaces2,
                'createPerson':createPerson2
            }
        ],
            'activityName':activityName,
            'activityType':activityType,
            'pushList':[
                pushList1,
                pushList2,
                pushList3
            ],
            'createPersonName':createPersonName,
            'createPerson':createPerson,
            'notice':notice
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res


    def createDealerActivity(self,dealerCouponName,dealerCouponType,dealerName,dealerId,totalNum,totalAmount,effectiveTime,uneffectiveTime,availableChannel,goodsId,goodsName,
                 areaLimit,platformLimit,createPersonName,createPerson,couponMinAmt,effectiveAmt,couponPriority,packageAmount,packageAmt,activityType,issueWay,
                 autoEnable,autoDisable,approvalAutoEnable,releaseCompletionDisable,limitNum,showWay,getWay,notice):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/activity'
        data = {}
        data['dealerCouponDto'] = {}
        data['dealerCouponDto']['dealerCouponName'] = dealerCouponName
        data['dealerCouponDto']['dealerCouponType'] = dealerCouponType
        data['dealerCouponDto']['dealerName'] = dealerName
        data['dealerCouponDto']['dealerId'] = dealerId
        data['dealerCouponDto']['totalNum'] = totalNum
        data['dealerCouponDto']['totalAmount'] = totalAmount
        data['dealerCouponDto']['effectiveTime'] = effectiveTime
        data['dealerCouponDto']['uneffectiveTime'] = uneffectiveTime
        data['dealerCouponDto']['availableChannel'] = availableChannel
        data['dealerCouponDto']['goodsId'] = goodsId
        data['dealerCouponDto']['goodsName'] = goodsName
        data['dealerCouponDto']['areaLimit'] = areaLimit
        data['dealerCouponDto']['platformLimit'] = platformLimit
        data['dealerCouponDto']['createPersonName'] = createPersonName
        data['dealerCouponDto']['createPerson'] = createPerson
        data['dealerCouponDto']['dealerCouponAmounts'] = {}
        data['dealerCouponDto']['dealerCouponAmounts']['couponMinAmt'] = couponMinAmt
        data['dealerCouponDto']['dealerCouponAmounts']['effectiveAmt'] = effectiveAmt
        data['dealerCouponDto']['dealerCouponAmounts']['couponPriority'] = couponPriority
        data['dealerCouponDto']['dealerCouponAmounts']['packageAmount'] = packageAmount
        data['dealerCouponDto']['dealerCouponAmounts']['packageAmt'] = packageAmt
        data['dealerCouponDto']['activityType'] = activityType
        data['dealerCouponDto']['issueWay'] = issueWay
        data['dealerCouponDto']['autoEnable'] = autoEnable
        data['dealerCouponDto']['autoDisable'] = autoDisable
        data['dealerCouponDto']['approvalAutoEnable'] = approvalAutoEnable
        data['dealerCouponDto']['releaseCompletionDisable'] = releaseCompletionDisable
        data['dealerCouponDto']['limitNum'] = limitNum
        data['dealerCouponDto']['showWay'] = showWay
        data['dealerCouponDto']['getWay'] = getWay
        data['dealerCouponDto']['notice'] = notice
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    #编辑优惠券、红包
    def updateDealerActivity(self,activityId,autoEnable,autoDisable,status):
        #PUT /dealer/coupon/{dealerCouponId}
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/coupon/' + activityId
        data = {
            'activityId':activityId,
            'autoEnable':autoEnable,
            'autoDisable':autoDisable,
            'status':status
        }
        response = requests.put(url,json=data)
        res=json.loads(response.content)
        return res

    #条件查询经销商的优惠券、红包
    def queryDealerActivity(self,dealerCouponType=None,dealerCouponName=None,dealerCouponId=None,effectiveTimeBegin=None,effectiveTimeEnd=None,uneffectiveTimeBegin=None,uneffectiveTimeEnd=None,
                            gmtCreateBegin=None,gmtCreateEnd=None,dealerName=None,goodsId=None,status=None,sort=None,pageIndex=None,pageSize=None):
        #POST /dealer/coupon
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/coupon'
        data = {
            'dealerCouponType':dealerCouponType,
            'dealerCouponName':dealerCouponName,
            'dealerCouponId':dealerCouponId,
            'effectiveTimeBegin':effectiveTimeBegin,
            'effectiveTimeEnd':effectiveTimeEnd,
            'uneffectiveTimeBegin':uneffectiveTimeBegin,
            'uneffectiveTimeEnd':uneffectiveTimeEnd,
            'gmtCreateBegin':gmtCreateBegin,
            'gmtCreateEnd':gmtCreateEnd,
            'dealerName':dealerName,
            'goodsId':goodsId,
            'status':status,
            'sort':sort,
            'pageIndex':pageIndex,
            'pageSize':pageSize
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    #条件查询推送
    def queryDealerPushActivity(self,activityName,gmtCreateBegin,gmtCreateEnd,createPersonName):
        #POST /dealer/pushcoupon
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/pushcoupon'
        data = {
            'activityName':activityName,
            'gmtCreateBegin':gmtCreateBegin,
            'gmtCreateEnd':gmtCreateEnd,
            'createPersonName':createPersonName
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res


    #优惠券、红包名称判重
    def isRepeated(self,dealerCouponName,dealerCouponType,flag):
        #GET /dealer/coupon?dealerCouponType={xx}&flag={x}&dealerCouponName={xxx}
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/coupon'
        data = {
            'dealerCouponType':dealerCouponType,
            'dealerCouponName':dealerCouponName,
            'flag':flag
        }
        response = requests.get(url,params=data)
        res=json.loads(response.content)
        return res


    def createDealerTrading(self,companyId,activityId):
        #POST /dealer/create_dealer_trading
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/create_dealer_trading'
        data = {
            'companyId':companyId,
            'activityId':activityId
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    def shareDealerTrading(self,userPhone,activityId):
        #POST /dealer/share_dealer_trading
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/share_dealer_trading'
        data = {
            'userPhone':userPhone,
            'activityId':activityId
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

