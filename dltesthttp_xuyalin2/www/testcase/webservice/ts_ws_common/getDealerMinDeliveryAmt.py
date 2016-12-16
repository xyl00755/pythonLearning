#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest
from www.api.webservice import *
from www.common.excel import wsData
from www.common.database import *

"""
common_param_02.获取经销商最低配送金额
http://127.0.0.1:8280/mallws/common/param/getDealerMinDeliveryAmt.json
{
    "token":"123",                       // 必须
	"dealerId":[						 // 经销商companyId
		"e54d8c0d993543558062e52195c5c8d4",
		"e54d8c0d993543558062e52195c5c8d3"
	]
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
		"success": "0",                  //0-成功  1-失败
        "dealerMinDeliveryAmtModel":[
			{
				"dealerId":"e54d8c0d993543558062e52195c5c8d4",		// 经销商companyId
				"minDeliveryAmt":"1200"								// 最小起送金额
			}
		]
    },
     "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.shoppingcart.DealerMinDeliveryAmtResponse"
    }
}

"""
class getDealerMinDeliveryAmt(unittest.TestCase):
    UserShop1 = wsData('TmlShop')
    UserShop2 = wsData('DealMager')
    UserShop3 = wsData('DealMager2')

    #正确获取一个经销商的起送金额
    def test_getDealerMinDeliveryAmt_oneDealer(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[self.UserShop2.companyId])
        self.assertEqual(getAmt.model['success'],'0')
        getAmtSql=select_one('select * from dlcompany.dl_biz_base_info where company_id=?',self.UserShop2.companyId)
        self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][0]['minDeliveryAmt'],str(getAmtSql.delivery_amount))

    #正确获取两个经销商的起送金额
    def test_getDealerMinDeliveryAmt_twoDealer(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[self.UserShop2.companyId,self.UserShop3.companyId])
        self.assertEqual(getAmt.model['success'],'0')
        getAmtSqlOne=select_one('select * from dlcompany.dl_biz_base_info where company_id=?',self.UserShop2.companyId)
        getAmtSqlTwo=select_one('select * from dlcompany.dl_biz_base_info where company_id=?',self.UserShop3.companyId)
        for i in range(0,2):
            if getAmt.model['dealerMinDeliveryAmtModel'][i]['dealerId']==self.UserShop2.companyId:
                self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][i]['minDeliveryAmt'],str(getAmtSqlOne.delivery_amount))
            else:
                self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][i]['minDeliveryAmt'],str(getAmtSqlTwo.delivery_amount))

    #一个经销商打开起送金额开关，一个关闭起送金额开关
    def test_getDealerMinDeliveryAmt_oneOpneOneClose(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        update('update dlcompany.dl_biz_base_info set delivery_amount_flg=? where company_id=?',0,self.UserShop2.companyId)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[self.UserShop2.companyId,self.UserShop3.companyId])
        self.assertEqual(getAmt.model['success'],'0')
        getAmtSqlTwo=select_one('select * from dlcompany.dl_biz_base_info where company_id=?',self.UserShop3.companyId)
        for i in range(0,2):
            if getAmt.model['dealerMinDeliveryAmtModel'][i]['dealerId']==self.UserShop2.companyId:
                self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][i]['minDeliveryAmt'],None)
            else:
                self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][i]['minDeliveryAmt'],str(getAmtSqlTwo.delivery_amount))
        update('update dlcompany.dl_biz_base_info set delivery_amount_flg=? where company_id=?',1,self.UserShop2.companyId)

    #dealerId为空
    def test_getDealerMinDeliveryAmt_dealerIdNull(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[])
        self.assertEqual(getAmt.model['success'],'1')
        self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'],None)

    #dealerId不存在
    def test_getDealerMinDeliveryAmt_dealerIdNotExist(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=['1234567890'])
        self.assertEqual(getAmt.model['success'],'0')
        self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'],[])

    #dealerId为空字符串
    def test_getDealerMinDeliveryAmt_dealerIDNone(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[''])
        self.assertEqual(getAmt.model['success'],'0')
        self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'],[])

    #经销商开启起送金额开关且金额为空
    def test_getDealerMinDeliveryAmt_openAmtNull(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        update('update dlcompany.dl_biz_base_info set delivery_amount=? where company_id=?',None,self.UserShop2.companyId)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[self.UserShop2.companyId])
        self.assertEqual(getAmt.model['success'],'0')
        self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][0]['minDeliveryAmt'],None)
        update('update dlcompany.dl_biz_base_info set delivery_amount=? where company_id=?',3400,self.UserShop2.companyId)

    #经销商设置起送金额的开关关闭
    def test_getDealerMinDeliveryAmt_close(self):
        ws=webservice()
        ws.login(self.UserShop1.username,self.UserShop1.password)
        update('update dlcompany.dl_biz_base_info set delivery_amount_flg=? where company_id=?',0,self.UserShop2.companyId)
        getAmt=ws.getDealerMinDeliveryAmt(dealerId=[self.UserShop2.companyId])
        self.assertEqual(getAmt.model['success'],'0')
        self.assertEqual(getAmt.model['dealerMinDeliveryAmtModel'][0]['minDeliveryAmt'],None)
        update('update dlcompany.dl_biz_base_info set delivery_amount_flg=? where company_id=?',1,self.UserShop2.companyId)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_oneDealer"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_twoDealer"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_oneOpneOneClose"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_dealerIdNull"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_dealerIdNotExist"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_dealerIDNone"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_openAmtNull"))
    suite.addTest(getDealerMinDeliveryAmt("test_getDealerMinDeliveryAmt_close"))
    return suite




