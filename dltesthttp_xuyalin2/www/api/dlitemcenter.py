#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlitemcenter:
    def __init__(self,ini_file='../../config/http_config.ini'):
        # 从配置文件中读取接口服务器IP、域名，端口
        config = configparser.ConfigParser()
        config.read(ini_file)
        self.dlitemcenterhost = config['HTTP']['dlitemcenterhost']
        self.dlitemcenterport = config['HTTP']['dlitemcenterport']

    #POST请求，根据指定的查询条件获取相应的产品信息列表
    def getProductList(self,data):
        url = 'http://' + self.dlitemcenterhost + ':' + str(self.dlitemcenterport) + '/center/products/v1/productList'
        headers = {'X-ApiVersion':'1.0'}
        response = requests.post(url,headers=headers,json=data)
        response.connection.close()
        return response

    #GET请求，通过商品id获取产品主表信息
    def getProduct(self,id):
        #GET /center/products/v1/goods/{id}/product
        url = 'http://' + self.dlitemcenterhost + ':' + str(self.dlitemcenterport) + '/center/products/v1/goods/' + id + '/product'
        headers = {'X-ApiVersion':'1.0'}
        response = requests.get(url,headers=headers)
        response.connection.close()
        return response

    #GET请求，获取产品对应的类目信息
    def getCategoryinfo_by_productcodes(self,data):
        url = 'http://' + self.dlitemcenterhost + ':' + str(self.dlitemcenterport) + '/center/products/v1/category/categoryinfo_by_productcodes'+"?"+data
        headers = {'X-ApiVersion':'1.0'}
        response = requests.get(url,headers=headers)
        response.connection.close()
        return response

    #GET请求，获取产品对应的类目信息
    def getBrandinfo(self,data):
        url = 'http://' + self.dlitemcenterhost + ':' + str(self.dlitemcenterport) + '/center/products/v1/brand/brandinfo'+"?"+data
        headers = {'X-ApiVersion':'1.0'}
        response = requests.get(url,headers=headers)
        response.connection.close()
        return response

    #POST请求，获取商品和业务员信息
    def getGoodsDetail(self,data):
        url = 'http://' + self.dlitemcenterhost + ':' + str(self.dlitemcenterport) + '/center/goods/v1/goods_detail'
        headers = {'X-ApiVersion':'1.0'}
        response = requests.post(url,headers=headers,json=data)
        response.connection.close()
        return response