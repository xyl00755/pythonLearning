#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0130.获取确认订单信息
http://127.0.0.1:8280/mallws/shoppingcart/getPreViewOrderByShoppingcart.json
{
    "token":"123",                                                      // 必须
    "toSettlementModel":[                                               // 卖家模型
        {
            "sellerId": "7b632e29789d406595e93246fdb50fa4",             // 必须 卖家id
            "sellerName":"123",                                         // 必须 卖家名
			"isYijipayAccount": "0",                                    // 必须 卖家是否是易极付账户 0-是 1-不是
            "paymentFlag": "0",                                         // 必须 购物车接口的 paymentFlag
            "codFlag": "0",                                             // 必须 购物车接口的 codFlag
            "supportVatInvoice": "0",                                   // 必须 购物车接口的 supportVatInvoice
            "merchList": [                                              // 商品列表模型
                {
                    "id": "b8d8f93a5eae48b4a8918f741982d405",           // 必须 购物车主键
                    "merchId": "67d4cb03595348cdacd61000bc96ba03",      // 必须 商品id
                    "merchName": "liuliuliu",                           // 必须 商品名
                    "merchBarCode": "TM003",                            // 必须 商品条码
                    "promotionId": "",                                  // 可选 促销id
                    "promotionType":"",                                 // 可选 促销类型 0-满赠 1-满减
                    "reductionFlg":"",                                  // 可选 满减类型 0-减单价 1-减总额
                    "promotionDetail":""                                // 可选 促销详情
                    "ruleId":"123"                                      // 可选 规则
                }
            ]
        }
    ]
}

{
    "code": 200,
    "description": "执行成功!",
    "metadata": {
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.PreViewOrderResponse",
        "type": 0
    },
    "model": {
        "failedReasons": {                                  // 去结算失败 返回的失败原因
            "notExistsList": [                              // 商品不存在 提示: "以上商品在购物车中不存在，请先查看最新信息"
                "商品名/店铺名"
            ],
            "lessThanMiniStartSaleQuantityList": [          // 商品数量小于最小起售量
                "商品名/店铺名"
            ],
            "delList": [                                    // 产品被删除 提示："以上商品不存在，无法购买"
                "商品名/店铺名"
            ],
            "invalidList": [                                // 无售卖权或无价格 提示："以上商品已失效，无法购买"
                "商品名/店铺名"
            ],
            "nameChangedList": [                            // 商品名称发生变化 提示："xx商品名称更改为xx商品    以上商品名称发生改变，请先查看最新信息"
                "商品名/店铺名"                             // 返回值为 : "xx商品名称更改为xx商品" 不用自己拼接 只用补最后一句
            ],
            "noInventoryList": [                            // 无库存 提示："以上商品暂时缺货，无法购买"
                "商品名/店铺名"
            ],
            "noOnHandInventoryList": [                      // 有库存但不足 提示："以上商品库存不足，请修改购买数量"
                "商品名/店铺名"
            ],
            "noSupplyInvoicList": [                         // 选择需要结算的商品对应的配送商如果由支持"开增值税发票"变为不支持 提示："以上配送商不再支持开增值税票，请查看最新信息"
                "商品名/店铺名"
            ],
            "priceChangedList": [                           // 价格变动 提示："以上商品价格变动，请先查看最新价格"
                "商品名/店铺名"
            ],
            "promotiontChangedList": [                      // 促销信息发生变化 提示："以上商品促销信息已变化，请查看最新的促销信息"
                "商品名/店铺名"
            ],
            "shelvesOffList": [                             // 平台或卖家操作下架（或锁定） 提示："以上商品已下架，无法购买"
                "商品名/店铺名"
            ],
            "specChangedList": [                            // 商品规格发生变化 提示："xx商品规格由x更改为x 以上商品规格发生改变，请先查看最新信息"
                "商品名/店铺名"                             // 返回值为："xx商品规格由x更改为x" 不用自己拼接 只用补最后一句
            ],
            "supplyCodPaymentChangedList": [                // 支付方式变化（增加或取消货到付款） 提示："以上配送商支付方式发生变动，请先查看最新信息"
                "商品名/店铺名"
            ]
        },
        "toSettlementInfoModel": {                                          // 去结算成功模型
            "defaultNormalInvoice": {                                       // 默认普通发票模型
                "customerId": "76fc5f07fcef421a9cd4b9cb17ca1f27",           // 用户id
                "invoiceId": "c9f0150a179e43c5a5bbd7566a94c13a",            // 发票id
                "invoiceType": "N011",                                      // 发票类型 N011-普通发票 N012-增值税发票
                "invoiceHeader": "DHC",                                     // 发票抬头
                "companyName": "",
                "taxpayerRegistrationNumber": "",
                "registerAddress": "",
                "registerTel": "",
                "depositBank": "",
                "accountBank": "",
                "accountLicence": "",
                "isDefault": "0",                                           // 是否默认 0-默认 1-非默认
                "receiveManName": null,
                "receiveManTel": null,
                "receiveManProvince": null,
                "receiveManAddress": null
            },
            "vatInvoice": {                                                   // 默认增值税发票模型
                "customerId": "76fc5f07fcef421a9cd4b9cb17ca1f27",             // 用户id
                "invoiceId": "4ec418ce99544c619bdfbb0a7ce9a9d8",              // 发票id
                "invoiceType": "N012",                                        // 发票类型 N011-普通发票 N012-增值税发票
                "invoiceHeader": "",
                "companyName": "大连DHC",                                     // 公司名称
                "taxpayerRegistrationNumber": "2234332223",                   // 纳税人识别号
                "registerAddress": "辽宁省大连市",                            // 注册地址
                "registerTel": "13478464122",                                 // 注册电话
                "depositBank": "建设银行",                                    // 开户银行
                "accountBank": "324485858493939239383849494393",              // 帐户银行
                "accountLicence": "",                                         // 开户许可证
                "isDefault": null,                                            // 是否默认 0-默认 1-非默认
                "receiveManName": null,                                       // 收票人姓名
                "receiveManTel": null,                                        // 收票人电话
                "receiveManProvince": null,                                   // 收票人省份
                "receiveManAddress": null                                     // 收票人详细地址
            },
            "deliverAddress": {                                       // 默认收货地址模型 具体见收货地址接口文档-列表接口
                "addressId": "1aefb9a18c5a4f0089b67903c5d5bd2a",      // 收货地址id
                "customerId": "76fc5f07fcef421a9cd4b9cb17ca1f27",     // 用户id
                "areaProvinceCode": "P014",                           // 省id
                "areaProvinceName": "辽宁",                           // 省名
                "areaCityCode": "C124",                               // 市id
                "areaCityName": "大连",                               // 市名
                "areaDistrictCode": "D1179",                          // 区id
                "areaDistrictName": "高新区",                         // 区名
                "addressDetail": "dd",                                // 详细地址
                "zipCode": "",                                        // 邮编
                "deliverPerson": "xt",                                // 收货人
                "deliverMobile": "13390006677",                       // 联系电话
                "deliverTel": "",                                     // 固定电话
                "isDefault": "1",                                     // 是否默认 0-默认 1-非默认
            },
            "couponList": [                                           // 优惠券列表
                {
                    "couponId":"",                                    // 优惠券id
                    "companyId":"",                                   // 企业id
                    "couponCode":"",                                  // 优惠券code
                    "applyMerch":"",                                  // 适用商品
                    "couponFee":"",                                   // 优惠价
                    "couponDescrip":""                                // 优惠券描述
                }
            ]
        }
        "success": "1"                                                // 去结算结果 0-成功 1-失败
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
result说明:
    当success字段为0时 toSettlementInfoModel模型有值 当success字段为1时 failedReasons模型有值 如果无值 返回null
"""

import unittest

from www.api.webservice import *
from www.common.database import update
from www.common.excel import wsData
from www.common.model import Shoppingcart


class getPreViewOrderByShoppingcart(unittest.TestCase):

    UserShop = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')
    Merch1 = wsData('Merch1')
    Merch2 = wsData('Merch2')
    Merch4 = wsData('Merch4')

    def setUp(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop2.userId)

    # S1.获取确认订单信息
    def test_getPreViewOrderByShoppingcart_add(self):
        ws = webservice()
        ws.login(self.UserShop2.username, self.UserShop2.password)
        ws.addShoppingcar(merchId=self.Merch1.goodsId, merchCount='1', sellerId=self.Merch1.seller_store_id, sellerName=self.Merch1.sellerName)
        shopcart = Shoppingcart.find_first('where user_id = ? and goods_id = ?', self.UserShop2.userId, self.Merch1.goodsId)
        settlement = self.SettlementModel(self.Merch1, shopcart.id)
        getPreViewOrderByShoppingcart = ws.getPreViewOrderByShoppingcart(settlement)



    # 获取订单信息请求消息model
    def SettlementModel(self, merch, shopcartID):
        Settlement = {"sellerId": merch.shopcartSellerId, "sellerName":merch.sellerName, "isYijipayAccount": merch.isYijipayAccount, "paymentFlag": merch.paymentFlag, "codFlag":merch.supportCod,
                      "supportVatInvoice":merch.supportVatInvoice}
        merchList = []
        merchList.append({"id": shopcartID,"merchId": merch.goodsId,"merchName": merch.fullName, "merchBarCode": merch.productBarCode, "promotionId": "", "promotionType":"", "reductionFlg":"", "promotionDetail":"","ruleId":"123" })
        Settlement['merchList'] = merchList
        return Settlement

    def tearDown(self):
        update('delete from danlu_cd_database.dl_shoppingcart where user_id = ?', self.UserShop2.userId)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getPreViewOrderByShoppingcart("test_getPreViewOrderByShoppingcart_add"))
    return suite

