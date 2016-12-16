#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from www.api.dlpromotionx import *
from www.common.excel import *
from www.common.database import *
from www.operation.redisCache import *
from www.testcase.dlpromotionx.tool.createDealerActivityTool import *


"""
post
http://dlpromotionx.com/dealer/share_dealer_trading
{
  "userPhone": "13551148213",
  "activityId": "0210836632302",

}
{
  "status": 0,
  "msg": "券已领取成功，可在'我的优惠券'中进行查看",
  "data": {
    "activityId": "0210836632302",
    "dealerCouponId": "2023642603",
    "couponAmt": "20",
    "dealer_name":"湖北人人大",
    "dealer_id":"0000d96033cd441c8a9fdee3f99a20dd",
    "effectiveTime":"2016-08-31",
    "uneffectiveTime": "2017-08-31",
    "dealer_coupon_type":"01",
    "platform_limit":"web",
    "effectiveAmt":"200",
    "dealer_name":"适用店铺名称",
    "available_channel":"烟酒专卖店",
    "dealer_coupon_img_url":"http://user.qzone.qq.com/1608514296?ptlang=2052",
    "goodsId":"使用商品限制",
    "goods_name":"【烟酒专卖店】白云边1979 45度 "
  }
}
"""

class shareDealerTrading(unittest.TestCase):
    newBenefitActivityInfo = eData('AvailableCouponsBenfits')
    dealerInfo = wsData('DealMager')
    goodsInfo=wsData('Merch1')
    dlservice = dlpromotionx()
    actID=newBenefitActivityInfo.benefitActivityId

    #领取优惠券
    def receiveBenefit(self,userPhone,activityId):
        queryResult = self.dlservice.shareDealerTrading(userPhone=userPhone, activityId=activityId)
        return queryResult

    #将入参指定的优惠券置于已使用状态
    def useBenefit(self,benefitActivityId,dealer_coupon_id,tmlCompanyId):
        #   dealer_coupon_entity_status varchar(2) comment '经销商红包、优惠卷实体状态 01–未使用;02-已使用;03-锁定;04-已过期',
        update('update dlpromotionx.dl_dealer_coupon_snapshot set dealer_coupon_entity_status=? where dealer_coupon_id=?', '02', dealer_coupon_id)
        deleteActivityKey(benefitActivityId=benefitActivityId, benefitId=dealer_coupon_id, tmlCompanyId=tmlCompanyId)

    #造前提数据
    def setUp(self):
        self.tearDown()

    #0.链接领券成功
    def test_shareDealerTrading_success(self):
        queryResult=self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        self.assertEqual(queryResult['status'], 0)
        # print queryResult
        # self.assertEqual(queryResult['msg'],'券已领取成功，可在\'我的优惠券\'中进行查看'.decode('utf-8').encode('utf-8')  )  #提示信息由前端自己造
        self.assertEqual(queryResult['data']['activityId'],self.actID)
        # benefitInfo=select_one('select * from dlcoupon.dl_dealer_coupon where dealer_coupon_name=?', self.newBenefitActivityInfo.dealerBenefitName)
        self.assertEqual(queryResult['data']['dealerCouponDto']['dealerCouponId'], self.newBenefitActivityInfo.dealerBenefitId)
        self.assertEqual(queryResult['data']['couponMinAmt'],99900)
        self.assertEqual(queryResult['data']['dealerCouponDto']['dealerName'].encode("utf-8"), self.dealerInfo.fullName)
        self.assertEqual(queryResult['data']['dealerCouponDto']['dealerId'], self.dealerInfo.companyId)
        self.assertEqual(queryResult['data']['activityType'], '11')
        self.assertEqual(queryResult['data']['dealerCouponDto']['platformLimit'],'')
        self.assertEqual(queryResult['data']['dealerCouponDto']['availableChannel'], self.newBenefitActivityInfo.availableChannel)
        self.assertEqual(queryResult['data']['dealerCouponDto']['dealerCouponImgUrl'], '')
        self.assertEqual(queryResult['data']['dealerCouponDto']['goodsId'], self.goodsInfo.goodsId)
        self.assertEqual(queryResult['data']['dealerCouponDto']['goodsName'].encode('utf-8'), (self.goodsInfo.productName+' '+self.goodsInfo.goodsName))

    #1:优惠券已过期，直接提示该链接已失效
    def test_shareDealerTrading_outOfDate(self):
        #准备已过期的activityId
        queryResult = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.newBenefitActivityInfo.benefitOutOfDateActivityId)
        self.assertEqual(queryResult['status'], 1)
        # print queryResult['msg']
        # self.assertEqual(queryResult['msg'], u'优惠券已过期，直接提示该链接已失效!')

    #链接领券手机号未注册
    def test_shareDealerTrading_phoneUnregister(self):
        queryResult = self.receiveBenefit(userPhone='18228693564', activityId=self.actID)
        # print queryResult
        self.assertEqual(queryResult['status'], 2)
        self.assertEqual(queryResult['msg'], u'对不起，您还不是丹露终端店注册用户，请先注册！')

    #链接领券时手机号对应经销商
    def test_shareDealerTrading_phoneOfDealer(self):
        queryResult = self.receiveBenefit(userPhone=self.dealerInfo.mobileNumber, activityId=self.actID)
        self.assertEqual(queryResult['status'], 3)
        # self.assertEqual(queryResult['msg'], u'对不起，该优惠券仅限终端店用领取，请您关注丹露其它促销活动！')

    #所在的区域不在本次发放区域内
    def test_shareDealerTrading_outOfArea(self):
        # 查询在售卖权范围（赤尾屿、乐山呼叫岛）内、不在发放区域（赤尾屿、黄岩岛）内的手机号(乐山呼叫岛 -烟酒专卖）
        phoneOutOfArea=select_one(r'SELECT user_phone FROM dluser.dl_user WHERE user_type=02 and user_status =01 and user_id in '
                                       r'(SELECT user_id FROM dlcompany.dl_company_ref_user WHERE company_id in (SELECT company_id from dlcompany.dl_biz_base_info WHERE reg_area_code=? and terminal_type=?))','CHNP035C345D2999','S011')
        queryResult = self.receiveBenefit(userPhone=str(phoneOutOfArea['user_phone']), activityId=self.actID) #需要在基础数据xls中添加此行
        self.assertEqual(queryResult['status'], 4)
        self.assertEqual(queryResult['msg'], u'对不起，由于你所在的区域不在本次发放区域内，您无法领取该优惠券！')

    #由于售卖权不匹配，您无法领取该优惠券
    def test_shareDealerTrading_outOfSaleRight(self):
        #查询在发放区域（赤尾屿、黄岩岛）内、不在售卖权范围（赤尾屿、乐山呼叫岛）内的手机号
        phoneOutOfSaleRight=select_one(r'SELECT user_phone FROM dluser.dl_user WHERE user_type=02 and user_status =01 and user_id in '
                                       r'(SELECT user_id FROM dlcompany.dl_company_ref_user WHERE company_id in (SELECT company_id from dlcompany.dl_biz_base_info WHERE reg_area_code=? and terminal_type=?))','CHNP035C345D3001','S011')
        # print str(phoneOutOfSaleRight['user_phone'])
        queryResult = self.receiveBenefit(str(phoneOutOfSaleRight['user_phone']), activityId=self.actID) #需要在基础数据xls中添加此行
        self.assertEqual(queryResult['status'], 5)
        # print queryResult['msg']
        # self.assertEqual(queryResult['msg'], u'对不起，由于售卖权不匹配，您无法领取该优惠券！')

    #6:账号还在审批中，提示“您的账号还在审批中，请审批通过后再进行领取”
    def test_shareDealerTrading_accountNotApproved(self):
        #查询未通过审批的终端店手机号
        phoneNotApproved=select_one(r'SELECT terminal_tel FROM dlworkflow.dl_apply_terminal WHERE flow_status in (02,03,05) AND is_deleted=?',0)
        queryResult = self.receiveBenefit(userPhone=str(phoneNotApproved['terminal_tel']), activityId=self.actID)
        self.assertEqual(queryResult['status'], 6)
        # self.assertEqual(queryResult['msg'],u'您的账号还在审批中，请审批通过后再进行领取')

    #8：您已领取该券，请使用后再进行领取  -bug
    def test_shareDealerTrading_receiveNotUsed(self):
        queryResult1=self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        queryResult2 = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        self.assertEqual(queryResult1['status'], 0)
        self.assertEqual(queryResult2['status'], 8)
        # self.assertEqual(queryResult2['msg'], u'您已领取该券，请使用后再进行领取！')

    #7：对不起，该券一人只能领三次，您已领取三次，无法再次领取
    def test_shareDealerTrading_overLimitNum(self):
        queryResult1 = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        self.assertEqual(queryResult1['status'], 0)
        time.sleep(30)
        self.useBenefit(benefitActivityId= self.actID ,dealer_coupon_id=self.newBenefitActivityInfo.dealerBenefitId,tmlCompanyId=self.newBenefitActivityInfo.tmlCompanyId)

        queryResult2 = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        self.assertEqual(queryResult2['status'], 0)
        time.sleep(30)
        self.useBenefit(benefitActivityId= self.actID ,dealer_coupon_id=self.newBenefitActivityInfo.dealerBenefitId,tmlCompanyId=self.newBenefitActivityInfo.tmlCompanyId)
        time.sleep(60)

        queryResult3 = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        self.assertEqual(queryResult3['status'], 0)
        time.sleep(30)
        self.useBenefit(benefitActivityId= self.actID ,dealer_coupon_id=self.newBenefitActivityInfo.dealerBenefitId,tmlCompanyId=self.newBenefitActivityInfo.tmlCompanyId)
        time.sleep(30)

        queryResult4 = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.actID)
        self.assertEqual(queryResult4['status'], 7)
        time.sleep(30)


    #9：对不起，您来晚了，券已被领完，下次加油！--券库存为0,手机号未领取过该券
    def test_shareDealerTrading_benefitOutOfStock(self):
        queryResult = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.newBenefitActivityInfo.benefitOutOfStock)
        self.assertEqual(queryResult['status'], 9)
        # print queryResult['msg']
        #self.assertEqual(queryResult['msg'], '对不起，您来晚了，券已被领完，下次加油！')

    # 9：对不起，您来晚了，券已被领完，下次加油！--券库存为0,手机号领取过该券(到上限）
    def test_shareDealerTrading_benefitOutOfStock2(self):
        userPhone = self.newBenefitActivityInfo.outOfChannel
        queryResult = self.receiveBenefit(userPhone, activityId=self.newBenefitActivityInfo.benefitOutOfStock)
        self.assertEqual(queryResult['status'], 8)
        # print queryResult
        #self.assertEqual(queryResult['msg'], '对不起，您来晚了，券已被领完，下次加油！')

    #9：对不起，您来晚了，券已被领完，下次加油！--活动状态置为已结束
    def test_shareDealerTrading_activityEnd(self):
        queryResult = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.userPhone, activityId=self.newBenefitActivityInfo.actIDactivityEnd)
        self.assertEqual(queryResult['status'], 1)
        # print queryResult['msg']

    #10：渠道不匹配
    def test_shareDealerTrading_outOfChannel(self):
        queryResult = self.receiveBenefit(userPhone=self.newBenefitActivityInfo.outOfChannel, activityId=self.actID)
        self.assertEqual(queryResult['status'], 10)
        # print queryResult['msg']

    #快速添加case到suite中
    def test_functions(self):
        for i in range(0,len(dir(self))):
            if dir(self)[i][0:5]=='test_':
                print 'suite.addTest('+str(self.__class__.__name__)+'(\"'+dir(self)[i]+'\"))'

    #用例执行完成后的操作
    def tearDown(self):
        time.sleep(5)
        couponId = select_one('SELECT dealer_coupon_id from dlcoupon.dl_dealer_coupon '
                              'where dealer_coupon_name = (SELECT activity_name from dlpromotionx.dl_dealer_coupon_activity where activity_id =?)',
                              self.actID)
        # print couponId
        if self.actID != None:
            update('delete from dlpromotionx.dl_dealer_coupon_snapshot where dealer_coupon_id = ?',
                   couponId['dealer_coupon_id'])  # 领取实体快照
            update('delete from dlpromotionx.dl_dealer_coupon_issue_record where dealer_coupon_id = ?',
                   couponId['dealer_coupon_id'])  # 领取记录
            # 恢复库存
            update('update dlcoupon.dl_coupon_detail set package_grant_amt=?, package_grant_amount=? where coupon_id=?',
                   0, 0, couponId['dealer_coupon_id'])
        # deleteActivityKey(activityId=self.actID)
        deleteActivityKey(benefitActivityId=self.actID, benefitId=self.newBenefitActivityInfo.dealerBenefitId,
                              tmlCompanyId=self.newBenefitActivityInfo.tmlCompanyId)  # 删除redis中的缓存

def suite():
    suite=unittest.TestSuite()
    suite.addTest(shareDealerTrading("test_shareDealerTrading_accountNotApproved"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_activityEnd"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_benefitOutOfStock"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_benefitOutOfStock2"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_outOfArea"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_outOfDate"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_outOfSaleRight"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_overLimitNum"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_phoneOfDealer"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_phoneUnregister"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_receiveNotUsed"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_success"))
    suite.addTest(shareDealerTrading("test_shareDealerTrading_outOfChannel"))

    return suite

