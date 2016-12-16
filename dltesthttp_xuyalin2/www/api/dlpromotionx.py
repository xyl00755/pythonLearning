#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlpromotionx:
    def __init__(self):
        # 从配置文件中读取接口服务器IP、域名，端口
        from www.common.config import config
        httpConfig = config().confighttp
        self.dlpromotionxhost = httpConfig['dlpromotionxhost']
        self.dlpromotionxport = httpConfig['dlpromotionxport']


    #创建推送优惠券和红包的活动
    def createDealerPushActivity(self,activityName=None,activityType=None,createPersonName=None,createPerson=None,notice=None, dealerId=None,pushList1=None,pushList2=None,couponId=None,couponTypeId=None,prizePlaces=None):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/activity'
        data = {
            'activityName':activityName,
            'activityType':activityType,
            'createPersonName':createPersonName,
            'createPerson':createPerson,
            'notice':notice,
            'dealerId':dealerId,
            'pushList':[
                pushList1,
                pushList2
            ],
            'activityDetailDtos':[
            {
                'couponId':couponId,
                'couponTypeId':couponTypeId,
                'prizePlaces':prizePlaces
            }
        ]
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    def nameMatching(self,dealerName=None,companyType=None,pageIndex=None,pageSize=None):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealerCoupon/nameMatching'
        data = {
            'dealerName':dealerName,
            'companyType':companyType,
            'pageIndex':pageIndex,
            'pageSize':pageSize
        }
        response = requests.get(url,params = data)
        res = json.loads(response.content)
        return res

    def goodsMatching(self,goodsName=None,pageIndex=None,pageSize=None):
        url =  'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealerCoupon/goodsMatching'
        data = {
            'goodsName':goodsName,
            'pageIndex':pageIndex,
            'pageSize':pageSize
        }
        response = requests.get(url,params = data)
        res = json.loads(response.content)
        return res

    # def getGoodsCoupon(self,goodsIds=None,companyId=None):
    #     url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/getGoodsCoupon'
    #     data = {
    #         'goodsIds':goodsIds,
    #         'companyId':companyId,
    #     }
    #     response = requests.get(url, params = data)
    #     return response.content

    def getCenterCouponDetail(self,companyId=None,dealerCouponType=None,categoryCode=None,brandIds=None,dealerName=None,goodsName=None,showWay=None,pageIndex=None,pageSize=None,sortParams=None):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealerCoupon/getCenterCouponDetail'
        data = {
                "companyId": companyId,
                "dealerCouponType": dealerCouponType,
                "categoryCode": categoryCode,
                "brandIds": brandIds,
                "dealerName": dealerName,
                "goodsName": goodsName,
                "showWay":showWay,
                "pageIndex": pageIndex,
                "pageSize": pageSize,
                "sortParams": sortParams
        }
        response = requests.post(url, json = data)
        res = json.loads(response.content)
        return res

    # def getGoodsCouponDetail(self, goodsIds = None, companyId = None, dealerCouponType = None):
    #     url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/getGoodsCouponDetail'
    #     data = {
    #         'goodsIds':goodsIds,
    #         'companyId':companyId,
    #         'dealerCouponType':dealerCouponType
    #     }
    #     response = requests.get(url, params = data)
    #     return response.content

    #创建领取优惠券和红包的活动
    def createDealerActivity(self,dealerCouponName=None,dealerCouponType=None,dealerName=None,dealerId=None,totalNum=None,totalAmount=None,effectiveTime=None,uneffectiveTime=None,availableChannel=None,goodsId=None,goodsName=None,
                 areaLimit=None,dealerCouponImgUrl=None,platformLimit=None,createPersonName_coupon=None,createPerson_coupon=None,couponMinAmt=None,effectiveAmt=None,couponPriority=None,packageAmount=None,activityType=None,
                 issueWay=None,autoEnable=None,autoDisable=None,approvalAutoEnable=None,releaseCompletionDisable=None,limitNum=None,showWay=None,getWay=None,createPersonName=None,createPerson=None,notice=None):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/activity'
        data = {
            'dealerCouponDto':
                    {
                        'dealerCouponName':dealerCouponName,
                        'dealerCouponType':dealerCouponType,
                        'dealerName':dealerName,
                        'dealerId':dealerId,
                        'totalNum':totalNum,
                        'totalAmount':totalAmount,
                        'effectiveTime':effectiveTime,
                        'uneffectiveTime':uneffectiveTime,
                        'availableChannel':availableChannel,
                        'goodsId':goodsId,
                        'goodsName':goodsName,
                        'areaLimit':areaLimit,
                        'dealerCouponImgUrl':dealerCouponImgUrl,
                        'createPersonName':createPersonName_coupon,
                        'createPerson':createPerson_coupon,
                        'dealerCouponAmounts':[
                            {
                                'couponMinAmt':couponMinAmt,
                                'effectiveAmt':effectiveAmt,
                                'couponPriority':couponPriority,
                                'packageAmount':packageAmount,
                            }
                        ]
                    },
            'activityType':activityType,
            'issueWay':issueWay,
            'autoEnable':autoEnable,
            'autoDisable':autoDisable,
            'approvalAutoEnable':approvalAutoEnable,
            'releaseCompletionDisable':releaseCompletionDisable,
            'limitNum':limitNum,
            'showWay':showWay,
            'getWay':getWay,
            'createPersonName':createPersonName,
            'createPerson':createPerson,
            'notice':notice
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    #编辑优惠券、红包
    def modifyDealerActivity(self,activityId=None,autoEnable=None,autoDisable=None,status=None):
        #PUT /dealer/coupon/{activityId}
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
    def queryDealerActivity(self,activityType=None,dealerCouponIdOrName=None,activityName=None,effectiveTimeBegin=None,effectiveTimeEnd=None,uneffectiveTimeBegin=None,uneffectiveTimeEnd=None,
                            gmtCreateBegin=None,gmtCreateEnd=None,dealerName=None,goodsName=None,status=None,sort=None,pageIndex=None,pageSize=None):
        #POST /dealer/coupon
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/coupon'
        data = {
            'activityType':activityType,
            'dealerCouponIdOrName':dealerCouponIdOrName,
            'activityName':activityName,
            'effectiveTimeBegin':effectiveTimeBegin,
            'effectiveTimeEnd':effectiveTimeEnd,
            'uneffectiveTimeBegin':uneffectiveTimeBegin,
            'uneffectiveTimeEnd':uneffectiveTimeEnd,
            'gmtCreateBegin':gmtCreateBegin,
            'gmtCreateEnd':gmtCreateEnd,
            'dealerName':dealerName,
            'goodsName':goodsName,
            'status':status,
            'sort':sort,
            'pageIndex':pageIndex,
            'pageSize':pageSize
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    #条件查询推送
    def queryDealerPushActivity(self,activityName=None,gmtCreateBegin=None,gmtCreateEnd=None,createPersonName=None):
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

    #删除优惠券和红包
    def deleteDealerActivity(self,activityId=None,logicDeleteFlag=1):
        #PUT /dealer/coupon/{activityId}
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/coupon/' + str(activityId)
        data = {
            'activityId':activityId,
            'logicDeleteFlag':logicDeleteFlag
        }
        response = requests.put(url,json=data)
        res=json.loads(response.content)
        return res


    #优惠券、红包名称判重
    def verifyName(self,dealerCouponName=None,dealerCouponType=None,flag=None,activityId=None):
        #POST /dealer/verifyName
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/verifyName'
        data = {
            'dealerCouponType':dealerCouponType,
            'dealerCouponName':dealerCouponName,
            'flag':flag,
            'activityId':activityId
        }
        response = requests.post(url,json=data)
        res=json.loads(response.content)
        return res

    #获取商品
    def goodsList(self,goodsNameOrNumber=None,brandIdList=None,pageIndex=None,pageSize=None):
        #POST /goods/goodsList
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/goods/goodsList'
        data = {
            'goodsNameOrNumber':goodsNameOrNumber,
            'brandIdList':brandIdList,
            'pageIndex':pageIndex,
            'pageSize':pageSize
        }
        response = requests.post(url,json=data)
        if response.status_code != 200:
            print '请求的状态码为非200'
            return
        res=json.loads(response.content)
        return res


    #x01抢券
    def createDealerTrading(self,companyId,activityId):
        #POST /dealer/create_dealer_trading
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/create_dealer_trading'
        data = {
            'companyId':companyId,
            'activityId':activityId
        }
        response = requests.post(url,json=data)
        response.connection.close()
        res=json.loads(response.content)
        return res

    #x02分享链接领取优惠券
    def shareDealerTrading(self,userPhone,activityId):
        #POST /dealer/share_dealer_trading
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/share_dealer_trading'
        data = {
            'userPhone':userPhone,
            'activityId':activityId
        }
        response = requests.post(url,json=data)
        response.connection.close()
        res=json.loads(response.content)
        return res


    # x04终端店已领取红包/优惠券个数，根据多个经销商Id查询    ---dubbo接口，不写
    # def getMoreReceivedCouponSum(self, companyId=None,dealerCouponType=None,dealerIds=None):
    #     url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealer/getMoreReceivedCouponSum'
    #     data = {
    #         "companyId": companyId,
    #         "dealerCouponType": dealerCouponType,
    #         "dealerIds": dealerIds
    #     }
    #     response = requests.get(url,params=data)
    #     response.connection.close()
    #     res = json.loads(response.content)
    #     return res

    #x08 根据类目Code，字母或者品牌名称查询品牌
    def getBrands(self, categoryCodesStr=None,initial=None,brandName=None):
        url = 'http://' + self.dlpromotionxhost + ':' + str(self.dlpromotionxport) + '/dealerCoupon/getBrands'
        data = {
            "categoryCodesStr": categoryCodesStr,
            "initial": initial,
            "brandName": brandName
        }
        response = requests.get(url,params=data)
        response.connection.close()
        res = json.loads(response.content)
        return res
