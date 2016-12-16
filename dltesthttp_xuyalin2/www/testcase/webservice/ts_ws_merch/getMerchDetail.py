#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0038.获取商品详情
http://127.0.0.1:8280/mallws/merch/getMerchDetail.json
{
    "token":"117f6b5886714107a9c7bcb6d4556f64",                     // 必须
    "merchId":"67d4cb03595348cdacd61000bc96ba03"                    // 必须 商品id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                                 // 成功 0-成功
        "merchDetail": {
            "merchId": "67d4cb03595348cdacd61000bc96ba03",                              // 商品id
            "merchName": "测试产品3 珍品古钟红星二锅头 46度 450ml（6瓶/箱）(APP专用)",  // 商品名
            "merchStatus":"0",                                                          // 商品状态 0 正常 1 暂时缺货 2 已下架 3 已失效 4 商品不存在
            "merchSpec":"123",                                                          // 商品规格
            "isFavorite":"0",                                                           // 是否收藏 0-收藏 1-未收藏
            "sellerId": "7b632e29789d406595e93246fdb50fa4",                             // 卖家id
            "sellerName": "黄尾超市",                                                   // 卖家名
            "supportCod": "12",                                                         // 货到付款 0-支持 1-不支持
            "inventoryFlag": "0",                                                       // 库存标志 0-有 1-无
            "saleQuantityS1": "11",                                                     // 阶梯价
            "priceS1": "11",
            "saleQuantityS2": "22",
            "priceS2": "21",
            "saleQuantityS3": "33",
            "priceS3": "31",
            "onHandInventory":"123",                                                    // 库存
            "fullReductionList": [                                                      // 满降列表
                "123123"
            ],
            "fullPresentationList": [                                                   // 满赠列表
                "123123"
            ],
            "propertyList": [
                {
                    "firstValue": "商品名称",                                           // 属性名
                    "secondValue": "测试产品3"                                          // 属性值
                }
            ],
            "albumPicUrl": [                                                            // 相册
                "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/04/11/02/1423018927666.jpg",
                "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"
            ],
            "detailPicUrl": [                                                           // 详情
                "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/04/11/02/1423018927666.jpg",
                "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/03/09/22/1422926529478.jpg",
                "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchDetailResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
其他说明:
    属性列表直接拿下面的列表进行展示 忽略上面的列表
"""
import unittest

from www.api.webservice import webservice
from www.common.database import update
from www.common.excel import wsData


class getMerchDetail(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch3 = wsData('Merch3')


    # S1.获取商品详情
    def test_getMerchDetail_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchDetail = ws.getMerchDetail(merchId=self.Merch1.goodsId)
        self.assertGetMerchDetail(merchDetail, self.Merch1)

    # S2.获取不存在的商品详情——错误 #5277,暂不修改，先注释掉~
    def test_getMerchDetail_NotExist(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchDetail = ws.getMerchDetail(merchId='NotExist')
        self.assertEqual(merchDetail.model['merchDetail']['merchStatus'],'4')

    # S3.获取缺货的商品详情
    def test_getMerchDetail_stockout(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set on_hand_inventory = 0 where goods_id = ?', self.Merch1.goodsId)
        merchDetail = ws.getMerchDetail(merchId=self.Merch1.goodsId)
        self.assertEqual(merchDetail.model['merchDetail']['merchStatus'],'1')

    # S4.获取已下架的商品详情
    def test_getMerchDetail_soldout(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status = \'02\' where goods_id = ?', self.Merch1.goodsId)
        merchDetail = ws.getMerchDetail(merchId=self.Merch1.goodsId)
        self.assertEqual(merchDetail.model['merchDetail']['merchStatus'],'2')

    # S5.获取已锁定的商品详情
    def test_getMerchDetail_lock(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status = \'03\' where goods_id = ?', self.Merch1.goodsId)
        merchDetail = ws.getMerchDetail(merchId=self.Merch1.goodsId)
        self.assertEqual(merchDetail.model['merchDetail']['merchStatus'],'2')

    # S6.获取已失效(没有价格)的商品详情
    def test_getMerchDetail_noPrice(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchDetail = ws.getMerchDetail(merchId=self.Merch3.goodsId)
        self.assertEqual(merchDetail.model['merchDetail']['merchStatus'],'3')

    # S7.获取无售卖权的商品详情
    def test_getMerchDetail_noSalesRight(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        merchDetail = ws.getMerchDetail(merchId=self.Merch2.goodsId)
        self.assertEqual(merchDetail.model['merchDetail']['merchStatus'],'3')


    def tearDown(self):
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)
        update('update dlmerchandise.dl_goods set goods_status = \'01\' where goods_id = ?', self.Merch1.goodsId)

    def assertGetMerchDetail(self, rsp, Merch, code = 200, success='0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['merchDetail']['merchId'], Merch['goodsId'])
        self.assertEqual(rsp.model['merchDetail']['merchName'], Merch['fullName'])
        self.assertEqual(rsp.model['merchDetail']['merchStatus'], Merch['merchStatus'])
        self.assertEqual(rsp.model['merchDetail']['merchSpec'], Merch['merchSpec'])
        self.assertEqual(rsp.model['merchDetail']['isFavorite'], Merch['isFavorite'])
        self.assertEqual(rsp.model['merchDetail']['sellerId'], Merch['seller_store_id'])
        self.assertEqual(rsp.model['merchDetail']['sellerName'], Merch['sellerName'])
        self.assertEqual(rsp.model['merchDetail']['supportCod'], Merch['supportCod'])
        self.assertEqual(rsp.model['merchDetail']['inventoryFlag'], Merch['inventoryFlag'])
        self.assertEqual(rsp.model['merchDetail']['saleQuantityS1'], Merch['saleQuantityS1'])
        self.assertEqual(rsp.model['merchDetail']['priceS1'], Merch['priceS1'])
        if rsp.model['merchDetail']['saleQuantityS2'] is not None:
            self.assertEqual(rsp.model['merchDetail']['saleQuantityS2'], Merch['saleQuantityS2'])
            self.assertEqual(rsp.model['merchDetail']['priceS2'], Merch['priceS2'])
        if rsp.model['merchDetail']['saleQuantityS3'] is not None:
            self.assertEqual(rsp.model['merchDetail']['saleQuantityS3'], Merch['saleQuantityS3'])
            self.assertEqual(rsp.model['merchDetail']['priceS3'], Merch['priceS3'])
        self.assertEqual(rsp.model['merchDetail']['onHandInventory'], Merch['onHandInventory'])
        for i in range(0, len(rsp.model['merchDetail']['fullReductionList'])):
            if i == 0:
                self.assertEqual(rsp.model['merchDetail']['fullReductionList'][0], Merch['fullReductionList'].decode('utf-8'))
            else :
                self.assertEqual(rsp.model['merchDetail']['fullReductionList'][i], Merch['fullReductionList'+str(i+1)].decode('utf-8'))
        for i in range(0, len(rsp.model['merchDetail']['fullPresentationList'])):
            if i == 0:
                self.assertEqual(rsp.model['merchDetail']['fullPresentationList'][0], Merch['fullPresentationList'].decode('utf-8'))
            else :
                self.assertEqual(rsp.model['merchDetail']['fullPresentationList'][i], Merch['fullPresentationList'+str(i+1)].decode('utf-8'))
        for i in range(0, len(rsp.model['merchDetail']['propertyList'])):
            if rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '生产商':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'生产商'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '净含量':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'净含量老'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '净含量单位':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'净含量单位'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '保质期':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'保质期'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '包装规格':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'包装规格'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '酒精度':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'酒精度老'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '储藏方法':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'储藏方法'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '执行标准号':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'执行标准号'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '生产许可证编号':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'生产许可证编号'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '原料':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'原料'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '适用场景':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'适用场景'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '产地':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'产地'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '香型':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'香型'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '色泽':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'色泽'].encode('utf-8'))
            elif rsp.model['merchDetail']['propertyList'][i]['firstValue'] == '商品类型':
                self.assertEqual(rsp.model['merchDetail']['propertyList'][i]['secondValue'], Merch[u'商品类型'].encode('utf-8'))
            else :
                self.assertEqual(True,False,rsp.model['merchDetail']['propertyList'][i]['firstValue'] + " is not find in the excel!")


        for i in range(0, len(rsp.model['merchDetail']['albumPicUrl'])):
            if i == 0:
                self.assertEqual(rsp.model['merchDetail']['albumPicUrl'][0], Merch['albumPicUrl'])
            else :
                self.assertEqual(rsp.model['merchDetail']['albumPicUrl'][i], Merch['albumPicUrl'+str(i+1)])
        for i in range(0, len(rsp.model['merchDetail']['detailPicUrl'])):
            if i == 0:
                self.assertEqual(rsp.model['merchDetail']['detailPicUrl'][0], Merch['detailPicUrl'])
            else :
                self.assertEqual(rsp.model['merchDetail']['detailPicUrl'][i], Merch['detailPicUrl'+str(i+1)])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getMerchDetail("test_getMerchDetail_all"))
    #suite.addTest(getMerchDetail("test_getMerchDetail_NotExist"))
    suite.addTest(getMerchDetail("test_getMerchDetail_stockout"))
    suite.addTest(getMerchDetail("test_getMerchDetail_soldout"))
    suite.addTest(getMerchDetail("test_getMerchDetail_lock"))
    suite.addTest(getMerchDetail("test_getMerchDetail_noPrice"))
    suite.addTest(getMerchDetail("test_getMerchDetail_noSalesRight"))
    return suite
