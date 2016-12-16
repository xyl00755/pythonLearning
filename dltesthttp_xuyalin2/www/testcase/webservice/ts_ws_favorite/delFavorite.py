#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0221.删除收藏(支持批量删除)
http://127.0.0.1:8280/mallws/mydl/favorites/delFavorite.json
{
    "token":"4c521edaed5f4824a822a6416518a847",             // 必须
    "merchId": [                                            // 必须 商品id
		"123",
		"124"
	]
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-未知失败
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    merchId      @NotNull
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""
class delFavorite(unittest.TestCase):
    UserShop2 = wsData('TmlShop2')
    UserShop1 = wsData('TmlShop')
    Merch1=wsData('Merch1')
    Merch2=wsData('Merch2')

    def setUp(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)


    #删除收藏夹一个商品
    def delFavorite_one(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        merchIds=[self.Merch1.goodsId]
        delFavoriteOne=ws.delFavorite(merchId=merchIds)
        self.assertEqual(delFavoriteOne.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #批量删除收藏夹两个商品
    def delFavorite_two(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods1=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods1.model['success'],'0')
        addFavoriteGoods2=ws.addFavorite(merchId=self.Merch2.goodsId)
        self.assertEqual(addFavoriteGoods2.model['success'],'0')
        merchIds=[self.Merch1.goodsId,self.Merch2.goodsId]
        delFavoriteTwo=ws.delFavorite(merchId=merchIds)
        self.assertEqual(delFavoriteTwo.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #删除收藏夹不存在的商品(已提交bug#5591)
    def delFavorite_notExist(self):
         ws=webservice()
         ws.login(self.UserShop2.username,self.UserShop2.password)
         merchIds=[self.Merch1.goodsId]
         delFavoriteOne=ws.delFavorite(merchId=merchIds)
         self.assertEqual(delFavoriteOne.model['success'],'1')
         getFavoriteListGoods=ws.getFavoriteList()
         self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #删除收藏夹数据库不存在的商品(已提交bug#5591)
    def delFavorite_null(self):
         ws=webservice()
         ws.login(self.UserShop2.username,self.UserShop2.password)
         delFavoriteOne=ws.delFavorite(merchId=[123456789])
         self.assertEqual(delFavoriteOne.model['success'],'1')
         getFavoriteListGoods=ws.getFavoriteList()
         self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #删除其他用户收藏的商品(已提交bug#5591)
    def delFavorite_other(self):
         ws=webservice()
         ws.login(self.UserShop2.username,self.UserShop2.password)
         delFavoriteOne=ws.delFavorite(merchId=[self.UserShop1.favoriteMerchId])
         self.assertEqual(delFavoriteOne.model['success'],'1')
         getFavoriteListGoods=ws.getFavoriteList()
         self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])

    #删除收藏中已下架的商品
    def delFavorite_under(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','02',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        delFavoriteListGoods=ws.delFavorite(merchId=[self.Merch1.goodsId])
        self.assertEqual(delFavoriteListGoods.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','01',self.Merch1.goodsId)

    #删除收藏夹锁定的商品
    def delFavorite_lock(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','03',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        delFavoriteListGoods=ws.delFavorite(merchId=[self.Merch1.goodsId])
        self.assertEqual(delFavoriteListGoods.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])
        update('update dlmerchandise.dl_goods set goods_status = ? where goods_id=?','01',self.Merch1.goodsId)

    #删除收藏夹缺货的商品
    def delFavorite_noInventory(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id=?','0',self.Merch1.goodsId)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        delFavoriteListGoods=ws.delFavorite(merchId=[self.Merch1.goodsId])
        self.assertEqual(delFavoriteListGoods.model['success'],'0')
        getFavoriteListGoods=ws.getFavoriteList()
        self.assertEqual(getFavoriteListGoods.model['favoriteList'],[])
        update('update dlmerchandise.dl_goods set on_hand_inventory = ? where goods_id=?',self.Merch1.onHandInventory,self.Merch1.goodsId)

    def tearDown(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)


def suite():
    suite=unittest.TestSuite()
    suite.addTest(delFavorite("delFavorite_one"))
    suite.addTest(delFavorite("delFavorite_two"))
    suite.addTest(delFavorite("delFavorite_under"))
    suite.addTest(delFavorite("delFavorite_lock"))
    suite.addTest(delFavorite("delFavorite_noInventory"))
    return suite