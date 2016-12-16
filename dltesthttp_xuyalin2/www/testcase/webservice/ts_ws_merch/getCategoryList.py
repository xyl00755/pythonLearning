#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0036.获取品牌列表
http://127.0.0.1:8280/mallws/merch/getCategoryList.json
{
    "token":"123",                                      // 必须
    "merchCategoryCode":"123"                           // 必须 类目code C01T01-茶（webservices已默认绿茶） C01L0101-白酒 C01L0102-葡萄酒 C01L0103-洋酒 C01L0104-啤酒 C01X0101-其他饮品
}

########## 茶 ##########
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "categoryCode": "C01T01",
        "categoryItem": [
            {
                "categoryTuple": {                          // 类目
                    "firstValue": "C01T0101",
                    "secondValue": "绿茶"
                },
                "propertyTupleList": [                      // 属性
                    {
                        "firstValue": "PT20101_split_PT20101V01_split_西湖龙井",
                        "secondValue": "西湖龙井"
                    }
                ],
                "brandTupleList": [                         // 品牌
                    {
                        "firstValue": "B00138",
                        "secondValue": "咏萌"
                    }
                ]
            }
        ]
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchCategoryListResponse"
    }
}

########## 白酒 ##########
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "categoryCode": "C01L0101",
        "categoryItem": {
            "brandTupleList": [                             // 品牌
                {
                    "firstValue": "B00001",
                    "secondValue": "牛栏山"
                }
            ],
            "odorTupleList": [                              // 属性
                {
                    "firstValue": "PL20103_split_PL20103V01_split_酱香型",
                    "secondValue": "酱香型"
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchCategoryListResponse"
    }
}

########## 葡萄酒 ##########
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "categoryCode": "C01L0102",
        "categoryItem": {
            "brandTupleList": [                             // 品牌
                {
                    "firstValue": "B00071",
                    "secondValue": "云南红"
                }
            ],
            "productionTupleList": [                        // 属性
                {
                    "firstValue": "PL20202_split_PL20202V01_split_中国",
                    "secondValue": "中国"
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchCategoryListResponse"
    }
}

########## 洋酒 ##########
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "categoryCode": "C01L0103",
        "categoryItem": {
            "classifyTupleList": [                          // 属性
                {
                    "firstValue": "PL20301_split_PL20301V01_split_威士忌",
                    "secondValue": "威士忌"
                }
            ],
            "brandTupleList": [                             // 品牌
                {
                    "firstValue": "BL3001",
                    "secondValue": "芝华士"
                }
            ],
            "countryTupleList": [                           // 属性
                {
                    "firstValue": "PL20302_split_PL20302V01_split_法国",
                    "secondValue": "法国"
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchCategoryListResponse"
    }
}

########## 啤酒 ##########
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "categoryCode": "C01L0104",
        "categoryItem": {
            "classifyTupleList": [                          // 属性
                {
                    "firstValue": "PL20401_split_PL20401V01_split_黑啤",
                    "secondValue": "黑啤"
                }
            ],
            "brandTupleList": [                             // 品牌
                {
                    "firstValue": "BL4001",
                    "secondValue": "百威"
                }
            ],
            "countryTupleList": [                           // 属性
                {
                    "firstValue": "PL20402_split_PL20402V01_split_中国",
                    "secondValue": "中国"
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchCategoryListResponse"
    }
}

########## 其他饮品 ##########
{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",
        "categoryCode": "C01X01",
        "categoryItem": {
            "brandTupleList": [                             // 品牌
                {
                    "firstValue": "BL4001",
                    "secondValue": "百威"
                }
            ]
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.merch.MerchCategoryListResponse"
    }
}

参数校验:
    // 只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    根据传递的参数不同 会返回不同结构的JSON 需要根据返回值中的categoryCode来选择用什么对象接
    在商品列表接口中 传递的三个主要参数为 类目/属性/品牌 根据本接口中备注的类型传递参数 其中属性可能有多个值
"""

import unittest
from www.common.excel import wsData
from www.api.webservice import webservice
from www.common.database import select_int

class getCategoryList(unittest.TestCase):

    UserShop = wsData('TmlShop')

    wsUserShop = webservice()
    wsUserShop.login(UserShop.username, UserShop.password)

    # S1.获取白酒品牌列表
    def test_getCategoryList_sprit(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        baijiuList = ws.getCategoryList()
        self.assertEqual(baijiuList.model['success'], '0')
        self.assertEqual(baijiuList.model['categoryCode'], 'C01L0101')
        # 校验品牌数量dlcategroy
        numBaijiuBrand = select_int('select count(*) from dlcategroy.dl_brand where brand_id in (select brand_id from dlcategroy.dl_brand_ref_category where category_id = \'C01L0101\' and brand_status = \'01\') and brand_status != \'99\'')
        self.assertEqual(len(baijiuList.model['categoryItem']['brandTupleList']), numBaijiuBrand)
        # 校验香型数量
        numBaijiuProperty = select_int('select count(*) from dlcategroy.dl_property_value where property_id = \'PL20103\'')
        self.assertEqual(len(baijiuList.model['categoryItem']['odorTupleList']), numBaijiuProperty)

    # S2.获取葡萄酒品牌列表
    def test_getCategoryList_wine(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        putaojiuList = ws.getCategoryList(merchCategoryCode = 'C01L0102')
        self.assertEqual(putaojiuList.model['success'], '0')
        self.assertEqual(putaojiuList.model['categoryCode'], 'C01L0102')
        # 校验品牌数量
        numPutaojiuBrand = select_int('select count(*) from dlcategroy.dl_brand where brand_id in (select brand_id from dlcategroy.dl_brand_ref_category where category_id = \'C01L0102\' and brand_status = \'01\') and brand_status != \'99\'')
        self.assertEqual(len(putaojiuList.model['categoryItem']['brandTupleList']), numPutaojiuBrand)
        # 校验产地
        numPutaojiuProperty = select_int('select count(*) from dlcategroy.dl_property_value where property_id = \'PL20202\'')
        self.assertEqual(len(putaojiuList.model['categoryItem']['productionTupleList']), numPutaojiuProperty)

    # S3.获取洋酒的品牌列表
    def test_getCategoryList_foreignwine(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        yangjiuList = ws.getCategoryList(merchCategoryCode = 'C01L0103')
        self.assertEqual(yangjiuList.model['success'], '0')
        self.assertEqual(yangjiuList.model['categoryCode'], 'C01L0103')
        # 校验品牌数量
        numYangjiuBrand = select_int('select count(*) from dlcategroy.dl_brand where brand_id in (select brand_id from dlcategroy.dl_brand_ref_category where category_id = \'C01L0103\' and brand_status = \'01\') and brand_status != \'99\'')
        self.assertEqual(len(yangjiuList.model['categoryItem']['brandTupleList']), numYangjiuBrand)
        # 校验分类数量
        numYangjiuClassify = select_int('select count(*) from dlcategroy.dl_property_value where property_id = \'PL20301\'')
        self.assertEqual(len(yangjiuList.model['categoryItem']['classifyTupleList']), numYangjiuClassify)
        # 校验国家数量
        numYangjiuCountry = select_int('select count(*) from dlcategroy.dl_property_value where property_id = \'PL20302\'')
        self.assertEqual(len(yangjiuList.model['categoryItem']['countryTupleList']), numYangjiuCountry)

    # S4.获取啤酒的品牌列表
    def test_getCategoryList_beer(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        pijiuList = ws.getCategoryList(merchCategoryCode = 'C01L0104')
        self.assertEqual(pijiuList.model['success'], '0')
        self.assertEqual(pijiuList.model['categoryCode'], 'C01L0104')
        # 校验品牌数量
        numPijiuBrand = select_int('select count(*) from dlcategroy.dl_brand where brand_id in (select brand_id from dlcategroy.dl_brand_ref_category where category_id = \'C01L0104\' and brand_status = \'01\') and brand_status != \'99\'')
        self.assertEqual(len(pijiuList.model['categoryItem']['brandTupleList']), numPijiuBrand)
        # 校验分类数量
        numPijiuClassify = select_int('select count(*) from dlcategroy.dl_property_value where property_id = \'PL20401\'')
        self.assertEqual(len(pijiuList.model['categoryItem']['classifyTupleList']), numPijiuClassify)
        # 校验国家数量
        numPijiuCountry = select_int('select count(*) from dlcategroy.dl_property_value where property_id = \'PL20402\'')
        self.assertEqual(len(pijiuList.model['categoryItem']['countryTupleList']), numPijiuCountry)

    # S5.获取茶的品牌列表
    def test_getCategoryList_tea(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        teaList = ws.getCategoryList(merchCategoryCode = 'C01T01')
        self.assertEqual(teaList.model['success'], '0')
        self.assertEqual(teaList.model['categoryCode'], 'C01T01')
        # 校验茶类数量
        numTeaClassify = select_int('select count(*) from dlcategroy.dl_category where parent_category_id = \'C01T01\'')
        self.assertEqual(len(teaList.model['categoryItem']), numTeaClassify)
        # 校验茶种数量——后续补

        # 校验品牌数量——后续补


    # S6.获取其他饮品的品牌列表
    def test_getCategoryList_drink(self):
        ws = webservice()
        ws.login(self.UserShop.username, self.UserShop.password)
        drinkList = ws.getCategoryList(merchCategoryCode = 'C01X0101')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01X0101')
        # 校验其他饮品数量
        numDrinkBrand = select_int('select count(*) from dlcategroy.dl_brand where brand_id in (select brand_id from dlcategroy.dl_brand_ref_category where category_id = \'C01X0101\' and brand_status = \'01\') and brand_status != \'99\'')
        self.assertEqual(len(drinkList.model['categoryItem']['brandTupleList']), numDrinkBrand)

    # S7.获取饮料类目
    def test_getCategoryList_beverage(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01X01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01X01')
        # 校验饮料种类数量
        # numDrinkBrand = select_int('select count(*) from dlcategroy.dl_brand where brand_id in (select brand_id from dlcategroy.dl_brand_ref_category where category_id = \'C01X0101\' and brand_status = \'01\') and brand_status != \'99\'')
        # self.assertEqual(len(drinkList.model['categoryItem']['brandTupleList']), numDrinkBrand)
        # 校验饮料品牌数量

    # S8.获取粮油类目
    def test_getCategoryList_grain(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01G01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01G01')
        # 校验粮油种类

        #校验粮油品牌

    # S9.获取家电类目
    def test_getCategoryList_electrics(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01J01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01J01')
        # 校验家电种类

        # 校验家电品牌


    # S10.获取五金类目
    def test_getCategoryList_metals(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01H01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01H01')
        # 校验五金种类

        # 校验五金品牌

    # S11.获取日化类目
    def test_getCategoryList_dailyChemical(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01P01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01P01')
        # 校验日化种类

        # 校验日化品牌

    # S12.获取副食类目
    def test_getCategoryList_nonstaple(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01F01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01F01')
        # 校验副食种类

        # 校验副食品牌

    # S12.获取其它类目
    def test_getCategoryList_other(self):
        drinkList = self.wsUserShop.getCategoryList(merchCategoryCode = 'C01E01')
        self.assertEqual(drinkList.model['success'], '0')
        self.assertEqual(drinkList.model['categoryCode'], 'C01E01')
        # 校验其它种类

        # 校验其它品牌

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getCategoryList("test_getCategoryList_sprit"))
    suite.addTest(getCategoryList("test_getCategoryList_wine"))
    suite.addTest(getCategoryList("test_getCategoryList_foreignwine"))
    suite.addTest(getCategoryList("test_getCategoryList_beer"))
    suite.addTest(getCategoryList("test_getCategoryList_tea"))
    suite.addTest(getCategoryList("test_getCategoryList_drink"))
    suite.addTest(getCategoryList("test_getCategoryList_beverage"))
    suite.addTest(getCategoryList("test_getCategoryList_grain"))
    suite.addTest(getCategoryList("test_getCategoryList_electrics"))
    suite.addTest(getCategoryList("test_getCategoryList_metals"))
    suite.addTest(getCategoryList("test_getCategoryList_dailyChemical"))
    suite.addTest(getCategoryList("test_getCategoryList_nonstaple"))
    suite.addTest(getCategoryList("test_getCategoryList_other"))
    return suite
