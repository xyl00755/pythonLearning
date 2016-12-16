#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""

0222.获取收藏列表
http://127.0.0.1:8280/mallws/mydl/favorites/getFavoriteList.json
{
    "token":"4c521edaed5f4824a822a6416518a847",                      // 必须 token
	"page": "2",                                                     // 必须 页码 起始页为1
	"rows": "10",                                                    // 必须 每页条数 第一页为20 其他页为10
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                             // 成功 0-成功
        "favoriteListSize": "1",                                    // 收藏数量
        "favoriteList": [
            {
                "merchId": "68489979033456f5cbffca2b474e8c83",      // 商品id
                "merchName": "ceshi, 312312",                       // 商品名
                "merchStatus": "0",                           // 商品状态 0 正常 1 暂时缺货 2 已下架（包含锁定） 3 已失效 4商品不存在（新增）
                "sellerId": "12",                                   // 卖家id
                "sellerName": "34",                                 // 卖家名
                "propagandaInfo": "五折优惠",                       // 促销语
                "unitPrice": "2000",                                // 单价
                "fullReduction": "1",                               // 满降 0-有 1-无
                "fullPresentation": "0",                            // 满赠 0-有 1-无
                "picUrl": "http://afadsfasdf.img"                   // 图片URL
            }
        ],
		"currPage": "2"                                             // 当前页
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.favorite.FavoriteListResponse"
    }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆

"""

class getFavoriteList(unittest.TestCase):
    UserShop2 = wsData('TmlShop2')
    UserShop1=wsData('TmlShop')
    Merch1=wsData('Merch1')

    def setUp(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)

    #收藏列表有商品获取收藏列表
    def test_getFavoriteList(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['success'],'0')
        self.assertEqual(getFavoriteListGoods.model['favoriteListSize'],'1')
        self.assertEqual(getFavoriteListGoods.model['favoriteList'][0]['merchStatus'],'0')
        self.assertGetFavoriteGoodsSuccess(getFavoriteListGoods)

    #收藏列表没有商品直接获取商品列表
    def test_getFavoriteList_noGoods(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['success'],'0')
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #设置page=2,rows=10,获取收藏列表
    def test_getFavoriteList_page(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList(page=2,rows=10)
        self.assertEqual(getFavoriteListGoods.model['success'],'0')
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #token为空获取收藏列表
    def test_getFavoriteList_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getFavoriteListGoods=ws.getFavoriteList(token='null')
        self.assertEqual(getFavoriteListGoods.code,600)
        self.assertEqual(getFavoriteListGoods.model,None)

    #token错误获取收藏列表
    def test_getFavoriteList_tokenError(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getFavoriteListGoods=ws.getFavoriteList(token='123456789')
        self.assertEqual(getFavoriteListGoods.code,100)
        self.assertEqual(getFavoriteListGoods.model,None)

    def assertGetFavoriteGoodsSuccess(self,getFavoriteGoodsList):
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['merchId'],self.Merch1.goodsId)
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['merchName'],self.Merch1.fullName)
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['sellerId'],self.Merch1.sellerId)
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['sellerName'],self.Merch1.sellerName)
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['propagandaInfo'],self.Merch1.propagandaInfo)
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['unitPrice'],str(int(self.Merch1.unitPrice)/100))
        self.assertEqual(getFavoriteGoodsList.model['favoriteList'][0]['picUrl'],self.Merch1.picUrl)


    def tearDown(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(getFavoriteList("test_getFavoriteList"))
    suite.addTest(getFavoriteList("test_getFavoriteList_noGoods"))
    suite.addTest(getFavoriteList("test_getFavoriteList_page"))
    suite.addTest(getFavoriteList("test_getFavoriteList_tokenNull"))
    suite.addTest(getFavoriteList("test_getFavoriteList_tokenError"))
    return suite
