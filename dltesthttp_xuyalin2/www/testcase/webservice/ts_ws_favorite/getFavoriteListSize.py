#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0223.获取收藏列表数量
http://127.0.0.1:8280/mallws/mydl/favorites/getFavoriteListSize.json
{
    "token":"4c521edaed5f4824a822a6416518a847"
}

{
  "code": 200,
  "description": "执行成功!",
  "model": {
    "success": "0",                                                 // 成功 0-成功
    "favoriteListSize": "1"                                         // 收藏列表数量
  },
  "metadata": {
    "type": 0,
    "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.favorite.FavoriteListSizeResponse"
  }
}

参数校验:
    NONE
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class getFavoriteListSize(unittest.TestCase):
    UserShop2 = wsData('TmlShop2')
    Merch1=wsData('Merch1')
    def setUp(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)

    #收藏列表有一个商品。获取收藏列表数量
    def test_getFavoriteListSize_one(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addFavoriteGoods=ws.addFavorite(merchId=self.Merch1.goodsId)
        self.assertEqual(addFavoriteGoods.model['success'],'0')
        getFavoriteListSizeOne=ws.getFavoriteListSize()
        self.assertEqual(getFavoriteListSizeOne.model['success'],'0')
        self.assertEqual(getFavoriteListSizeOne.model['favoriteListSize'],'1')

    #收藏列表没有商品，获取收藏列表数量
    def test_getFavoriteListSize_zero(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getFavoriteListSizeOne=ws.getFavoriteListSize()
        self.assertEqual(getFavoriteListSizeOne.model['success'],'0')
        self.assertEqual(getFavoriteListSizeOne.model['favoriteListSize'],'0')

    #token错误，获取收藏列表数量
    def test_getFavoriteListSize_tokenError(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getFavoriteListSizeOne=ws.getFavoriteListSize(token='123456789')
        self.assertEqual(getFavoriteListSizeOne.model,None)
        self.assertEqual(getFavoriteListSizeOne.code,100)

    #token为空，获取收藏列表数量
    def test_getFavoriteListSize_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        getFavoriteListSizeOne=ws.getFavoriteListSize(token='null')
        self.assertEqual(getFavoriteListSizeOne.code,600)
        self.assertEqual(getFavoriteListSizeOne.model,None)


    def tearDown(self):
        update('delete from danlu_cd_database.dl_favorites where user_id=?',self.UserShop2.userId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(getFavoriteListSize("test_getFavoriteListSize_one"))
    suite.addTest(getFavoriteListSize("test_getFavoriteListSize_zero"))
    suite.addTest(getFavoriteListSize("test_getFavoriteListSize_tokenError"))
    suite.addTest(getFavoriteListSize("test_getFavoriteListSize_tokenNull"))
    return suite