#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0039.获取丹露促销商品列表
http://127.0.0.1:8280/mallws/merch/getPromotionList.json
{
    "token":"123"						// 必须
	"page":1,                           // 必须
    "rows":6                            // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                         // 成功 0-成功
		"totalRecord":"20",														// 列表总记录数
        "promotionListModel": [
            {
				"merchId": "67d4cb03595348cdacd61000bc96ba03",                  // 商品id
				"merchName": "null测试商品 - 1",                                // 商品名
				"sellerId": "4564564564560",                                    // 卖家id
                "sellerName": "卖家 - 1",                                       // 卖家名
				"merchStatus":"0",												// 是否有货 0-有货 1-暂时缺货
				"danluPrice": "1000",											// 丹露价格
                "isPromotion":"0",												// 是否促销 0-促销 1-不是促销
				"goodsPromotionInfo":"促销信息"	,								// 促销信息(UI中显示“火热促销中”样例)
				"isRecommended":"是否推荐",										// 是否推荐 0-推荐 1-不是推荐

				"minSaleNumber":"3",											// 最小起售数量
				"promotionList":[												// 促销详细信息
					"12345"
				],
				"merchSpec":"箱",												// 商品规格 /件/箱
                "picUrl": "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"  // 图片URL
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.PromotionListResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
参数说明：
	isPromotion 由IsFullReduction和IsFullPrensentation决定，满减与满赠进行或运算，真对应促销，假对应不是促销
"""

import unittest

from www.api.webservice import webservice
from www.common.database import update
from www.common.excel import wsData


class getPromotionList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch4 = wsData('Merch4')

    # S1.获取促销列表
    def test_getMerchList_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchList = ws.getPromotionList(rows="999")
        # 商品1存在
        self.assertGetMerchList(merchList, self.Merch1)
        # 商品4不在列表
        for i in range(0, len(merchList.model['promotionListModel'])):
            if merchList.model['promotionListModel'][i] == self.Merch4.goodsId:
                self.assertEqual(False,True,self.fullName + 'is found in PromotionList')

    # S2.促销列表分页
    def test_getMerchList_page(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getPromotionList(rows='999')
        numMerch = len(allMerchList.model['promotionListModel'])
        page = numMerch/4

        time = 0
        for p in range(1,page+2):
            MerchListPage = ws.getPromotionList(page=p)
            # 判断商品1是否存在，如果存在time +1
            for i in range(0,len(MerchListPage.model['promotionListModel'])):
                if MerchListPage.model['promotionListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                    time+=1
            if p == page+1:
                self.assertEqual(len(MerchListPage.model['promotionListModel']),numMerch%4,"The last page is wrong")
            else:
                self.assertEqual(len(MerchListPage.model['promotionListModel']),4,"Every page is wrong")

        self.assertEqual(time,1,self.Merch1.fullName+" is not once.")

    # S3.没有促销商品时获取促销列表
    def test_getMerchList_null(self):
        # 修改终端店2的采购区域为香港CHNP032C342D2995
        update('update dlcompany.dl_biz_purchase set purchase_area_code = ? where company_id = ?', 'CHNP032C342D2995', self.UserShop2.companyId)

        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        MerchList = ws.getPromotionList(rows='999')
        self.assertEqual(MerchList.model['promotionListModel'],[])


    def tearDown(self):
        # 还原终端店2的采购区域
        update('update dlcompany.dl_biz_purchase set purchase_area_code = ? where company_id = ?', self.UserShop2.areaCode, self.UserShop2.companyId)

    def assertGetMerchList(self, rsp, merch, code = 200, success = '0',isPromotion='0',isRecommended='0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        if rsp.model['totalRecord'] == '0':
            self.assertEqual(True, False, merch.fullName +"is not found")
        else:
            self.assertEqual(rsp.model['totalRecord'], str(len(rsp.model['promotionListModel'])))
        # 用于判断商品是否存在
        flag = False
        for i in range(0, len(rsp.model['promotionListModel'])):
            if rsp.model['promotionListModel'][i]['merchId'] == merch.goodsId:
                flag = True
                self.assertEqual(rsp.model['promotionListModel'][i]['merchName'],  merch.fullName)
                self.assertEqual(rsp.model['promotionListModel'][i]['sellerId'],  merch.seller_store_id)
                self.assertEqual(rsp.model['promotionListModel'][i]['sellerName'],  merch.sellerName)
                self.assertEqual(rsp.model['promotionListModel'][i]['danluPrice'],  merch.priceDanlu)
                self.assertEqual(rsp.model['promotionListModel'][i]['goodsPromotionInfo'],  merch.propagandaInfo)
                self.assertEqual(rsp.model['promotionListModel'][i]['merchStatus'],  merch.merchStatus)
                self.assertEqual(rsp.model['promotionListModel'][i]['isPromotion'],  merch.isPromotion)
                self.assertEqual(rsp.model['promotionListModel'][i]['isRecommended'],  merch.isRecommended)
                self.assertEqual(rsp.model['promotionListModel'][i]['minSaleNumber'],  merch.saleQuantityS1)
                for j in range(0, len(rsp.model['promotionListModel'][i]['promotionList'])):
                    flag2 = False
                    for k in range(1, len(rsp.model['promotionListModel'][i]['promotionList'])+1):
                        if rsp.model['promotionListModel'][i]['promotionList'][j] == merch['promotionList'+str(k)].decode('utf-8'):
                            flag2 = True
                            break
                        if k == 6:
                            self.assertEqual(flag2, True, rsp.model['promotionListModel'][i]['promotionList'][j] + "is not found!")
                self.assertEqual(rsp.model['promotionListModel'][i]['merchSpec'],  merch.merchSpec)
                self.assertEqual(rsp.model['promotionListModel'][i]['picUrl'],  merch.picUrl)
        self.assertEqual(flag, True, merch.fullName +"is not found")




def suite():
    suite = unittest.TestSuite()
    suite.addTest(getPromotionList("test_getMerchList_all"))
    suite.addTest(getPromotionList("test_getMerchList_page"))
    suite.addTest(getPromotionList("test_getMerchList_null"))
    return suite
