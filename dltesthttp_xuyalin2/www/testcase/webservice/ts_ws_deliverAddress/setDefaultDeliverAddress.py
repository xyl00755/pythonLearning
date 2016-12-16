#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
0213.设置默认收货地址
http://127.0.0.1:8280/mallws/mydl/deliverAddress/setDefaultDeliverAddress.json
{
    "token":"19ff0bb9e96846979163df1bd02ccf53",             // 必须
    "deliverAddressId":"d79b18b477d34ad3b356ef8cdbd4858b"   // 必须 收货地址id
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-未知失败 2-地址不存在
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

class setDefaultDeliverAddress(unittest.TestCase):
    UserShop1 = wsData('TmlShop')
    UserShop2 = wsData('TmlShop2')

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

    # S1.设置收货地址为默认收货地址
    def test_setDefaultDeliverAddress(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        setDefaultAddress=ws.setDefaultDeliverAddress(deliverAddressId=deliAddressId)
        self.assertEqual(setDefaultAddress.model['success'],'0')
        deliverAddressListDefault=ws.getDeliverAddressList()
        self.assertEqual(deliverAddressListDefault.model['deliverAddressModelList'][0]['isDefault'],'0')

    # S2.设置不存在的收货地址为默认地址（接口返回500）
    def test_setDefaultDeliverAddress_notExist(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        setDefDeliverAddress=ws.setDefaultDeliverAddress(deliverAddressId='123456789')
        self.assertEqual(setDefDeliverAddress.code,500)
        self.assertEqual(setDefDeliverAddress.model,None)

    # S3.设置addressID为空的收货地址为默认地址（接口返回500）
    def test_setDefaultDeliverAddress_null(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        setDefDeliverAddress=ws.setDefaultDeliverAddress(deliverAddressId='')
        self.assertEqual(setDefDeliverAddress.code,500)
        self.assertEqual(setDefDeliverAddress.model,None)

    # S4.设置其他人的收货地址为默认地址（接口返回500）已提交Bug错误 #5542
    def test_setDefaultDeliverAddress_other(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        setDefDeliverAddress=ws.setDefaultDeliverAddress(deliverAddressId=self.UserShop1.addressId)
        self.assertEqual(setDefDeliverAddress.model['success'],'2')

    # S5.已设置默认的收货地址再设置其他收货地址为默认地址
    def test_setDefaultDeliverAddress_repeat(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress1=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = '详细地址1',zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress1.model['success'],'0')
        addressIdSql1=select_one('select address_id from dlcompany.dl_biz_delivery_address where address_detail=?','详细地址1')
        deliverAddressId1=addressIdSql1.address_id
        addDeliverAddress2=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = '详细地址2',zipCode = self.UserShop2.zipCode,deliverPerson = 'testsun',deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress2.model['success'],'0')
        addressIdSql2=select_one('select address_id from dlcompany.dl_biz_delivery_address where address_detail=?','详细地址2')
        deliverAddressId2=addressIdSql2.address_id
        setDefaultDeliverAddress_result=ws.setDefaultDeliverAddress(deliverAddressId=deliverAddressId1)
        self.assertEqual(setDefaultDeliverAddress_result.model['success'],'0')
        deliverAddressDefault1=select_one('select is_default from dlcompany.dl_biz_delivery_address where address_id=?',deliverAddressId1)
        self.assertEqual(deliverAddressDefault1.is_default,'1')
        deliverAddressDefault2=select_one('select is_default from dlcompany.dl_biz_delivery_address where address_id=?',deliverAddressId2)
        self.assertEqual(deliverAddressDefault2.is_default,'0')
        setDefaultDeliverAddress_result1=ws.setDefaultDeliverAddress(deliverAddressId=deliverAddressId2)
        self.assertEqual(setDefaultDeliverAddress_result1.model['success'],'0')
        deliverAddressDefault11=select_one('select is_default from dlcompany.dl_biz_delivery_address where address_id=?',deliverAddressId1)
        self.assertEqual(deliverAddressDefault11.is_default,'0')
        deliverAddressDefault22=select_one('select is_default from dlcompany.dl_biz_delivery_address where address_id=?',deliverAddressId2)
        self.assertEqual(deliverAddressDefault22.is_default,'1')

    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(setDefaultDeliverAddress("test_setDefaultDeliverAddress"))
    suite.addTest(setDefaultDeliverAddress("test_setDefaultDeliverAddress_notExist"))
    suite.addTest(setDefaultDeliverAddress("test_setDefaultDeliverAddress_null"))
    suite.addTest(setDefaultDeliverAddress("test_setDefaultDeliverAddress_other"))
    suite.addTest(setDefaultDeliverAddress("test_setDefaultDeliverAddress_repeat"))
    return suite