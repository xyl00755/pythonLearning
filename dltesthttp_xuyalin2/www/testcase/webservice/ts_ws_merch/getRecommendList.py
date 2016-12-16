#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0040.获取丹露推荐商品列表
http://127.0.0.1:8280/mallws/merch/getRecommendList.json
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
        "recommendListModel": [
            {
                "merchId": "67d4cb03595348cdacd61000bc96ba03",                  // 商品id
                "merchName": "测试商品 - 1",                                    // 商品名
                "sellerId": "4564564564560",                                    // 卖家id
                "sellerName": "卖家 - 1",                                       // 卖家名
                "danluPrice": "0",												// 丹露价格
				"isRecommended":"是否推荐",										// 是否推荐 0-推荐 1-非推荐 默认且固定为0
				"isPromoted":"是否促销"											// 是否促销 0-促销 1-非促销 默认1
				"goodsPromotionInfo":"促销信息"									// 促销信息(UI中显示“火热促销中”样例)

				"merchStatus":"0",												// 是否有货 0-有货 1-暂时缺货
				"minSaleNumber":"3",											// 最小起售数量
				"promotionList":[												// 促销详细信息
					"12345"
				],
				"merchSpec":"箱",												// 商品规格 /件/箱
                "picUrl": "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"   // 图片URL
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.RecommendListResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import webservice
from www.common.database import update
from www.common.excel import wsData


class getRecommendList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    # S1.获取推荐列表
    def test_getRecdMerchList_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchList = ws.getRecommendList(rows="999")
        # 商品1存在
        self.assertGetMerchList(merchList, self.Merch1)
        # 商品2不在列表
        for i in range(0, len(merchList.model['recommendListModel'])):
            if merchList.model['recommendListModel'][i] == self.Merch2.goodsId:
                self.assertEqual(False,True,self.Merch2.fullName + 'is found in recommendList')

    # S2.促销列表分页
    def test_getRecdMerchList_page(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getRecommendList(rows='999')
        numMerch = len(allMerchList.model['recommendListModel'])
        page = numMerch/4

        time = 0
        for p in range(1,page+2):
            MerchListPage = ws.getRecommendList(page=p)
            # 判断商品1是否存在，如果存在time +1
            for i in range(0,len(MerchListPage.model['recommendListModel'])):
                if MerchListPage.model['recommendListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                    time+=1
            if p == page+1:
                self.assertEqual(len(MerchListPage.model['recommendListModel']),numMerch%4,"The last page is wrong")
            else:
                self.assertEqual(len(MerchListPage.model['recommendListModel']),4,"Every page is wrong")

        self.assertEqual(time,1,self.Merch1.fullName+" is not once.")

    # S3.没有促销商品时获取促销列表
    def test_getRecdMerchList_null(self):
        # 修改终端店2的采购区域为香港CHNP032C342D2995
        update('update dlcompany.dl_biz_purchase set purchase_area_code = ? where company_id = ?', 'CHNP032C342D2995', self.UserShop2.companyId)

        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        MerchList = ws.getRecommendList(rows='999')
        self.assertEqual(MerchList.model['recommendListModel'],[])


    def tearDown(self):
        # 还原终端店2的采购区域
        update('update dlcompany.dl_biz_purchase set purchase_area_code = ? where company_id = ?', self.UserShop2.areaCode, self.UserShop2.companyId)

    def assertGetMerchList(self, rsp, merch, code = 200, success = '0',isPromotion='0',isRecommended='0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        if rsp.model['totalRecord'] == '0':
            self.assertEqual(True, False, merch.fullName +"is not found")
        else:
            self.assertEqual(rsp.model['totalRecord'], str(len(rsp.model['recommendListModel'])))
        # 用于判断商品是否存在
        flag = False
        for i in range(0, len(rsp.model['recommendListModel'])):
            if rsp.model['recommendListModel'][i]['merchId'] == merch.goodsId:
                flag = True
                self.assertEqual(rsp.model['recommendListModel'][i]['merchName'],  merch.fullName)
                self.assertEqual(rsp.model['recommendListModel'][i]['sellerId'],  merch.seller_store_id)
                self.assertEqual(rsp.model['recommendListModel'][i]['sellerName'],  merch.sellerName)
                self.assertEqual(rsp.model['recommendListModel'][i]['danluPrice'],  merch.priceDanlu)
                self.assertEqual(rsp.model['recommendListModel'][i]['goodsPromotionInfo'],  merch.propagandaInfo)
                self.assertEqual(rsp.model['recommendListModel'][i]['merchStatus'],  merch.merchStatus)
                self.assertEqual(rsp.model['recommendListModel'][i]['isPromotion'],  merch.isPromotion)
                self.assertEqual(rsp.model['recommendListModel'][i]['isRecommended'],  merch.isRecommended)
                self.assertEqual(rsp.model['recommendListModel'][i]['minSaleNumber'],  merch.saleQuantityS1)
                for j in range(0, len(rsp.model['recommendListModel'][i]['promotionList'])):
                    flag = False
                    for k in range(1, len(rsp.model['recommendListModel'][i]['promotionList'])+1):
                        if rsp.model['recommendListModel'][i]['promotionList'][j] == merch['promotionList'+str(k)].decode('utf-8'):
                            flag = True
                            break
                        if k == 6:
                            self.assertEqual(flag, True, rsp.model['recommendListModel'][i]['promotionList'][j] + "is not found!")
                self.assertEqual(rsp.model['recommendListModel'][i]['merchSpec'],  merch.merchSpec)
                self.assertEqual(rsp.model['recommendListModel'][i]['picUrl'],  merch.picUrl)
        self.assertEqual(flag, True, merch.fullName +"is not found")




def suite():
    suite = unittest.TestSuite()
    suite.addTest(getRecommendList("test_getRecdMerchList_all"))
    suite.addTest(getRecommendList("test_getRecdMerchList_page"))
    suite.addTest(getRecommendList("test_getRecdMerchList_null"))
    return suite
