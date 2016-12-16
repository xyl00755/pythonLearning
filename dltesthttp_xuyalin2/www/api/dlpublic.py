#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlpublic:
    def __init__(self):
        # 从配置文件中读取接口服务器IP、域名，端口
        from www.common.config import config
        httpConfig = config().confighttp
        self.dlpublichost = httpConfig['dlpublichost']
        self.dlpublicport = httpConfig['dlpublicport']

    def area(self,areaParentCode):
        #GET /area/?area_parent_code={省市区编码}
        url = 'http://' + self.dlpublichost + ':' + str(self.dlpublicport) + '/area/'
        data = {'area_parent_code':areaParentCode}
        response = requests.get(url,params=data)
        res=json.loads(response.content)
        return res

    def data(self):
        #GET /data/?data_code_path=SELLER_TYPE/S01
        url = 'http://' + self.dlpublichost + ':' + str(self.dlpublicport) + '/data/'
        data = {'data_code_path':'SELLER_TYPE/S01'}
        response = requests.get(url,params=data)
        res=json.loads(response.content)
        return res