#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import unittest

from www.api.webservice import *
from www.common.database import *
from www.common.excel import *
from www.common.model import *

'''
0233.比较应用版本信息
http://127.0.0.1:8280/mallws/common/version/compareAppVersion.json
{
    "token":"117f6b5886714107a9c7bcb6d4556f64",     // 必须
    "clientVersion":"1.2.3",                        // 必须 客户端版本号
    "osCode":"0",                                   // 必须 操作系统类型 0-安卓 1-苹果
    "equipmentCode":"0",                            // 必须 设备类型 0-phone 1-pad
    "appType":"0"                                   // 必须 应用类型 0-终端店 1-经销商 2-配送员
}

{
    "code": 200,
    "description": "执行成功!",
    "model": {
        "success": "0",                                 // 成功 0-成功 1-无此类型应用信息
        "clientObsoleted": "0",                         // 客户端是否过时 0-未过时 1-过时
        "latestVersion": "1.0.0",                       // 当前最新版本号
        "downloadUrl": "http://172.16.75.203:88//2015/08/19/15/22/1439968930782.apk

",   // 当前最新版本下载地址
        "forceUpgrade": "1"                             // 是否强制升级 0-不强制 1-强制
    },
    "metadata": {
        "type": 0,
        "clazz": "cn.com.hd.mall.web.webservices.entity.response.mydl.version.AppVersionCompareResponse"
    }
}

参数校验:
    // 只做必须校验
code说明:
    100-token失效 200-成功 300-错误的角色(无权限) 400-非法的参数 500-服务器异常 600-重新登陆

'''


class compareAppVersion(unittest.TestCase):


    def setUp(self):
        # 清空升级配置表
        update('delete from danlu_cd_database.t_app_version_management')

    # S1.未配置任何升级版本，验证接口不会提示需要升级
    def test_compver_Null(self):
        # 安卓终端店
        cvNullShopAnd = webservice().compareAppVersion('1.0.0', '0', '0', '0')
        self.assertCompverSuccess(cvNullShopAnd, success = '1')

        # iOS终端店
        cvNullShopIos = webservice().compareAppVersion('1.0.0', '1', '0', '0')
        self.assertCompverSuccess(cvNullShopIos, success = '1')

        # 安卓经销商
        cvNullDealAnd = webservice().compareAppVersion('1.0.0', '0', '0', '1')
        self.assertCompverSuccess(cvNullDealAnd, success = '1')

        # iOS经销商
        cvNullDealIos = webservice().compareAppVersion('1.0.0', '1', '0', '1')
        self.assertCompverSuccess(cvNullDealIos, success = '1')



    # S2.当前已是最新版本，验证接口不会提示需要升级
    def test_compver_Under(self):
        # 插入版本为低版本


        verUnderShopAnd = AppVersion(id = 'verUnderShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '1.0.0', is_force_upgrade = '1', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUnderShopAnd.insert()
        verUnderShopIos = AppVersion(id = 'verUnderShopIos',
                                  version = '1.0.000', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUnderShopIos.insert()
        verUnderDealAnd = AppVersion(id = 'verUnderDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '1.0.0', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUnderDealAnd.insert()
        verUnderDealIos = AppVersion(id = 'verUnderDealIos', app_download_address = '',
                                  version = '1.0.000', is_force_upgrade = '1', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUnderDealIos.insert()


        # 安卓终端店
        cvUnderShopAnd = webservice().compareAppVersion('1.0.1', '0', '0', '0')
        self.assertCompverSuccess(cvUnderShopAnd, clientObsoleted='0', latestVersion='1.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='1')

        # iOS终端店
        cvUnderShopIos = webservice().compareAppVersion('1.1.000', '1', '0', '0')
        self.assertCompverSuccess(cvUnderShopIos, clientObsoleted='0', latestVersion='1.0.000', forceUpgrade='0')

        # 安卓经销商
        cvUnderDealAnd = webservice().compareAppVersion('2.0.0', '0', '0', '1')
        self.assertCompverSuccess(cvUnderDealAnd, clientObsoleted='0', latestVersion='1.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='0')

        # iOS经销商
        cvUnderDealIos = webservice().compareAppVersion('2.0.100', '1', '0', '1')
        self.assertCompverSuccess(cvUnderDealIos, clientObsoleted='0', latestVersion='1.0.000', forceUpgrade='1')



    # S3.非强制升级提示
    def test_compver_Up(self):
        # 插入版本为非强制版本


        verUpShopAnd = AppVersion(id = 'verUpShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '3.0.0', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopAnd.insert()
        verUpShopIos = AppVersion(id = 'verUpShopIos',
                                  version = '3.0.100', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopIos.insert()
        verUpDealAnd = AppVersion(id = 'verUpDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '3.0.1', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpDealAnd.insert()
        verUpDealIos = AppVersion(id = 'verUpDealIos', app_download_address = '',
                                  version = '3.1.000', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpDealIos.insert()


        # 安卓终端店
        cvUpShopAnd = webservice().compareAppVersion('1.0.1', '0', '0', '0')
        self.assertCompverSuccess(cvUpShopAnd, clientObsoleted='1', latestVersion='3.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='0')

        # iOS终端店
        cvUpShopIos = webservice().compareAppVersion('1.1.000', '1', '0', '0')
        self.assertCompverSuccess(cvUpShopIos, clientObsoleted='1', latestVersion='3.0.100', forceUpgrade='0')

        # 安卓经销商
        cvUpDealAnd = webservice().compareAppVersion('2.0.0', '0', '0', '1')
        self.assertCompverSuccess(cvUpDealAnd, clientObsoleted='1', latestVersion='3.0.1', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='0')

        # iOS经销商
        cvUpDealIos = webservice().compareAppVersion('2.0.100', '1', '0', '1')
        self.assertCompverSuccess(cvUpDealIos, clientObsoleted='1', latestVersion='3.1.000', forceUpgrade='0')



    # S4.强制升级提示
    def test_compver_Upf(self):
        # 插入版本为强制版本


        verUpfShopAnd = AppVersion(id = 'verUpfShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '4.0.0', is_force_upgrade = '1', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpfShopAnd.insert()
        verUpfShopIos = AppVersion(id = 'verUpfShopIos',
                                  version = '4.0.100', is_force_upgrade = '1', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpfShopIos.insert()
        verUpfDealAnd = AppVersion(id = 'verUpfDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '4.0.1', is_force_upgrade = '1', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpfDealAnd.insert()
        verUpfDealIos = AppVersion(id = 'verUpfDealIos', app_download_address = '',
                                  version = '4.1.000', is_force_upgrade = '1', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpfDealIos.insert()


        # 安卓终端店
        cvUpfShopAnd = webservice().compareAppVersion('3.2.1', '0', '0', '0')
        self.assertCompverSuccess(cvUpfShopAnd, clientObsoleted='1', latestVersion='4.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='1')

        # iOS终端店
        cvUpfShopIos = webservice().compareAppVersion('3.2.100', '1', '0', '0')
        self.assertCompverSuccess(cvUpfShopIos, clientObsoleted='1', latestVersion='4.0.100', forceUpgrade='1')

        # 安卓经销商
        cvUpfDealAnd = webservice().compareAppVersion('3.2.0', '0', '0', '1')
        self.assertCompverSuccess(cvUpfDealAnd, clientObsoleted='1', latestVersion='4.0.1', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='1')

        # iOS经销商
        cvUpfDealIos = webservice().compareAppVersion('3.2.100', '1', '0', '1')
        self.assertCompverSuccess(cvUpfDealIos, clientObsoleted='1', latestVersion='4.1.000', forceUpgrade='1')



    # S5.非强制跨版本升级提示
    def test_compver_Upk(self):
        # 插入版本
        verUpShopAnd = AppVersion(id = 'verUpShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '3.0.0', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopAnd.insert()
        verUpShopIos = AppVersion(id = 'verUpShopIos',
                                  version = '3.0.100', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopIos.insert()
        verUpDealAnd = AppVersion(id = 'verUpDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '3.0.1', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpDealAnd.insert()
        verUpDealIos = AppVersion(id = 'verUpDealIos', app_download_address = '',
                                  version = '3.1.000', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpDealIos.insert()

        verUpfShopAnd = AppVersion(id = 'verUpfShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '4.0.0', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpfShopAnd.insert()
        verUpfShopIos = AppVersion(id = 'verUpfShopIos',
                                  version = '4.0.100', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpfShopIos.insert()
        verUpfDealAnd = AppVersion(id = 'verUpfDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '4.0.1', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpfDealAnd.insert()
        verUpfDealIos = AppVersion(id = 'verUpfDealIos', app_download_address = '',
                                  version = '4.1.000', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpfDealIos.insert()


        # 安卓终端店
        cvUpfShopAnd = webservice().compareAppVersion('1.2.1', '0', '0', '0')
        self.assertCompverSuccess(cvUpfShopAnd, clientObsoleted='1', latestVersion='4.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='0')

        # iOS终端店
        cvUpfShopIos = webservice().compareAppVersion('1.2.100', '1', '0', '0')
        self.assertCompverSuccess(cvUpfShopIos, clientObsoleted='1', latestVersion='4.0.100', forceUpgrade='0')

        # 安卓经销商
        cvUpfDealAnd = webservice().compareAppVersion('1.2.0', '0', '0', '1')
        self.assertCompverSuccess(cvUpfDealAnd, clientObsoleted='1', latestVersion='4.0.1', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='0')

        # iOS经销商
        cvUpfDealIos = webservice().compareAppVersion('1.2.100', '1', '0', '1')
        self.assertCompverSuccess(cvUpfDealIos, clientObsoleted='1', latestVersion='4.1.000', forceUpgrade='0')



    # S6.强制跨版本升级提示
    def test_compver_Upfk(self):
        # 插入版本
        verUpShopAnd = AppVersion(id = 'verUpShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '3.0.0', is_force_upgrade = '1', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopAnd.insert()
        verUpShopIos = AppVersion(id = 'verUpShopIos',
                                  version = '3.0.100', is_force_upgrade = '1', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopIos.insert()
        verUpDealAnd = AppVersion(id = 'verUpDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '3.0.1', is_force_upgrade = '1', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpDealAnd.insert()
        verUpDealIos = AppVersion(id = 'verUpDealIos', app_download_address = '',
                                  version = '3.1.000', is_force_upgrade = '1', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpDealIos.insert()

        verUpfShopAnd = AppVersion(id = 'verUpfShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '4.0.0', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpfShopAnd.insert()
        verUpfShopIos = AppVersion(id = 'verUpfShopIos',
                                  version = '4.0.100', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpfShopIos.insert()
        verUpfDealAnd = AppVersion(id = 'verUpfDealAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_dealer.apk',
                                  version = '4.0.1', is_force_upgrade = '0', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpfDealAnd.insert()
        verUpfDealIos = AppVersion(id = 'verUpfDealIos', app_download_address = '',
                                  version = '4.1.000', is_force_upgrade = '0', os_code = '1', os_name = 'ios', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '1')
        verUpfDealIos.insert()


        # 安卓终端店
        cvUpfShopAnd = webservice().compareAppVersion('1.2.1', '0', '0', '0')
        self.assertCompverSuccess(cvUpfShopAnd, clientObsoleted='1', latestVersion='4.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='1')

        # iOS终端店
        cvUpfShopIos = webservice().compareAppVersion('1.2.100', '1', '0', '0')
        self.assertCompverSuccess(cvUpfShopIos, clientObsoleted='1', latestVersion='4.0.100', forceUpgrade='1')

        # 安卓经销商
        cvUpfDealAnd = webservice().compareAppVersion('1.2.0', '0', '0', '1')
        self.assertCompverSuccess(cvUpfDealAnd, clientObsoleted='1', latestVersion='4.0.1', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='1')

        # iOS经销商
        cvUpfDealIos = webservice().compareAppVersion('1.2.100', '1', '0', '1')
        self.assertCompverSuccess(cvUpfDealIos, clientObsoleted='1', latestVersion='4.1.000', forceUpgrade='1')


    # S7.带token时升级
    def test_compver_Upt(self):
        UserShop = wsData('TmlShop')
        verUpShopAnd = AppVersion(id = 'verUpShopAnd', app_download_address = 'http://asset.danlu.com/mobile/client/android/danlu_store.apk',
                                  version = '3.0.0', is_force_upgrade = '1', os_code = '0', os_name = 'android', equipment_code = '0', equipment_name = 'phone',
                                  created_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_type = '0')
        verUpShopAnd.insert()
        dl = webservice().login(UserShop.username, UserShop.password)
        cvtoken = webservice().compareAppVersion('0.0.1', '0', '0', '0', dl['model']['token'])
        self.assertCompverSuccess(cvtoken, clientObsoleted='1', latestVersion='3.0.0', downloadUrl='http://asset.danlu.com/mobile/client/android/danlu_store.apk ', forceUpgrade='1')

    def tearDown(self):
        # 清空升级配置表
        update('delete from danlu_cd_database.t_app_version_management')

    def assertCompverSuccess(self, rsp, code = 200, success = '0', clientObsoleted = None, latestVersion = None,  downloadUrl = None, forceUpgrade = None):
        self.assertEqual(rsp.code, code)
        self.assertEqual(rsp.model['success'], success)
        self.assertEqual(rsp.model['clientObsoleted'], clientObsoleted)
        self.assertEqual(rsp.model['latestVersion'], latestVersion)
        self.assertEqual(rsp.model['latestVersion'], latestVersion)
        self.assertEqual(rsp.model['forceUpgrade'], forceUpgrade)


def suite():
    suite = unittest.TestSuite()
    # 7
    suite.addTest(compareAppVersion("test_compver_Null"))
    suite.addTest(compareAppVersion("test_compver_Under"))
    suite.addTest(compareAppVersion("test_compver_Up"))
    suite.addTest(compareAppVersion("test_compver_Upf"))
    suite.addTest(compareAppVersion("test_compver_Upk"))
    suite.addTest(compareAppVersion("test_compver_Upfk"))
    suite.addTest(compareAppVersion("test_compver_Upt"))
    return suite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main(defaultTest = 'ts_ws_version_compareAppVersion')