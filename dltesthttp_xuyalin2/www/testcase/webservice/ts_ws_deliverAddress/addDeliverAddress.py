#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *

"""
http://127.0.0.1:8280/mallws/mydl/deliverAddress/addDeliverAddress.json
	{
		"token":"19ff0bb9e96846979163df1bd02ccf53", // 必须
		"deliverAddress":{
			"areaProvinceCode": "P035",             // 必须 收货人省ID
			"areaCityCode": "C345",                 // 必须 收货人市ID
			"areaDistrictCode": "D3001",            // 必须 收货人区ID
			"addressDetail": "人生如剑2",           // 必须 详细地址
			"zipCode": "161616",                    // 可选 邮编
			"deliverPerson": "人生如剑2",           // 必须 收货人
			"deliverMobile": "13390006678",         // 必须 联系电话
			"deliverTel": "0123-456789012",         // 可选 固定电话 区号-电话号码 或 手机号码
			"isDefault": "0"                        // 必须 是否默认 0-默认 1非默认
		}
	}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0"                          // 成功 0-成功 1-待审批 2-未知失败
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.BaseResponse"
    }
}

参数校验:
    // 必须验证
    addressDetail           @NotNull        @Pattern(regexp = "\\w{1,420}")
    zipCode                 @Pattern(regexp = "\\w{1,10}")
    deliverPerson           @NotNull        @Pattern(regexp = "\\w{1,30}")
    deliverMobile           @NotNull        @Pattern(regexp = "[0-9]{1,30}")
    deliverTel              @Pattern(regexp = "([0-9]{1,6}-[0-9]{1,20})|([0-9]{1,30})")
    isDefault               @NotNull        @Pattern(regexp = "0|1")
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆

"""

class addDeliverAddress(unittest.TestCase):
    UserShop2 = wsData('TmlShop2')
    UserShopMin = wsData('TmlShopMin')
    UserShopMax = wsData('TmlShopMax')

    def setUp(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id=?',self.UserShop2.companyId)

    # S1.添加正确收货地址
    def test_addDliverAddress(self):
        ws = webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDelAddress = ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDelAddress.model['success'], '0')
        addDelAddressList=ws.getDeliverAddressList()
        self.assertAddDelAddrSuccess(addDelAddressList)

    # S2.添加最小收货地址
    def test_addDeliverAddress_min(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_min=ws.addDeliverAddress(areaProvinceCode=self.UserShop2.areaProvinceCode,areaCityCode=self.UserShop2.areaCityCode,areaDistrictCode=self.UserShop2.areaDistrictCode,
                                                   addressDetail=self.UserShopMin.deliverAddress,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShopMin.deliverPerson,deliverMobile=self.UserShop2.deliverMobile,
                                                   deliverTel=self.UserShop2.deliverTel,isDefault=self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress_min.model['success'],'0')
        addDelAddressList=ws.getDeliverAddressList()
        self.assertAddDelAddrSuccess(addDelAddressList)

    # S3.添加最大收获地址
    def test_addDeliverAddress_max(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_max=ws.addDeliverAddress(areaProvinceCode=self.UserShop2.areaProvinceCode,areaCityCode=self.UserShop2.areaCityCode,areaDistrictCode=self.UserShop2.areaDistrictCode,
                                                   addressDetail=self.UserShopMax.deliverAddress,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShopMax.deliverPerson,deliverMobile=self.UserShop2.deliverMobile,
                                                   deliverTel=self.UserShop2.deliverTel,isDefault=self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress_max.model['success'],'0')
        addDelAddressList=ws.getDeliverAddressList()
        self.assertAddDelAddrSuccess(addDelAddressList)


    # S4.添加待审批的收货地址(未找到待审批收货地址的数据表)
    def test_addDeliverAddress_approve(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_approve=ws.addDeliverAddress(areaProvinceCode=self.UserShop2.areaProvinceCode,areaCityCode=self.UserShop2.areaCityCode,areaDistrictCode='CHNP035C345D3001',
                                                   addressDetail=self.UserShop2.deliverAddress,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,deliverMobile=self.UserShop2.deliverMobile,
                                                   deliverTel=self.UserShop2.deliverTel,isDefault=self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress_approve.model['success'],'1')

    # S5.添加收货地址必填项为空(省市区为空)(接口返回code！=400，返回的code=500)
    def test_addDeliverAddress_null(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_null=ws.addDeliverAddress(areaProvinceCode='',areaCityCode='',areaDistrictCode='',
                                                   addressDetail=self.UserShop2.deliverAddress,zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson,deliverMobile=self.UserShop2.deliverMobile,
                                                   deliverTel=self.UserShop2.deliverTel,isDefault=self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress_null.model,None)
        self.assertEqual(addDeliverAddress_null.code,500)
        addDeliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'],[])

    # S6.添加收货地址必填项收货人、收货详细地址、联系电话为空(server端没有校验)
    def test_addDeliverAddress_nullMust(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDelAddressNullPerson = ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = '',deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDelAddressNullPerson.model['success'],'3')
        addDelAddressNullDetail = ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = '',zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDelAddressNullDetail.model['success'],'3')
        addDelAddressNullTel = ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = self.UserShop2.deliverPerson,deliverMobile = '',
                                             deliverTel = self.UserShop2.deliverTel,isDefault = self.UserShop2.isDefault)
        self.assertEqual(addDelAddressNullTel.model['success'],'3')

    # S7.添加收货人超过最大长度
    def test_addDeliverAddress_longPerson(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_longPerson=ws.addDeliverAddress(areaProvinceCode=self.UserShop2.areaProvinceCode,areaCityCode=self.UserShop2.areaCityCode,areaDistrictCode=self.UserShop2.areaDistrictCode,
                                                   addressDetail=self.UserShop2.deliverAddress,zipCode=self.UserShop2.zipCode,deliverPerson='收货人收货人收货人收货',
                                                   deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel,isDefault=self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress_longPerson.model['success'],'3')
        addDeliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'],[])

    # S8.添加收货详细地址超过最大长度
    def test_addDeliverAddress_longAddress(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_longAddress=ws.addDeliverAddress(areaProvinceCode=self.UserShop2.areaProvinceCode,areaCityCode=self.UserShop2.areaCityCode,areaDistrictCode=self.UserShop2.areaDistrictCode,
                                                   addressDetail='联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空'
                                                                 '联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空联系电话为空空',
                                                   zipCode=self.UserShop2.zipCode,deliverPerson=self.UserShop2.deliverPerson, deliverMobile=self.UserShop2.deliverMobile,deliverTel=self.UserShop2.deliverTel,isDefault=self.UserShop2.isDefault)
        self.assertEqual(addDeliverAddress_longAddress.model['success'],'3')
        addDeliverAddressList=ws.getDeliverAddressList()
        self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'],[])

    # S9.添加第一个收货地址为默认地址，第二个收货地址为非默认地址
    def test_addDeliverAddress_default(self):
        ws=webservice()
        ws.login(self.UserShop2.username,self.UserShop2.password)
        addDeliverAddress_default=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = '默认收货地址',deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = '0')
        self.assertEqual(addDeliverAddress_default.model['success'],'0')
        addDeliverAddress_noDefault=ws.addDeliverAddress(areaProvinceCode = self.UserShop2.areaProvinceCode,areaCityCode = self.UserShop2.areaCityCode,areaDistrictCode = self.UserShop2.areaDistrictCode,
                                             addressDetail = self.UserShop2.deliverAddress,zipCode = self.UserShop2.zipCode,deliverPerson = '非默认收货地址',deliverMobile = self.UserShop2.deliverMobile,
                                             deliverTel = self.UserShop2.deliverTel,isDefault = '1')
        self.assertEqual(addDeliverAddress_noDefault.model['success'],'0')
        addDeliverAddressList=ws.getDeliverAddressList()
        if(addDeliverAddressList.model['deliverAddressModelList'][0]['deliverPerson']=='默认收货地址'):
            self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'][0]['isDefault'],'0')
            self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'][1]['isDefault'],'1')
        elif(addDeliverAddressList.model['deliverAddressModelList'][0]['deliverPerson']=='非默认收货地址'):
            self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'][0]['isDefault'],'1')
            self.assertEqual(addDeliverAddressList.model['deliverAddressModelList'][1]['isDefault'],'0')


    #验证添加收货地址是否成功
    def assertAddDelAddrSuccess(self,rsp):
        addressId_sql=select_one('select address_id from dlcompany.dl_biz_delivery_address where company_id = ?',self.UserShop2.companyId)
        addressId=rsp.model['deliverAddressModelList'][0]['addressId']
        self.assertEqual(addressId,addressId_sql.address_id)

    def tearDown(self):
        update('delete from dlcompany.dl_biz_delivery_address where company_id = ?', self.UserShop2.companyId)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(addDeliverAddress("test_addDliverAddress"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_min"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_max"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_approve"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_null"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_nullMust"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_longPerson"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_longAddress"))
    suite.addTest(addDeliverAddress("test_addDeliverAddress_default"))
    return suite
