#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
0070.获取订单商品快照
http://127.0.0.1:8280/mallws/orders/getOrderMerchSnapshot.json
{
    "token": "57469529686440a88fedb0bed51ba5d0",        // 必须
    "orderNo":"123123123",                              // 必须 小订单号
    "merchId":"123123123"                               // 必须 商品id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                 // 成功 0-成功
        "merchSnapshot": {
            "merchId": null,                            // 商品id
            "merchNo": null,                            // 商品编号
            "merchName": null,                          // 商品名
            "merchCount": null,                         // 商品数量
            "merchSpec": null,                          // 商品规格
            "unitPrice": null,                          // 单价
            "sellerName": null,                         // 卖家名
            "description": null,                        // 商品描述
            "picUrl": null,                             // 封面URL
            "albumPicUrl": [                            // 画册URL列表
                "123"
            ],
            "propertyList": [                           // 属性列表
                {
                    "firstValue": "净含量",
                    "secondValue": "1L"
                }
            ],
            "canShowMerchDetail": null                  // 是否可以跳转到详情页 1-可以查看 0-不可以查看
        }
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.order.OrderMerchSnapshotResponse"
    }
}

参数校验:
    只做必须验证
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

import unittest

from www.api.webservice import *
from www.common.database import select_one
from www.common.excel import wsData


class getOrderMerchSnapshot(unittest.TestCase):
    UserShop = wsData('TmlShop')
    Dealmager = wsData('DealMager')
    Merch1 = wsData('Merch1')
    Merch4 = wsData('Merch4')

    wsUserShop = webservice()
    wsUserShop.login(UserShop.username, UserShop.password)

    # S1.获取订单商品快照
    def test_getOrderMerchSnapshot_one(self):
        getSnapshot = self.wsUserShop.getOrderMerchSnapshot(orderNo=self.UserShop.orderCodWaitDeliver.orderNo, merchId=self.Merch1.goodsId)
        self.assertEqual(getSnapshot.model['success'], '0')
        self.assertSnapshot(getSnapshot, self.UserShop.orderCodWaitDeliver, merch=self.Merch1)

    # S2.订单有多个商品时获取商品快照

    # S3.订单商品不匹配时获取商品快照

    # S4.无商品快照时获取

    # S5.获取其他人的商品快照——获取成功
    def test_getOrderMerchSnapshot_other(self):
        getSnapshot = self.wsUserShop.getOrderMerchSnapshot(orderNo=self.Dealmager.orderNo, merchId=self.Merch4.goodsId)
        self.assertEqual(getSnapshot.model['success'], '0')
        self.assertSnapshot(getSnapshot, self.UserShop.orderCodWaitDeliver, merch=self.Merch4)


    def assertSnapshot(self, rsp, order, merch):
        orderSnapshot = select_one('select * from dlorder.dl_order_ordersnapshot where order_no = ?', order.orderNo)
        orderItem = select_one('select * from dlorder.dl_order_orderitem where order_no = ?', order.orderNo)
        self.assertEqual(rsp.model['merchSnapshot']['merchId'], orderSnapshot.merchandise_id)
        self.assertEqual(rsp.model['merchSnapshot']['merchNo'], merch.merchNo)
        self.assertEqual(rsp.model['merchSnapshot']['merchName'], merch.fullName)
        self.assertEqual(rsp.model['merchSnapshot']['merchCount'], str(orderItem.num))
        self.assertEqual(rsp.model['merchSnapshot']['merchSpec'], merch[u'包装规格'].encode('utf-8'))
        self.assertEqual(rsp.model['merchSnapshot']['unitPrice'], str(float(merch.unitPrice)/100))
        self.assertEqual(rsp.model['merchSnapshot']['sellerName'], merch.sellerName)
        self.assertEqual(rsp.model['merchSnapshot']['description'], '')
        self.assertEqual(rsp.model['merchSnapshot']['picUrl'], merch.picUrl)
        for i in range(0, len(rsp.model['merchSnapshot']['albumPicUrl'])):
            if i == 0:
                self.assertEqual(rsp.model['merchSnapshot']['albumPicUrl'][0], merch['detailPicUrl'])
            else :
                self.assertEqual(rsp.model['merchSnapshot']['albumPicUrl'][i], merch['detailPicUrl'+str(i+1)])

        for i in range(0, len(rsp.model['merchSnapshot']['propertyList'])):
            if rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '生产商':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'生产商'].decode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '净含量':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'净含量老'].encode('utf-8') + ' ' +merch[u'净含量单位'].encode('utf-8'))
            # elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '净含量单位':
            #     self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'], merch[u'净含量单位'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '保质期':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'保质期'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '包装规格':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'包装规格'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '酒精度':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'酒精度老'].encode('utf-8') + u' 度')
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '储藏方法':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'储藏方法'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '执行标准号':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'执行标准号'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '生产许可证编号':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'生产许可证编号'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '原料':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'原料'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '适用场景':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'适用场景'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '产地':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'产地'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '香型':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'香型'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '色泽':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'色泽'].encode('utf-8'))
            elif rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] == '商品类型':
                self.assertEqual(rsp.model['merchSnapshot']['propertyList'][i]['secondValue'].strip(), merch[u'商品类型'].encode('utf-8'))
            else :
                self.assertEqual(True,False,rsp.model['merchSnapshot']['propertyList'][i]['firstValue'] + " is not find in the excel!")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(getOrderMerchSnapshot("test_getOrderMerchSnapshot_one"))
    # suite.addTest(getOrderMerchSnapshot("test_getOrderMerchSnapshot_other"))
    return suite

