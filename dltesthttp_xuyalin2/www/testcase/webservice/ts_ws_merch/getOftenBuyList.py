#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0041.获取我的常购商品列表
http://127.0.0.1:8280/mallws/merch/getOftenBuyList.json
{
    "token":"123",						   // 必须
	"saleFlag":"0",                        // 必须 上架下架标识：0-上架 1-下架
	"page":1,                              // 必须
    "rows":6                               // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                         // 成功 0-成功
		"totalRecord":"20",														// 列表总记录数
		"oftenBuyListModel":[													// 商品列表
			{
				"merchId": "67d4cb03595348cdacd61000bc96ba03",                  // 商品id
                "merchName": "null测试商品 - 1",                                // 商品名
                "merchStatus":"0",												// 是否有货 0-有货 1-暂时缺货
                "sellerId": "4564564564560",                                    // 卖家id
                "sellerName": "卖家 - 1",                                       // 卖家名
				"isPromotion":"0"												// 是否促销 0-促销 1-不是促销
                "danluPrice": "1000",											// 丹露价格
				"goodsPromotionInfo":"促销信息"									// 促销信息(UI中显示“火热促销中”样例)

				"isRecommended":"是否推荐",										// 是否推荐 0-推荐 1-不是推荐
				"minSaleNumber":"3",											// 最小起售数量
				"promotionList":[												// 促销详细信息
					"12345"
				],
				"merchSpec":"箱",												// 商品规格 /件/箱
                "picUrl": "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"	  // 图片URL
			}
		]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.OftenBuyListResponse"
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


class getOftenBuyList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch4 = wsData('Merch4')

    # S1.获取已上架常购列表
    def test_getOftenMerchList_soldUp(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchList = ws.getOftenBuyList(rows="999")
        # 商品1存在
        self.assertGetMerchList(merchList, self.Merch1)
        # 商品4不在列表
        for i in range(0, len(merchList.model['oftenBuyListModel'])):
            if merchList.model['oftenBuyListModel'][i] == self.Merch4.goodsId:
                self.assertEqual(False,True,self.Merch4.fullName + 'is found in oftenBuyList')

    # S2.获取已下架常购列表
    def test_getOftenMerchList_soldOut(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id = ?', '02', self.Merch1.goodsId)
        from www.operation.redisCache import delGoodCache
        delGoodCache(self.Merch1.goodsId, self.UserShop.companyId)
        # 获取下架商品，商品1存在
        merchList = ws.getOftenBuyList(saleFlag="1", rows="999")
        # 下架后商品无促销无推荐
        self.assertGetMerchList(merchList, self.Merch1, isPromotion = '1', isRecommended= '1')

        # 获取上架商品，商品1不在列表
        merchList = ws.getOftenBuyList(saleFlag="1", rows="999")
        for i in range(0, len(merchList.model['oftenBuyListModel'])):
            if merchList.model['oftenBuyListModel'][i] == self.Merch1.goodsId:
                self.assertEqual(False,True,self.Merch1.fullName + 'is found in oftenBuyList')

    # S3.常购列表分页
    def test_getOftenMerchList_page(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getOftenBuyList(rows='999')
        numMerch = len(allMerchList.model['oftenBuyListModel'])
        page = numMerch/4

        time = 0
        for p in range(1,page+2):
            MerchListPage = ws.getOftenBuyList(page=p)
            # 判断商品1是否存在，如果存在time +1
            for i in range(0,len(MerchListPage.model['oftenBuyListModel'])):
                if MerchListPage.model['oftenBuyListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                    time+=1
            if p == page+1:
                self.assertEqual(len(MerchListPage.model['oftenBuyListModel']),numMerch%4,"The last page is wrong")
            else:
                self.assertEqual(len(MerchListPage.model['oftenBuyListModel']),4,"Every page is wrong")

        self.assertEqual(time,1,self.Merch1.fullName+" is not once.")

    # S4.没有常购商品时获取促销列表
    def test_getOftenMerchList_null(self):
        # 修改终端店2的采购区域为香港CHNP032C342D2995
        update('update dlcompany.dl_biz_purchase set purchase_area_code = ? where company_id = ?', 'CHNP032C342D2995', self.UserShop2.companyId)

        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        MerchList = ws.getOftenBuyList(rows='999')
        self.assertEqual(MerchList.model['oftenBuyListModel'],[])


    def tearDown(self):
        # 还原终端店2的采购区域
        update('update dlcompany.dl_biz_purchase set purchase_area_code = ? where company_id = ?', self.UserShop2.areaCode, self.UserShop2.companyId)
        # 还原商品1为上架状态
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id = ?', '01', self.Merch1.goodsId)


    def assertGetMerchList(self, rsp, merch, code = 200, success = '0',isPromotion=None,isRecommended=None):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        if rsp.model['totalRecord'] == '0':
            self.assertEqual(True, False, merch.fullName +"is not found")
        else:
            self.assertEqual(rsp.model['totalRecord'], str(len(rsp.model['oftenBuyListModel'])))
        # 用于判断商品是否存在
        flag = False
        for i in range(0, len(rsp.model['oftenBuyListModel'])):
            if rsp.model['oftenBuyListModel'][i]['merchId'] == merch.goodsId:
                flag = True
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['merchName'],  merch.fullName)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['sellerId'],  merch.seller_store_id)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['sellerName'],  merch.sellerName)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['danluPrice'],  merch.priceDanlu)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['goodsPromotionInfo'],  merch.propagandaInfo)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['merchStatus'],  merch.merchStatus)
                if isPromotion is None:
                    self.assertEqual(rsp.model['oftenBuyListModel'][i]['isPromotion'],  merch.isPromotion)
                else:
                    self.assertEqual(rsp.model['oftenBuyListModel'][i]['isPromotion'],  isPromotion)
                if isRecommended is None:
                    self.assertEqual(rsp.model['oftenBuyListModel'][i]['isRecommended'],  merch.isRecommended)
                else:
                    self.assertEqual(rsp.model['oftenBuyListModel'][i]['isRecommended'],  isRecommended)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['minSaleNumber'],  merch.saleQuantityS1)
                if rsp.model['oftenBuyListModel'][i]['isPromotion'] == '0':
                    for j in range(0, len(rsp.model['oftenBuyListModel'][i]['promotionList'])):
                        flag = False
                        for k in range(1, len(rsp.model['oftenBuyListModel'][i]['promotionList'])+1):
                            if rsp.model['oftenBuyListModel'][i]['promotionList'][j] == merch['promotionList'+str(k)].decode('utf-8'):
                                flag = True
                                break
                            if k == 6:
                                self.assertEqual(flag, True, rsp.model['oftenBuyListModel'][i]['promotionList'][j] + "is not found!")
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['merchSpec'],  merch.merchSpec)
                self.assertEqual(rsp.model['oftenBuyListModel'][i]['picUrl'],  merch.picUrl)
        self.assertEqual(flag, True, merch.fullName +"is not found")




def suite():
    suite = unittest.TestSuite()
    suite.addTest(getOftenBuyList("test_getOftenMerchList_soldUp"))
    suite.addTest(getOftenBuyList("test_getOftenMerchList_soldOut"))
    suite.addTest(getOftenBuyList("test_getOftenMerchList_page"))
    suite.addTest(getOftenBuyList("test_getOftenMerchList_null"))
    return suite
