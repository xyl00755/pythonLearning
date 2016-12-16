#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *

class createDealerActivityTool:

    ReceiveCouponInfo = eData('ReceiveCoupon')
    ReceiveBenefitInfo = eData('ReceiveBenefit')
    PushCouponInfo = eData('PushCoupon')
    PushBenefitInfo = eData('PushBenefit')
    dlservice = dlpromotionx()

    #创建红包领取活动
    def createReceiveCouponActivity(self,dealerCouponName = ReceiveCouponInfo.dealerCouponName,dealerCouponType = ReceiveCouponInfo.dealerCouponType,dealerName = ReceiveCouponInfo.dealerName,dealerId = ReceiveCouponInfo.dealerId,
                                    totalNum = ReceiveCouponInfo.totalNum,totalAmount = ReceiveCouponInfo.totalAmount,effectiveTime = ReceiveCouponInfo.effectiveTime,uneffectiveTime=ReceiveCouponInfo.uneffectiveTime,availableChannel = ReceiveCouponInfo.availableChannel,
                                    areaLimit = ReceiveCouponInfo.areaLimit,platformLimit = ReceiveCouponInfo.platformLimit,createPersonName_coupon = ReceiveCouponInfo.createPersonName_coupon,createPerson_coupon = ReceiveCouponInfo.createPerson_coupon,
                                    couponMinAmt = ReceiveCouponInfo.couponMinAmt,effectiveAmt = ReceiveCouponInfo.effectiveAmt,couponPriority = ReceiveCouponInfo.couponPriority,packageAmount = ReceiveCouponInfo.packageAmount,
                                    activityType = ReceiveCouponInfo.activityType,issueWay = ReceiveCouponInfo.issueWay,autoEnable = ReceiveCouponInfo.autoEnable,autoDisable = ReceiveCouponInfo.autoDisable,approvalAutoEnable=ReceiveCouponInfo.approvalAutoEnable,
                                    releaseCompletionDisable = ReceiveCouponInfo.releaseCompletionDisable,limitNum= ReceiveCouponInfo.limitNum,showWay = ReceiveCouponInfo.showWay,getWay = ReceiveCouponInfo.getWay,createPersonName = ReceiveCouponInfo.createPersonName,
                                    createPerson =ReceiveCouponInfo.createPerson,notice = ReceiveCouponInfo.notice):
        createReceiveCouponResult=self.dlservice.createDealerActivity(dealerCouponName=dealerCouponName,dealerCouponType=dealerCouponType,dealerName=dealerName,dealerId=dealerId,totalNum=totalNum,totalAmount=totalAmount,effectiveTime=effectiveTime,
                                    uneffectiveTime=uneffectiveTime,availableChannel=availableChannel,areaLimit=areaLimit,platformLimit=platformLimit,createPersonName_coupon=createPersonName_coupon,createPerson_coupon=createPerson_coupon,couponMinAmt=couponMinAmt,
                                    effectiveAmt=effectiveAmt,couponPriority=couponPriority,packageAmount=packageAmount,activityType=activityType,issueWay=issueWay,autoEnable=autoEnable,autoDisable=autoDisable,approvalAutoEnable=approvalAutoEnable,
                                    releaseCompletionDisable=releaseCompletionDisable,limitNum=limitNum,showWay=showWay,getWay=getWay ,createPersonName=createPersonName,createPerson=createPerson,notice=notice)
        return createReceiveCouponResult

    #创建优惠券领取活动
    def createReceiveBenifitActivity(self,dealerCouponName = ReceiveBenefitInfo.dealerCouponName,dealerCouponType = ReceiveBenefitInfo.dealerCouponType,dealerName = ReceiveBenefitInfo.dealerName,dealerId = ReceiveBenefitInfo.dealerId,
                                    totalNum = ReceiveBenefitInfo.totalNum,totalAmount = ReceiveBenefitInfo.totalAmount,effectiveTime = ReceiveBenefitInfo.effectiveTime,uneffectiveTime=ReceiveBenefitInfo.uneffectiveTime,availableChannel = ReceiveBenefitInfo.availableChannel,
                                    goodsId=ReceiveBenefitInfo.goodsId,goodsName=ReceiveBenefitInfo.goodsName,areaLimit = ReceiveBenefitInfo.areaLimit,dealerCouponImgUrl=ReceiveBenefitInfo.dealerCouponImgUrl,platformLimit = ReceiveBenefitInfo.platformLimit,
                                    createPersonName_coupon = ReceiveBenefitInfo.createPersonName_coupon,createPerson_coupon = ReceiveBenefitInfo.createPerson_coupon,couponMinAmt = ReceiveBenefitInfo.couponMinAmt,effectiveAmt = ReceiveBenefitInfo.effectiveAmt,
                                    couponPriority = ReceiveBenefitInfo.couponPriority,packageAmount = ReceiveBenefitInfo.packageAmount,activityType = ReceiveBenefitInfo.activityType,issueWay = ReceiveBenefitInfo.issueWay,
                                    autoEnable =ReceiveBenefitInfo.autoEnable,autoDisable = ReceiveBenefitInfo.autoDisable,approvalAutoEnable=ReceiveBenefitInfo.approvalAutoEnable,releaseCompletionDisable = ReceiveBenefitInfo.releaseCompletionDisable,limitNum= ReceiveBenefitInfo.limitNum,
                                    showWay = ReceiveBenefitInfo.showWay,getWay = ReceiveBenefitInfo.getWay,createPersonName = ReceiveBenefitInfo.createPersonName,createPerson = ReceiveBenefitInfo.createPerson,notice = ReceiveBenefitInfo.notice):
         createReceiveBenifitResult=self.dlservice.createDealerActivity(dealerCouponName=dealerCouponName,dealerCouponType=dealerCouponType,dealerName=dealerName,dealerId=dealerId,totalNum=totalNum,totalAmount=totalAmount,effectiveTime=effectiveTime,
                                    uneffectiveTime=uneffectiveTime,availableChannel=availableChannel,goodsId=goodsId,goodsName=goodsName,areaLimit=areaLimit,dealerCouponImgUrl=dealerCouponImgUrl,platformLimit=platformLimit,createPersonName_coupon=createPersonName_coupon,
                                    createPerson_coupon=createPerson_coupon,couponMinAmt=couponMinAmt,effectiveAmt=effectiveAmt,couponPriority=couponPriority,packageAmount=packageAmount,activityType=activityType,issueWay=issueWay,
                                    autoEnable=autoEnable,autoDisable=autoDisable,approvalAutoEnable=approvalAutoEnable,releaseCompletionDisable=releaseCompletionDisable,limitNum=limitNum,showWay=showWay,getWay=getWay ,createPersonName=createPersonName,createPerson=createPerson,notice=notice)
         return createReceiveBenifitResult

    #创建红包推送活动的方法
    def createPushCouponActivity(self,activityName=PushCouponInfo.activityName,activityType=PushCouponInfo.activityType,createPersonName=PushCouponInfo.createPersonName,
                                                                       createPerson=PushCouponInfo.createPerson,notice=PushCouponInfo.notice,dealerId=PushCouponInfo.dealerId,pushList1=PushCouponInfo.pushList1,pushList2=PushCouponInfo.pushList2,
                                                                       couponId=PushCouponInfo.couponId,couponTypeId=PushCouponInfo.couponTypeId,prizePlaces=PushCouponInfo.prizePlaces):
        createPushCouponResult=self.dlservice.createDealerPushActivity(activityName,activityType,createPersonName,createPerson,notice,dealerId,pushList1,pushList2,couponId,couponTypeId,prizePlaces)
        return createPushCouponResult

    #创建优惠券活动的方法
    def createPushBenefitActivity(self,activityName=PushBenefitInfo.activityName,activityType=PushBenefitInfo.activityType,createPersonName=PushBenefitInfo.createPersonName,
                                                                       createPerson=PushBenefitInfo.createPerson,notice=PushBenefitInfo.notice,dealerId=PushCouponInfo.dealerId,pushList1=PushBenefitInfo.pushList1,pushList2=PushBenefitInfo.pushList2,
                                                                       couponId=PushBenefitInfo.couponId,couponTypeId=PushBenefitInfo.couponTypeId,prizePlaces=PushBenefitInfo.prizePlaces):
        createPushBenefitResult=self.dlservice.createDealerPushActivity(activityName,activityType,createPersonName,createPerson,notice,dealerId,pushList1,pushList2,couponId,couponTypeId,prizePlaces)
        return createPushBenefitResult

    #通过sql语句删除红包或者优惠券领取活动涉及的数据
    def deleteReceiveActivityBySQL(self,dealerCouponName=ReceiveCouponInfo.dealerCouponName,activityType=ReceiveCouponInfo.activityType,dealerCouponType=ReceiveCouponInfo.dealerCouponType,
                                   dealerCouponName2=ReceiveBenefitInfo.dealerCouponName,activityType2=ReceiveBenefitInfo.activityType,dealerCouponType2=ReceiveBenefitInfo.dealerCouponType):
        couponActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', dealerCouponName,activityType)
        coupondealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?',dealerCouponName,dealerCouponType)
        benefitActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', dealerCouponName2,activityType2)
        benefitdealerCouponId = select_one('select dealer_coupon_id from dlcoupon.dl_dealer_coupon where dealer_coupon_name = ? and dealer_coupon_type = ?', dealerCouponName2,dealerCouponType2)
        if couponActivityId != None:
            update('delete from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?',couponActivityId['activity_id'])
            update('delete from dlpromotionx.dl_promotionx_activity_detail where activity_id = ?',couponActivityId['activity_id'])
        if coupondealerCouponId != None:
            update('delete from dlcoupon.dl_dealer_coupon where dealer_coupon_id = ?', coupondealerCouponId['dealer_coupon_id'])
            update('delete from dlcoupon.dl_coupon_detail where coupon_id = ?', coupondealerCouponId['dealer_coupon_id'])
        if benefitActivityId != None:
            update('delete from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?',benefitActivityId['activity_id'])
            update('delete from dlpromotionx.dl_promotionx_activity_detail where activity_id = ?',benefitActivityId['activity_id'])
        if benefitdealerCouponId != None:
            update('delete from dlcoupon.dl_dealer_coupon where dealer_coupon_id = ?', benefitdealerCouponId['dealer_coupon_id'])
            update('delete from dlcoupon.dl_coupon_detail where coupon_id = ?', benefitdealerCouponId['dealer_coupon_id'])


    def deletePushActivityBySQL(self,activityName=PushCouponInfo.activityName,activityType=PushCouponInfo.activityType,activityName2=PushBenefitInfo.activityName,activityType2=PushBenefitInfo.activityType):
        couponActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?', activityName,activityType)
        benefitActivityId = select_one('select activity_id from dlpromotionx.dl_dealer_coupon_activity where activity_name = ? and activity_type = ?',activityName2,activityType2)
        if couponActivityId != None:
            update('delete from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?',couponActivityId['activity_id'])
            update('delete from dlpromotionx.dl_dealer_push_name_list where activity_id = ?',couponActivityId['activity_id'])
            update('delete from dlpromotionx.dl_promotionx_activity_detail where activity_id = ?',couponActivityId['activity_id'])
            dealerCouponEntityId = select('select dealer_coupon_entity_id from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id = ?',couponActivityId['activity_id'])
            for item in dealerCouponEntityId:
                update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id = ?',item['dealer_coupon_entity_id'])
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id = ?',couponActivityId['activity_id'])
        if benefitActivityId != None:
            update('delete from dlpromotionx.dl_dealer_coupon_activity where activity_id = ?',benefitActivityId['activity_id'])
            update('delete from dlpromotionx.dl_dealer_push_name_list where activity_id = ?',benefitActivityId['activity_id'])
            update('delete from dlpromotionx.dl_promotionx_activity_detail where activity_id = ?',benefitActivityId['activity_id'])
            dealerBenefitEntityId = select('select dealer_coupon_entity_id from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id = ?',benefitActivityId['activity_id'])
            for item in dealerBenefitEntityId:
                update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_entity_id = ?',item['dealer_coupon_entity_id'])
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_activity_id = ?',benefitActivityId['activity_id'])