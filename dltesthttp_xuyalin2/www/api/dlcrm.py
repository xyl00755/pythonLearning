#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlcrm:
    def __init__(self,ini_file='../../config/http_config.ini'):
        # 从配置文件中读取接口服务器IP、域名，端口
        config = configparser.ConfigParser()
        config.read(ini_file)
        self.dlcrmhost = config['HTTP']['dlcrmhost']
        self.dlcrmport = config['HTTP']['dlcrmport']

    #POST请求，商品订单明细统计查询
    def goods_orders_statistics(self,data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/achievement/v1/goods_orders_statistics'
        headers = {'X-ApiVersion':'1.0'}
        response = requests.post(url,headers=headers,json=data)
        return response

    #POST请求，商品销售情况统计查询
    def goods_statistics(self,data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/achievement/v1/goods_statistics'
        response = requests.post(url,json=data)
        return response

    #GET /center/assignments/v1/saler_all_business/{id} 获取业务员所有业务关系
    def saler_all_business(self,data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_all_business/'+data
        headers = {'X-ApiVersion':'1.0'}
        response = requests.get(url,headers=headers)
        response.connection.close()
        return response

    #GET /center/assignments/v1/saler_customers_assignment/{id} 获取业务员已分配客户列表
    def saler_customers_assignment(self, data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_customers_assignment/'+data
        headers = {'X-ApiVersion':'1.0'}
        response = requests.get(url,headers=headers)
        response.connection.close()
        return response

    #GET /center/assignments/v1/saler_products_assignment/{id} 获取业务员已分配产品列表
    def saler_products_assignment(self, data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_products_assignment/'+data
        headers = {'X-ApiVersion':'1.0'}
        response = requests.get(url,headers=headers)
        response.connection.close()
        return response

    #POST /center/assignments/v1/saler_customers_all 获取业务员所有客户列表
    def saler_customers_all(self, data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_customers_all'
        headers = {'X-ApiVersion': '1.0'}
        response = requests.post(url, headers=headers, json=data)
        response.connection.close()
        return response

    #POST /center/assignments/v1/saler_customers_assignment_product 获取业务员已分配产品的客户列表
    def saler_customers_assignment_product(self, data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_customers_assignment_product'
        headers = {'X-ApiVersion': '1.0'}
        response = requests.post(url, headers=headers, json=data)
        response.connection.close()
        return response

    #POST /center/assignments/v1/saler_products_all 获取业务员所有产品列表
    def saler_products_all(self, data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_products_all'
        headers = {'X-ApiVersion': '1.0'}
        response = requests.post(url, headers=headers, json=data)
        response.connection.close()
        return response

    #POST /center/assignments/v1/saler_products_assignment_customer 获取业务员已分配客户的产品列表
    def saler_products_assignment_customer(self,data):
        url = 'http://' + self.dlcrmhost + ':' + str(self.dlcrmport) + '/center/assignments/v1/saler_products_assignment_customer'
        headers = {'X-ApiVersion': '1.0'}
        response = requests.post(url, headers=headers, json=data)
        response.connection.close()
        return response