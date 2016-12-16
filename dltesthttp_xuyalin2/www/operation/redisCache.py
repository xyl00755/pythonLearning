#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import configparser

#machine details
from www.common.config import config
httpConfig = config().confighttp
server_ip=httpConfig['redishost']
server_port=httpConfig['redisport']



def connectionToRedis():
    pool = redis.ConnectionPool(host=server_ip, port=server_port, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    return r

def deleteActivityKey(r=connectionToRedis(), couponActivityId=None,benefitActivityId=None,benefitId=None,tmlCompanyId=None):
    '''
    :param r: 默认为本页上方的redis连接
    :param couponActivityId: 要删红包则传入红包活动id
    :param benefitActivityId: 优惠券活动id
    :param benefitId: 要删优惠券则传入优惠券id
    :param tmlCompanyId:领取操作的终端店
    :return:
    '''
    # keys = r.keys("dealerBenefitProcess*")
    # print keys
    # print r.get('couponQueue:'+str(activityId))
    # print  r.get('Counter:'+str(activityId))
    r.delete('Counter:'+str(couponActivityId))
    if couponActivityId!=None:
        r.delete('Counter:' + str(couponActivityId))
        r.delete('dealerCouponsTicket:' + str(couponActivityId) +':'+ tmlCompanyId)
    if benefitActivityId==None and benefitId!=None:
        r.delete('dealerBenefitProcess:' + str(benefitId) + ':' + tmlCompanyId)
    if benefitActivityId!=None and benefitId!=None:
        r.delete('Counter:' + str(benefitActivityId))
        r.delete('dealerBenefitProcess:' + str(benefitId) + ':' + tmlCompanyId)

    # r.delete('Counter:10102135707015')
    # r.delete('dealerCouponsTicket:10102135707015:6fb850120da449ef98a2c7e641100e02')
    # print keys
    # print  r.get('Counter:' + str(activityId))


def delGoodCache(goodsID=None, BuyCompanyID=None, r=connectionToRedis()):
    allkeys = r.keys()
    for key in allkeys:
        if goodsID in key and BuyCompanyID in  key and 'storageGroupNameForGoodsListByBuyer:@0:' in key:
            r.delete(key)

if __name__ == '__main__':
    # deleteKey(connectionToRedis(),1011656055820)
    # r.set('foo', 'bar')
    # r.get('foo')
    # pool = redis.ConnectionPool(host=server_ip, port=server_port, db=0)
    # r = redis.StrictRedis(connection_pool=pool)
    # allkeys = r.keys()
    # for key in allkeys:
    #     if '109ac50b14a7404a886d8d9912f6eae7' in key and '6fb850120da449ef98a2c7e641100e02' in  key and 'storageGroupNameForGoodsListByBuyer:@0:' in key:
    #         print key
    #         r.delete(key)
    #         print key
    # pass

    # merchkeys =
    # print keys
    # # r.delete('storageGroupNameForGoodsListByBuyer:*')
    # r.delete(*keys)
    # print r.keys()
    # r=connectionToRedis()
    # keys = r.keys("dealerBenefitProcess*")
    #
    # print keys
    #删优惠券缓存示例
    deleteActivityKey(benefitActivityId=1112173326601, benefitId=3363326621,
                      tmlCompanyId='b12bb1f4942b48dc85ec605bb0557c1a')
    #删红包缓存示例
    deleteActivityKey(couponActivityId=1112173326601,
                      tmlCompanyId='b12bb1f4942b48dc85ec605bb0557c1a')



