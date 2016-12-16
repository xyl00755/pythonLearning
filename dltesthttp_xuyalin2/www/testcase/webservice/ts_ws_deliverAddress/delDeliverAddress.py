#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0211.删除收货地址
http://127.0.0.1:8280/mallws/mydl/deliverAddress/delDeliverAddress.json
{
    "token":"3c9cc0e1da6c4a43b90cf866949f634e",                 // 必须
    "deliverAddressId":"7384e0a5c97c444eba162921ffac7838"       // 必须 收货地址id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                          // 成功 0-成功 1-未知失败 2-地址审批中，不能删除
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

class delDeliverAddress(unittest.TestCase):
    UserShop2 = wsData('TmlShop2')
    UserShopMin = wsData('TmlShopMin')
    UserShopMax = wsData('TmlShopMax')
    UserShop1 = wsData('TmlShop')

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

    # S1.正常删除收货地址
    def test_delDeliverAddress(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddress=select_one('select address_id from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)
        delDeliAddress=ws.delDeliverAddress(deliverAddressId=deliverAddress.address_id)
        self.assertEqual(delDeliAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'],[])

    # S2.删除审批中的收货地址
    def test_delDelilverAddress_approve(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        addressId_approve=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyAddress=ws.modifyDeliverAddress(addressId=addressId_approve,addressDetail='详细地址',areaProvinceCode=self.UserShop2.areaProvinceCode,areaCityCode=self.UserShop2.areaCityCode,
                                              areaDistrictCode='CHNP035C345D3001',zipCode='666666',deliverPerson='yx',deliverMobile='18495268591',deliverTel='028-85984568')
        delDeliAddress=ws.delDeliverAddress(deliverAddressId=addressId_approve)
        self.assertEqual(delDeliAddress.model['success'],'2')
        deliverAddressList_approve=ws.getDeliverAddressList()
        self.assertEqual(len(deliverAddressList_approve.model['deliverAddressModelList']),1)

    # S3.删除不存在的收货地址(接口返回500)
    def test_delDeliverAddress_notExist(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addressIdSql=select_one('select * from dlcompany.dl_biz_delivery_address where address_id=?','123456789')
        self.assertEqual(addressIdSql,None)
        delDeliverAddress=ws.delDeliverAddress(deliverAddressId=addressIdSql)
        self.assertEqual(delDeliverAddress.code,500)
        self.assertEqual(delDeliverAddress.model,None)

    # S4.删除其他用户的收货地址
    def test_delDeliverAddress_other(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        delDeliverAddress=ws.delDeliverAddress(deliverAddressId=self.UserShop1.addressId)
        self.assertEqual(delDeliverAddress.model['success'], '3')

    # S5.删除收货地址address_id位空(接口返回500)
    def test_delDeliverAddress_null(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        delDeliverAddress_null=ws.delDeliverAddress(deliverAddressId=None)
        self.assertEqual(delDeliverAddress_null.code,500)
        self.assertEqual(delDeliverAddress_null.model,None)

    # S6.删除收货地址token为空
    def test_DeliverAddress_tokenNull(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        deliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(deliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        delDeliverAddress_null=ws.delDeliverAddress(token='null',deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId'])
        self.assertEqual(delDeliverAddress_null.code,600)
        self.assertEqual(delDeliverAddress_null.model,None)

    # S7.删除收货地址token错误
    def test_DeliverAddress_tokenError(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        deliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(deliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        delDeliverAddress_null=ws.delDeliverAddress(token='123456789',deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId'])
        self.assertEqual(delDeliverAddress_null.code,100)
        self.assertEqual(delDeliverAddress_null.model,None)


    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

def suite():
        suite=unittest.TestSuite()
        suite.addTest(delDeliverAddress("test_delDeliverAddress"))
        suite.addTest(delDeliverAddress("test_delDelilverAddress_approve"))
        suite.addTest(delDeliverAddress("test_delDeliverAddress_notExist"))
        suite.addTest(delDeliverAddress("test_delDeliverAddress_other"))
        suite.addTest(delDeliverAddress("test_delDeliverAddress_null"))
        suite.addTest(delDeliverAddress("test_DeliverAddress_tokenNull"))
        suite.addTest(delDeliverAddress("test_DeliverAddress_tokenError"))
        return suite



