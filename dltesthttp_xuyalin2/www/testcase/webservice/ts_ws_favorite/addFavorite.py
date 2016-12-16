#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0220.添加收藏
http://127.0.0.1:8280/mallws/mydl/favorites/addFavorite.json
{
    "token":"4c521edaed5f4824a822a6416518a847",             // 必须
    "merchId":"68489979033456f5cbffca2b474e8c83"            // 必须 商品id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-未知失败 2-重复收藏
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class addFavorite(unittest.TestCase):
    UserShop2 = wsData('TmlShop2')
    UserShop1=wsData('TmlShop')
    Merch1=wsData('Merch1')

    def setUp(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)

    # S1.添加已上架的商品到收藏夹
    def test_addFavorite(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteListSize()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(self.Merch1.goodsId,merchIdSql.goods_id)

    # S2.添加已下架商品加入收藏夹
    def test_addFavorite_under(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','02',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteList()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        self.assertEqual(favoriteList.model['favoriteList'][0]['merchStatus'],'2')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(self.Merch1.goodsId,merchIdSql.goods_id)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','01',self.Merch1.goodsId)

    # S3.添加锁定的商品加入收藏夹
    def test_addFavorite_lock(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','03',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteList()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        self.assertEqual(favoriteList.model['favoriteList'][0]['merchStatus'],'2')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(self.Merch1.goodsId,merchIdSql.goods_id)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','01',self.Merch1.goodsId)

    # S4.添加已删除的商品加入收藏夹
    def test_addFavorite_delet(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','99',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteList()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        self.assertEqual(favoriteList.model['favoriteList'][0]['merchStatus'],'4')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(self.Merch1.goodsId,merchIdSql.goods_id)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','01',self.Merch1.goodsId)

    # S5.添加不存在的商品到收藏夹(已提交Bug错误 #5570)

    # S6.添加缺货的商品到收藏夹
    def test_addFavorite_noInventory(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id=?','0',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteList()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        self.assertEqual(favoriteList.model['favoriteList'][0]['merchStatus'],'1')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(self.Merch1.goodsId,merchIdSql.goods_id)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id=?',self.Merch1.onHandInventory,self.Merch1.goodsId)

    # S7.添加无售卖权的商品到收藏夹
    def test_addFavorite_noSaleright(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId='6552b86015b94e46abfe8922d0bee4c9')
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteList()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        self.assertEqual(favoriteList.model['favoriteList'][0]['merchStatus'],'3')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(merchIdSql.goods_id,'6552b86015b94e46abfe8922d0bee4c9')

    # S8.添加无阶梯价的商品到收藏夹
    def test_addFavorite_noStepPrice(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId='86f7456bdd3747d1ba1214d9457a91db')
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteList()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        self.assertEqual(favoriteList.model['favoriteList'][0]['merchStatus'],'3')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(merchIdSql.goods_id,'86f7456bdd3747d1ba1214d9457a91db')

    # S9.重复收藏商品'
    def test_addFavorite_repeat(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        favoriteList=ws.getFavoriteListSize()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')
        merchIdSql=select_one('select goods_id from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        self.assertEqual(self.Merch1.goodsId,merchIdSql.goods_id)
        addFavoriteGoods_repeat=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods_repeat.model['success'],'2')
        favoriteList_repeat=ws.getFavoriteListSize()
        self.assertEqual(favoriteList_repeat.model['favoriteListSize'],'1')

    # S10.收藏-删除-再收藏
    def test_addFavorite_deleteAdd(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)
        addFavorite_more=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavorite_more.model['success'],'0')
        favoriteList=ws.getFavoriteListSize()
        self.assertEqual(favoriteList.model['favoriteListSize'],'1')


    def tearDown(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(addFavorite("test_addFavorite"))
    suite.addTest(addFavorite("test_addFavorite_under"))
    suite.addTest(addFavorite("test_addFavorite_lock"))
    suite.addTest(addFavorite("test_addFavorite_delet"))
    suite.addTest(addFavorite("test_addFavorite_noInventory"))
    suite.addTest(addFavorite("test_addFavorite_noSaleright"))
    suite.addTest(addFavorite("test_addFavorite_noStepPrice"))
    suite.addTest(addFavorite("test_addFavorite_repeat"))
    suite.addTest(addFavorite("test_addFavorite_deleteAdd"))
    return suite



