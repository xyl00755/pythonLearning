#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0037.获取商品列表
http://127.0.0.1:8280/mallws/merch/getMerchList.json
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
        "merchList": [
            {
                "merchId": "67d4cb03595348cdacd61000bc96ba03",                  // 商品id
                "merchName": "null测试商品 - 1",                                // 商品名
                "merchStatus":"0",                                              // 商品状态 0-正常 1-暂时缺货
                "sellerId": "4564564564560",                                    // 卖家id
                "sellerName": "卖家 - 1",                                       // 卖家名
                "propagandaInfo": "挥泪大减价，买啥都两块，只要两块",           // 促销语
                "priceRetail": "1000",                                          // 零售价
                "priceDanlu": "0",                                              // 丹露价
                "minStepPrice":"0",                                             // 最低阶梯价
                "fullReduction": "0",                                           // 满降 0-有 1-没有
                "fullPresentation": "0",                                        // 满赠 0-有 1-没有
                "picUrl": "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"  // 图片URL
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchListResponse"
    }
}

参数校验:
    // 只做必须验证
    merchName               @Size(min = 2, max = 100)
    merchCategoryCode       @NotNull
    lowPrice                @Pattern(regexp = "[1-9][0-9]{0,8}")
    highPrice               @Pattern(regexp = "[1-9][0-9]{0,8}")
    sortField               @NotNull        @Pattern(regexp = "1|0")
    sortType                @NotNull        @Pattern(regexp = "1|0")
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
param说明:
    1.如果要查询所有商品列表(包括茶/酒) 则不传merchCategoryCode
    2.如果要查询白酒的商品列表 merchCategoryCode传 C01L0101
    3.如果要查询红酒的商品列表 merchCategoryCode传 C01L0102
    4.如果要查询茶的商品列表 merchCategoryCode传 C01T01
    5.如果要查询具体的茶类目 merchCategoryCode传具体的类目id
"""

import unittest

from www.api.webservice import webservice
from www.common.excel import wsData


class getMerchList(unittest.TestCase):

    UserShop = wsData('TmlShop')
    DealMgr = wsData('DealMager')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')

    # S1.获取所有商品列表
    def test_getMerchList_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getMerchList(rows='99999')
        self.assertEqual(allMerchList.model['success'], '0')
        #numMerchList = select_int('select count(*) from dl_goods.dl_goods_area_buyer_type where area_code = \'CHNP035C345D2998\' and buyer_type = \'S011\'')
        #self.assertEqual(len(allMerchList.model['merchList']), numMerchList)
        flag = False
        for i in range(0,len(allMerchList.model['merchList'])):
            if allMerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

    # S2.根据商品名搜索商品列表——错误 #5244  暂不修改
    def test_getMerchList_searchName(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getMerchList(merchName=self.Merch1.fullName.encode('utf-8'),rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

    # S3.根据类目筛选商品
    def test_getMerchList_filterCategory(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # 筛选白酒
        MerchList1 = ws.getMerchList(merchCategoryCode='C01L0101',rows='999')
        self.assertEqual(MerchList1.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList1.model['merchList'])):
            if MerchList1.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 筛选葡萄酒
        MerchList2 = ws.getMerchList(merchCategoryCode='C01L0102',rows='999')
        self.assertEqual(MerchList2.model['success'], '0')
        for i in range(0,len(MerchList2.model['merchList'])):
            if MerchList2.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not wine, but can find it.')

        # 筛选洋酒
        MerchList3 = ws.getMerchList(merchCategoryCode='C01L0103',rows='999')
        self.assertEqual(MerchList3.model['success'], '0')
        for i in range(0,len(MerchList3.model['merchList'])):
            if MerchList3.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not foreign wine, but can find it.')

        # 筛选啤酒
        MerchList4 = ws.getMerchList(merchCategoryCode='C01L0104',rows='999')
        self.assertEqual(MerchList4.model['success'], '0')
        for i in range(0,len(MerchList4.model['merchList'])):
            if MerchList4.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not beer, but can find it.')

        # 筛选其他饮品
        MerchList = ws.getMerchList(merchCategoryCode='C01X0101',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not drink, but can find it.')

    # S4.筛选茶类茶种
    def test_getMerchList_filterTea(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # 筛选茶
        MerchList = ws.getMerchList(merchCategoryCode='C01T01',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

        # 筛选绿茶——merch为红茶，故判断找不到
        MerchList = ws.getMerchList(merchCategoryCode='C01T0101',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch2.fullName + ' is red tea, but can find it in green tea.')

        # 筛选红茶
        MerchList = ws.getMerchList(merchCategoryCode='C01T0102',rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found.')


    # S5.筛选商品属性
    def test_getMerchList_filterProperty(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)

        # 筛选白酒香型
        MerchList = ws.getMerchList(merchPropertyValueCodeList=["PL20103_split_PL20103V01_split_酱香型"],rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 筛选茶种——祁门红茶
        MerchList = ws.getMerchList(merchCategoryCode="C01T0102",merchPropertyValueCodeList=["PT20201_split_PT20201V01_split_祁门红茶"],rows='999')
        self.assertEqual(MerchList.model['success'], '0')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')


    # S6.筛选商品品牌
    def test_getMerchList_brand(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        # 筛选白酒品牌
        MerchList = ws.getMerchList(merchBrandId="B00003",rows='999')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
                break
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 筛选茶品牌
        MerchList = ws.getMerchList(merchBrandId=self.Merch2.brandId,rows='999')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
                break
        self.assertEqual(flag, True, self.Merch2.fullName.encode('utf-8') + ' is not found')

    # S7.根据卖家ID筛选
    def test_getMerchList_sellerId(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getMerchList(sellerId=self.DealMgr.companyId,rows='999')
        flag = False
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')


    # S8.筛选价格区间_商品1在价格区间，商品2不在
    def test_getMerchList_priceRange(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getMerchList(lowPrice="11900",highPrice="12100",rows='999')
        flag = False
        # 商品1在价格区间
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')

        # 商品2不在价格区间
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

    # S9.筛选价格上限
    def test_getMerchList_priceLimitUpper(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getMerchList(highPrice="12100",rows='999')
        flag = False
        # 商品1在价格区间
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch1.fullName.encode('utf-8') + ' is not found')

        # 商品2不在价格区间
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

    # S10.筛选价格下限
    def test_getMerchList_priceLimitLower(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getMerchList(lowPrice="99900",rows='999')
        flag = False
        # 商品2在价格区间
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch2.fullName:
                flag = True
        self.assertEqual(flag, True, self.Merch2.fullName + ' is not found')

        # 商品1不在价格区间
        for i in range(0,len(MerchList.model['merchList'])):
            if MerchList.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                flag = False
        self.assertEqual(flag, True, self.Merch1.fullName + ' is not found')


    # S11.商品列表排序
    def test_getMerchList_sort(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)

        # 名称升序排列
        MerchListNameAsc = ws.getMerchList(sellerId=self.DealMgr.companyId,sortField="0",sortType="0",rows='999')
        self.assertEqual(MerchListNameAsc.model['merchList'][0]['merchName'].encode('utf-8'),self.Merch1.fullName)
        self.assertEqual(MerchListNameAsc.model['merchList'][1]['merchName'].encode('utf-8'),self.Merch2.fullName)

        # 名称降序排列
        MerchListNameDesc = ws.getMerchList(sellerId=self.DealMgr.companyId,sortField="0",sortType="1",rows='999')
        self.assertEqual(MerchListNameDesc.model['merchList'][0]['merchName'].encode('utf-8'),self.Merch2.fullName)
        self.assertEqual(MerchListNameDesc.model['merchList'][1]['merchName'].encode('utf-8'),self.Merch1.fullName)

        # 价格升序排列
        MerchListPriceAsc = ws.getMerchList(sellerId=self.DealMgr.companyId,sortField="1",sortType="0",rows='999')
        self.assertEqual(MerchListPriceAsc.model['merchList'][0]['merchName'].encode('utf-8'),self.Merch1.fullName)
        self.assertEqual(MerchListPriceAsc.model['merchList'][1]['merchName'].encode('utf-8'),self.Merch2.fullName)

        # 价格降序排列
        MerchListPriceDesc = ws.getMerchList(sellerId=self.DealMgr.companyId,sortField="1",sortType="1",rows='999')
        self.assertEqual(MerchListPriceDesc.model['merchList'][0]['merchName'].encode('utf-8'),self.Merch2.fullName)
        self.assertEqual(MerchListPriceDesc.model['merchList'][1]['merchName'].encode('utf-8'),self.Merch1.fullName)


    # S12.商品分页——判断商品数量是否正确，判断商品是否有重复
    def test_getMerchList_page(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        allMerchList = ws.getMerchList(rows='999')
        numMerch = len(allMerchList.model['merchList'])

        time = 0
        for r in range(1,numMerch/15+2):
            MerchListPage = ws.getMerchList(page=r)
            # 判断商品1是否存在，如果存在time +1
            for i in range(0,len(MerchListPage.model['merchList'])):
                if MerchListPage.model['merchList'][i]['merchName'].encode('utf-8') == self.Merch1.fullName:
                    time+=1
            if r == numMerch/15+1:
                self.assertEqual(len(MerchListPage.model['merchList']),numMerch%15,"The last page is wrong")
            else:
                self.assertEqual(len(MerchListPage.model['merchList']),15,"Every page is wrong")

        self.assertEqual(time,1,self.Merch1.fullName+" is not once.")


    # S13.没有商品时返回为空
    def test_getMerchList_null(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        MerchList = ws.getMerchList(merchName="NotExist")
        self.assertEqual(MerchList.model['merchList'],[],"The merch list is not null.")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getMerchList("test_getMerchList_all"))
    #suite.addTest(getMerchList("test_getMerchList_searchName"))
    suite.addTest(getMerchList("test_getMerchList_filterCategory"))
    suite.addTest(getMerchList("test_getMerchList_filterTea"))
    suite.addTest(getMerchList("test_getMerchList_filterProperty"))
    suite.addTest(getMerchList("test_getMerchList_brand"))
    suite.addTest(getMerchList("test_getMerchList_sellerId"))
    suite.addTest(getMerchList("test_getMerchList_priceRange"))
    suite.addTest(getMerchList("test_getMerchList_priceLimitUpper"))
    suite.addTest(getMerchList("test_getMerchList_priceLimitLower"))
    suite.addTest(getMerchList("test_getMerchList_sort"))
    suite.addTest(getMerchList("test_getMerchList_page"))
    suite.addTest(getMerchList("test_getMerchList_null"))
    return suite