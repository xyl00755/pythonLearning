#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0038.获取商品详情
http://127.0.0.1:8280/mallws/merch/getNewMerchDetail.json
{
    "token":"117f6b5886714107a9c7bcb6d4556f64",                     // 必须
    "merchId":"67d4cb03595348cdacd61000bc96ba03"                    // 必须 商品id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                                                 // 成功 0-成功
        "newMerchDetailModel": {
            "merchId": "67d4cb03595348cdacd61000bc96ba03",                              // 商品id
            "merchName": "测试产品3 珍品古钟红星二锅头 46度 450ml（6瓶/箱）(APP专用)",  // 商品名
            "merchStatus":"0",                                                          // 商品状态 0 有货 1 暂时缺货 2 已下架 3 已失效 4 商品不存在
            "merchSpec":"123",                                                          // 商品规格 /件/箱
            "isFavorite":"0",                                                           // 是否收藏 0-收藏 1-未收藏
            "sellerId": "7b632e29789d406595e93246fdb50fa4",                             // 卖家id
            "sellerName": "黄尾超市",                                                   // 卖家名
            "supportCod": "12",                                                         // 货到付款 0-支持 1-不支持

			"retailPrice":"零售价"														// 零售价
			"danluPrice":"1000"															// 丹露价
			"minSaleNumber":"3"															// 最小起售数量
			"picUrl": "http://danlu-cache.oss-cn-hangzhou.aliyuncs.com/2015/02/06/09/06/1423184802755.jpg"  // 图片URL
            "promotionList":[															// 促销详细信息
					"12345"
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
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.NewMerchDetailResponse"
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


class getNewMerchDetail(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch3 = wsData('Merch3')

    # S1.获取商品详情
    def test_getNewMerchDetail_all(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchDetail = ws.getNewMerchDetail(merchId=self.Merch1.goodsId)
        self.assertgetNewMerchDetail(merchDetail, self.Merch1)

    # S2.获取不存在的商品详情——错误 #5277,暂不修改，先注释掉~
    def test_getNewMerchDetail_NotExist(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchDetail = ws.getNewMerchDetail(merchId='NotExist')
        self.assertEqual(merchDetail.model['newMerchDetailModel']['merchStatus'],'4')

    # S3.获取缺货的商品详情
    def test_getNewMerchDetail_stockout(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set on_hand_inventory = 0 where goods_id = ?', self.Merch1.goodsId)
        merchDetail = ws.getNewMerchDetail(merchId=self.Merch1.goodsId)
        self.assertEqual(merchDetail.model['newMerchDetailModel']['merchStatus'],'1')

    # S4.获取已下架的商品详情
    def test_getNewMerchDetail_soldout(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status = \'02\' where goods_id = ?', self.Merch1.goodsId)
        merchDetail = ws.getNewMerchDetail(merchId=self.Merch1.goodsId)
        self.assertEqual(merchDetail.model['newMerchDetailModel']['merchStatus'],'2')

    # S5.获取已锁定的商品详情
    def test_getNewMerchDetail_lock(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        update('update dlmerchandise.dl_goods set goods_status = \'03\' where goods_id = ?', self.Merch1.goodsId)
        merchDetail = ws.getNewMerchDetail(merchId=self.Merch1.goodsId)
        self.assertEqual(merchDetail.model['newMerchDetailModel']['merchStatus'],'2')

    # S6.获取已失效(没有价格)的商品详情
    def test_getNewMerchDetail_noPrice(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        merchDetail = ws.getNewMerchDetail(merchId=self.Merch3.goodsId)
        self.assertEqual(merchDetail.model['newMerchDetailModel']['merchStatus'],'3')

    # S7.获取无售卖权的商品详情
    def test_getNewMerchDetail_noSalesRight(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        merchDetail = ws.getNewMerchDetail(merchId=self.Merch2.goodsId)
        self.assertEqual(merchDetail.model['newMerchDetailModel']['merchStatus'],'3')


    def tearDown(self):
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id = ?', self.Merch1.onHandInventory, self.Merch1.goodsId)
        update('update dlmerchandise.dl_goods set goods_status = \'01\' where goods_id = ?', self.Merch1.goodsId)

    def assertgetNewMerchDetail(self, rsp, Merch, code = 200, success='0'):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['newMerchDetailModel']['merchId'], Merch['goodsId'])
        self.assertEqual(rsp.model['newMerchDetailModel']['merchName'], Merch['fullName'])
        self.assertEqual(rsp.model['newMerchDetailModel']['merchStatus'], Merch['merchStatus'])
        self.assertEqual(rsp.model['newMerchDetailModel']['merchSpec'], Merch['merchSpec'])
        self.assertEqual(rsp.model['newMerchDetailModel']['isFavorite'], Merch['isFavorite'])
        self.assertEqual(rsp.model['newMerchDetailModel']['sellerId'], Merch['seller_store_id'])
        self.assertEqual(rsp.model['newMerchDetailModel']['sellerName'], Merch['sellerName'])
        self.assertEqual(rsp.model['newMerchDetailModel']['supportCod'], Merch['supportCod'])
        self.assertEqual(rsp.model['newMerchDetailModel']['retailPrice'], Merch['priceRetail'])
        self.assertEqual(rsp.model['newMerchDetailModel']['danluPrice'], Merch['priceS1'])
        self.assertEqual(rsp.model['newMerchDetailModel']['minSaleNumber'], Merch['saleQuantityS1'])
        self.assertEqual(rsp.model['newMerchDetailModel']['picUrl'], Merch['picUrl'])
        for i in range(0, len(rsp.model['newMerchDetailModel']['promotionList'])):
            flag = False
            for j in range(1, len(rsp.model['newMerchDetailModel']['promotionList'])+1):
                if rsp.model['newMerchDetailModel']['promotionList'][i] == Merch['promotionList'+str(j)].decode('utf-8'):
                    flag = True
                    break
                if j == 6:
                    self.assertEqual(flag, True, rsp.model['newMerchDetailModel']['promotionList'][i] + "is not found!")
        for i in range(0, len(rsp.model['newMerchDetailModel']['propertyList'])):
            if rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '生产商':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'生产商'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '净含量':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'净含量'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '保质期':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'保质期'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '包装规格':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'包装规格'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '酒精度':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'酒精度'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '储藏方法':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'储藏方法'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '执行标准号':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'执行标准号'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '生产许可证编号':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'生产许可证编号'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '原料':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'原料'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '适用场景':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'适用场景'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '产地':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'产地'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '香型':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'香型'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '色泽':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'色泽'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '商品类型':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'商品类型'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '产品条码':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch[u'产品条码'].encode('utf-8'))
            elif rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] == '品牌':
                self.assertEqual(rsp.model['newMerchDetailModel']['propertyList'][i]['secondValue'], Merch['brandName'].encode('utf-8'))
            else :
                self.assertEqual(True,False,rsp.model['newMerchDetailModel']['propertyList'][i]['firstValue'] + " is not find in the excel!")
        for i in range(0, len(rsp.model['newMerchDetailModel']['albumPicUrl'])):
            if i == 0:
                self.assertEqual(rsp.model['newMerchDetailModel']['albumPicUrl'][0], Merch['albumPicUrl'])
            else :
                self.assertEqual(rsp.model['newMerchDetailModel']['albumPicUrl'][i], Merch['albumPicUrl'+str(i+1)])
        for i in range(0, len(rsp.model['newMerchDetailModel']['detailPicUrl'])):
            if i == 0:
                self.assertEqual(rsp.model['newMerchDetailModel']['detailPicUrl'][0], Merch['detailPicUrl'])
            else :
                self.assertEqual(rsp.model['newMerchDetailModel']['detailPicUrl'][i], Merch['detailPicUrl'+str(i+1)])
        self.assertEqual(rsp.model['newMerchDetailModel']['unitsConvertion'], int(Merch['unitsConvertion']))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getNewMerchDetail("test_getNewMerchDetail_all"))
    #suite.addTest(getNewMerchDetail("test_getNewMerchDetail_NotExist"))
    suite.addTest(getNewMerchDetail("test_getNewMerchDetail_stockout"))
    suite.addTest(getNewMerchDetail("test_getNewMerchDetail_soldout"))
    suite.addTest(getNewMerchDetail("test_getNewMerchDetail_lock"))
    suite.addTest(getNewMerchDetail("test_getNewMerchDetail_noPrice"))
    suite.addTest(getNewMerchDetail("test_getNewMerchDetail_noSalesRight"))
    return suite
