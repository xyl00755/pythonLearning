#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0037.获取商品列表
http://127.0.0.1:8280/mallws/merch/getNewMerchList.json
{
    "token":"123",                      // 必须
    "merchName":"金奖黑砖",             // 可选 商品名
    "merchCategoryCode":"????",         // 必须 商品类目id
    "merchPropertyValueCodeList":[      // 可选 商品属性id列表
        "ids"
    ],
    "merchBrandId":"?????",             // 可选 商品品牌id
    "sellerId":"123",                   // 可选 卖家id
    "lowPrice":"159",                   // 可选 最低价
    "highPrice":"999",                  // 可选 最高价
    "sortField":"0",                    // 必须 排序字段 0 按名称排序 1 按价格排序
    "sortType":"0",                     // 必须 排序方式 0 升序 1 降序
    "page":1,                           // 必须
    "rows":15                           // 必须
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                         // 成功 0-成功
		"totalRecord":"20",														// 列表总记录数
        "newMerchListModel": [
            {
                "merchId": "67d4cb03595348cdacd61000bc96ba03",                  // 商品id
                "merchName": "null测试商品 - 1",                                // 商品名
                "merchStatus":"0",                                              // 是否有货 0-正常 1-暂时缺货
                "sellerId": "4564564564560",                                    // 卖家id
                "sellerName": "卖家 - 1",                                       // 卖家名
                "retailPrice": "1000",                                          // 零售价
                "danluPrice": "0",                                              // 丹露价

				"minSaleNumber":"3",											// 最小起售数量
				"goodsPromotionInfo":"促销信息"									// 促销信息(UI中显示“火热促销中”样例)
				"isPromotion":"0"												// 是否促销 0-促销 1-不是促销
				"isRecommended":"是否推荐",										// 是否推荐 0-推荐 1-不是推荐
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
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.NewMerchListResponse"
    }
}
"""

import unittest

from www.api.webservice import webservice
from www.common.excel import wsData


class getNewMerchList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    DealMgr = wsData('DealMager')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')

    # S1.获取所有商品列表
    def test_getNewMerchList_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getNewMerchList(rows='99999')
        self.assertMerchList(allMerchList, self.Merch1)

    # S2.根据商品名(全名)搜索商品列表——错误 #5244  暂不修改
    def test_getNewMerchList_searchName(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(merchName=self.Merch1.fullName.encode('utf-8'),rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

    # S3.搜索商品名称
    def test_getNewMerchList_searchGoodsName(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(merchName=self.Merch1.goodsName.encode('utf-8'),rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

    # S4.搜索产品名称
    def test_getNewMerchList_searchProductName(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(merchName=self.Merch1.productName.encode('utf-8'),rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

    # S5.根据类目筛选商品
    def test_getNewMerchList_filterCategory(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # 筛选白酒
        MerchList1 = ws.getNewMerchList(merchCategoryCode='C01L0101',rows='999')
        self.assertEqual(MerchList1.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList1.model['newMerchListModel'])):
            if MerchList1.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 筛选葡萄酒
        MerchList2 = ws.getNewMerchList(merchCategoryCode='C01L0102',rows='999')
        self.assertEqual(MerchList2.model['success'], '0')
        for i in range(0,len(MerchList2.model['newMerchListModel'])):
            if MerchList2.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not wine, but can find it.')

        # 筛选洋酒
        MerchList3 = ws.getNewMerchList(merchCategoryCode='C01L0103',rows='999')
        self.assertEqual(MerchList3.model['success'], '0')
        for i in range(0,len(MerchList3.model['newMerchListModel'])):
            if MerchList3.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not foreign wine, but can find it.')

        # 筛选啤酒
        MerchList4 = ws.getNewMerchList(merchCategoryCode='C01L0104',rows='999')
        self.assertEqual(MerchList4.model['success'], '0')
        for i in range(0,len(MerchList4.model['newMerchListModel'])):
            if MerchList4.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not beer, but can find it.')

        # 筛选其他饮品
        MerchList = ws.getNewMerchList(merchCategoryCode='C01X0101',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not drink, but can find it.')

    # S6.筛选茶类茶种
    def test_getNewMerchList_filterTea(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # 筛选茶
        MerchList = ws.getNewMerchList(merchCategoryCode='C01T01',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

        # 筛选绿茶——merch为红茶，故判断找不到
        MerchList = ws.getNewMerchList(merchCategoryCode='C01T0101',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch2.fullName + ' is red tea, but can find it in green tea.')

        # 筛选红茶
        MerchList = ws.getNewMerchList(merchCategoryCode='C01T0102',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found.')


    # S7.筛选商品属性
    def test_getNewMerchList_filterProperty(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)

        # 筛选白酒香型
        MerchList = ws.getNewMerchList(merchPropertyValueCodeList=["PL20103_split_PL20103V01_split_酱香型"],rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 筛选茶种——祁门红茶
        MerchList = ws.getNewMerchList(merchCategoryCode="C01T0102",merchPropertyValueCodeList=["PT20201_split_PT20201V01_split_祁门红茶"],rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')


    # S8.筛选商品品牌
    def test_getNewMerchList_brand(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # 筛选白酒品牌
        MerchList = ws.getNewMerchList(merchBrandId="B00003",rows='999')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
                break
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 筛选茶品牌
        MerchList = ws.getNewMerchList(merchBrandId=self.Merch2.brandId,rows='999')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
                break
        self.assertEqual(flag, True, self.Merch2.fullName.encode('utf-8') + ' is not found')

    # S9.根据卖家ID筛选
    def test_getNewMerchList_sellerId(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(sellerId=self.DealMgr.companyId,rows='999')
        flag = False
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')


    # S10.筛选价格区间_商品1在价格区间，商品2不在
    def test_getNewMerchList_priceRange(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(lowPrice="11900",highPrice="12100",rows='999')
        flag = False
        # 商品1在价格区间
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 商品2不在价格区间
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

    # S11.筛选价格上限
    def test_getNewMerchList_priceLimitUpper(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(highPrice="12100",rows='999')
        flag = False
        # 商品1在价格区间
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName.encode('utf-8') + ' is not found')

        # 商品2不在价格区间
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

    # S12.筛选价格下限
    def test_getNewMerchList_priceLimitLower(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(lowPrice="99900",rows='999')
        flag = False
        # 商品2在价格区间
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

        # 商品1不在价格区间
        for i in range(0,len(MerchList.model['newMerchListModel'])):
            if MerchList.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')


    # S13.商品列表排序
    def test_getNewMerchList_sort(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)

        # 名称升序排列
        MerchListNameAsc = ws.getNewMerchList(sellerId=self.DealMgr.companyId,sortField="0",sortType="0",rows='999')
        self.assertEqual(MerchListNameAsc.model['newMerchListModel'][0]['merchName'].encode('utf-8'),self.Merch1.fullName)
        self.assertEqual(MerchListNameAsc.model['newMerchListModel'][1]['merchName'].encode('utf-8'),self.Merch2.fullName)

        # 名称降序排列
        MerchListNameDesc = ws.getNewMerchList(sellerId=self.DealMgr.companyId,sortField="0",sortType="1",rows='999')
        self.assertEqual(MerchListNameDesc.model['newMerchListModel'][0]['merchName'].encode('utf-8'),self.Merch2.fullName)
        self.assertEqual(MerchListNameDesc.model['newMerchListModel'][1]['merchName'].encode('utf-8'),self.Merch1.fullName)

        # 价格升序排列
        MerchListPriceAsc = ws.getNewMerchList(sellerId=self.DealMgr.companyId,sortField="1",sortType="0",rows='999')
        self.assertEqual(MerchListPriceAsc.model['newMerchListModel'][0]['merchName'].encode('utf-8'),self.Merch1.fullName)
        self.assertEqual(MerchListPriceAsc.model['newMerchListModel'][1]['merchName'].encode('utf-8'),self.Merch2.fullName)

        # 价格降序排列
        MerchListPriceDesc = ws.getNewMerchList(sellerId=self.DealMgr.companyId,sortField="1",sortType="1",rows='999')
        self.assertEqual(MerchListPriceDesc.model['newMerchListModel'][0]['merchName'].encode('utf-8'),self.Merch2.fullName)
        self.assertEqual(MerchListPriceDesc.model['newMerchListModel'][1]['merchName'].encode('utf-8'),self.Merch1.fullName)


    # S14.商品分页——判断商品数量是否正确，判断商品是否有重复
    def test_getNewMerchList_page(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getNewMerchList(rows='999')
        numMerch = len(allMerchList.model['newMerchListModel'])
        rows = numMerch/15

        time = 0
        for r in range(1,numMerch/15+2):
            MerchListPage = ws.getNewMerchList(page=r)
            # 判断商品1是否存在，如果存在time +1
            for i in range(0,len(MerchListPage.model['newMerchListModel'])):
                if MerchListPage.model['newMerchListModel'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                    time+=1
            if r == numMerch/15+1:
                self.assertEqual(len(MerchListPage.model['newMerchListModel']),numMerch%15,"The last page is wrong")
            else:
                self.assertEqual(len(MerchListPage.model['newMerchListModel']),15,"Every page is wrong")

        self.assertEqual(time,1,self.Merch1.fullName+" is not once.")


    # S15.没有商品时返回为空
    def test_getNewMerchList_null(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getNewMerchList(merchName="NotExist")
        self.assertEqual(MerchList.model['newMerchListModel'],[],"The merch list is not null.")

    def assertMerchList(self, rsp, merch, code = 200, success = '0',isPromotion='0',isRecommended='0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        if rsp.model['totalRecord'] == '0':
            self.assertEqual(True, False, merch.fullName +"is not found")
        else:
            self.assertEqual(rsp.model['totalRecord'], str(len(rsp.model['newMerchListModel'])))
        flag = False
        for i in range(0, len(rsp.model['newMerchListModel'])):
            if rsp.model['newMerchListModel'][i]['merchId'] == merch.goodsId:
                flag = True
                self.assertEqual(rsp.model['newMerchListModel'][i]['merchName'],  merch.fullName)
                self.assertEqual(rsp.model['newMerchListModel'][i]['sellerId'],  merch.seller_store_id)
                self.assertEqual(rsp.model['newMerchListModel'][i]['sellerName'],  merch.sellerName)
                self.assertEqual(rsp.model['newMerchListModel'][i]['retailPrice'],  merch.priceRetail)
                self.assertEqual(rsp.model['newMerchListModel'][i]['danluPrice'],  merch.priceDanlu)
                self.assertEqual(rsp.model['newMerchListModel'][i]['goodsPromotionInfo'],  merch.propagandaInfo)
                self.assertEqual(rsp.model['newMerchListModel'][i]['merchStatus'],  merch.merchStatus)
                self.assertEqual(rsp.model['newMerchListModel'][i]['isPromotion'],  merch.isPromotion)
                self.assertEqual(rsp.model['newMerchListModel'][i]['isRecommended'],  merch.isRecommended)
                self.assertEqual(rsp.model['newMerchListModel'][i]['minSaleNumber'],  merch.saleQuantityS1)
                # for j in range(0,len(rsp.model['newMerchListModel'][i]['promotionList'])):
                #     self.assertEqual(rsp.model['newMerchListModel'][i]['promotionList'][j],  merch['promotionList'+str(j+1)].decode('utf-8'))

                for j in range(0, len(rsp.model['newMerchListModel'][i]['promotionList'])):
                    flag = False
                    for k in range(1, len(rsp.model['newMerchListModel'][i]['promotionList'])+1):
                        if rsp.model['newMerchListModel'][i]['promotionList'][j] == merch['promotionList'+str(k)].decode('utf-8'):
                            flag = True
                            break
                        if k == 6:
                            self.assertEqual(flag, True, rsp.model['newMerchListModel'][i]['promotionList'][j] + "is not found!")

                self.assertEqual(rsp.model['newMerchListModel'][i]['merchSpec'],  merch.merchSpec)
                self.assertEqual(rsp.model['newMerchListModel'][i]['picUrl'],  merch.picUrl)
        self.assertEqual(flag, True, merch.fullName +"is not found")



def suite():
    suite = unittest.TestSuite()
    suite.addTest(getNewMerchList("test_getNewMerchList_all"))
    #suite.addTest(getNewMerchList("test_getNewMerchList_searchName"))
    suite.addTest(getNewMerchList("test_getNewMerchList_searchGoodsName"))
    suite.addTest(getNewMerchList("test_getNewMerchList_searchProductName"))
    suite.addTest(getNewMerchList("test_getNewMerchList_filterCategory"))
    suite.addTest(getNewMerchList("test_getNewMerchList_filterTea"))
    suite.addTest(getNewMerchList("test_getNewMerchList_filterProperty"))
    suite.addTest(getNewMerchList("test_getNewMerchList_brand"))
    suite.addTest(getNewMerchList("test_getNewMerchList_sellerId"))
    suite.addTest(getNewMerchList("test_getNewMerchList_priceRange"))
    suite.addTest(getNewMerchList("test_getNewMerchList_priceLimitUpper"))
    suite.addTest(getNewMerchList("test_getNewMerchList_priceLimitLower"))
    suite.addTest(getNewMerchList("test_getNewMerchList_sort"))
    suite.addTest(getNewMerchList("test_getNewMerchList_page"))
    suite.addTest(getNewMerchList("test_getNewMerchList_null"))
    return suite