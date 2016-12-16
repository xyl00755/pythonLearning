#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *


"""
0212.修改收货地址
http://127.0.0.1:8280/mallws/mydl/deliverAddress/modifyDeliverAddress.json
{
    "token":"19ff0bb9e96846979163df1bd02ccf53",             // 必须
    "deliverAddress":{
        "addressId": "d79b18b477d34ad3b356ef8cdbd4858b",    // 原来是什么填什么
        "addressDetail": "人生如剑_Helo_Helo",              // 可选修改
        "areaProvinceCode": "P014",                         // 可选修改
        "areaCityCode": "C124",                             // 可选修改
        "areaDistrictCode": "D1179",                        // 可选修改
        "zipCode": "161616",                                // 可选修改
        "deliverPerson": "人生如剑",                        // 可选修改
        "deliverMobile": "13390006678",                     // 可选修改
        "deliverTel": "0123-456789012"                      // 可选修改
    }
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                                      // 成功 0-成功 1-待审批 2-未知失败 3-地址不存在
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 必须验证
    addressDetail           @Pattern(regexp = "\\w{1,420}")
    zipCode                 @Pattern(regexp = "\\w{1,10}")
    deliverPerson           @Pattern(regexp = "\\w{1,30}")
    deliverMobile           @Pattern(regexp = "[0-9]{1,30}")
    deliverTel              @Pattern(regexp = "([0-9]{1,6}-[0-9]{1,20})|([0-9]{1,30})")
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆
"""

class modifyDeliverAddress(unittest.TestCase):

    UserShop2 = wsData('TmlShop2')
    UserShopMin = wsData('TmlShopMin')
    UserShopMax = wsData('TmlShopMax')
    UserShop1 = wsData('TmlShop')

    def setUp(self):
         update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

    # S1.修改收货地址的详细地址以及联系人
    def test_modifyDeliverAddress(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = '详细地址是成都市环球中心',zipCode = self.UserShop2.zipCode,deliverPerson = 'yuxixi',deliverMobile = '18495685974',
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddress=ws.getDeliverAddressList()
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddress.model['deliverAddressModelList'][0]['addressId'],addressDetail=self.UserShop2.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['addressDetail'],self.UserShop2.deliverAddress)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['deliverPerson'],self.UserShop2.deliverPerson)
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['deliverMobile'],self.UserShop2.deliverMobile)

    # S2.修改收货地址为审批中地址
    def test_modifyDeliverAddress_approve(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddress=ws.getDeliverAddressList()
        deliverAddressId=deliverAddress.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail=self.UserShop2.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = 'CHNP035C345D3001',zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.model['success'],'1')
        deliverAddress_applyId=select_one('select apply_id from dlcompany.dl_biz_delivery_address where address_id=?',deliverAddressId)
        self.assertNotEqual(deliverAddress_applyId,None)

    # S3.修改收货地址address_id不存在
    def test_modifyDeliverAddress_notExist(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        modifyDeliAddress=ws.modifyDeliverAddress(addressId='123456789',addressDetail=self.UserShop2.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.code,500)
        self.assertEqual(modifyDeliAddress.model,None)

    # S4.修改其他用户的收货地址(已提bug错误 #5542)
    def test_modifyDeliverAddress_other(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        modifyDeliAddress=ws.modifyDeliverAddress(addressId='6d23ae6420d84ad68fd4c1267e65db34',addressDetail=self.UserShop2.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.code,500)
        self.assertEqual(modifyDeliAddress.model,None)

    # S5.修改收货地址详细地址为空
    def test_modifyDeliverAddress_addressNull(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail='',areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.model['success'], '0')
        deliverAddressList=ws.getDeliverAddressList()
        # 验证addressDetail并未被置空
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['addressDetail'], self.UserShop2.deliverAddress)

    # S6.修改收货地址收货人为空
    def test_modifyDeliverAddress_personNull(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail=self.UserShop2.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson='',
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.model['success'], '0')
        deliverAddressList=ws.getDeliverAddressList()
        # 验证addressDetail并未被置空
        self.assertEqual(deliverAddressList.model['deliverAddressModelList'][0]['deliverPerson'], self.UserShop2.deliverPerson)

    # S7.修改收货地址各个属性值最小
    def test_modifyDeliverAddress_min(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail=self.UserShopMin.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShopMin.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.model['success'],'0')

    # S8.修改收货地址各个属性值最大
    def test_modifyDeliverAddress_max(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail=self.UserShopMax.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShopMax.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.model['success'],'0')

    # S9.修改收货地址收货人超过最大长度
    def test_modifyDeliverAddress_longPerson(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail=self.UserShop2.deliverAddress,areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson='收货人收货人收货人收货人收货人收货人收货人收货人收货人收货人收货人收货人',
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.code,500)
        self.assertEqual(modifyDeliAddress.model,None)

    # S10.修改收货地址详细地址超过最大长度
    def test_modifyDeliverAddress_longAddress(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress.model['success'],'0')
        deliverAddressList=ws.getDeliverAddressList()
        deliverAddressId=deliverAddressList.model['deliverAddressModelList'][0]['addressId']
        modifyDeliAddress=ws.modifyDeliverAddress(addressId=deliverAddressId,addressDetail='联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空空',areaProvinceCode = self.UserShop2.areaProvinceCode,
                                                  areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode =self.UserShop2.areaDistrictCode,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,
                                                  deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel)
        self.assertEqual(modifyDeliAddress.code,500)
        self.assertEqual(modifyDeliAddress.model,None)

    def tearDown(self):
         update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_approve"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_notExist"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_other"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_addressNull"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_personNull"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_min"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_max"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_longPerson"))
    suite.addTest(modifyDeliverAddress("test_modifyDeliverAddress_longAddress"))
    return suite


