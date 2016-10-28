#!/usr/bin/env python
# -*- coding:utf-8 -*-

from www.common.httpbase import *
import hashlib
import logging
import configparser
from bs4 import BeautifulSoup
import requests

class dlmall:
    def __init__(self,ini_file='../../config/http_config.ini'):
        # 从配置文件中读取接口服务器IP、域名，端口
        config = configparser.ConfigParser()
        config.read(ini_file)
        self.dlmallhost = config['HTTP']['dlmallhost']
        self.dlmallport = config['HTTP']['dlmallport']
        self.ssohost = config['HTTP']['ssohost']
        self.ssoport = config['HTTP']['ssoport']

    def login(self, username, password):
        s = requests.Session()

        #GET请求，加载登陆页面，获取到lt、execution,url = 'http://123.57.244.205:9003/main/newLogin.html'
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/main/newLogin.html'
        response = s.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        lt = str(soup.find("input", {"name": "lt"})['value'])
        execution = str(soup.find("input", {"name": "execution"})['value'])

        #GET请求，请求验证码
        url2 = 'http://' + self.ssohost + ':' + str(self.ssoport) + '/validateCode.html'
        s.get(url2)

        #PORT请求，登陆, url3 = 'http://123.57.152.182:9002/login?service=http://123.57.244.205:9003/common/caslogin.html'
        url3 = 'http://' + self.ssohost + ':' + str(self.ssoport) + '/login?service=http://' + self.ssohost + ':' + str(self.ssoport) + '/common/caslogin.html'
        playdata = {'username': username,
                    'password': password,
                    'validateCode': '1111',
                    'lt':lt,
                    'execution':execution,
                    '_eventId': 'submit'}
        s.post(url3, data=playdata,allow_redirects=True)
        return  s

    def getSellerOrdersCount(self,session):
        #http://123.57.244.205:9003/orders/getSellerOrdersCount.html?date=1474532184439
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orders/getSellerOrdersCount.html?date=1474532184439'
        response = session.get(url)
        res=json.loads(response.content)
        return res

    def saveOrderSplitInfo(self,session,status=None,minAmount=None,maxTimes=None):
        #POST /businessInfoModify/saveOrderSplitInfo.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/businessInfoModify/saveOrderSplitInfo.html'
        data={'status':status,
              'minAmount':minAmount,
              'maxTimes':maxTimes
        }
        response = session.post(url,data)
        res=json.loads(response.content)
        return res

    def splitOrder(self,session,orderNo=None):
        #GET /orderSplit/splitOrder.html?orderNo=24324354654656
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orderSplit/splitOrder.html'
        data = {'orderNo':orderNo}
        response = session.get(url,params=data)
        res=json.loads(response.content)
        return res

    def doSplitOrder(self,session,orderNo=None,splitItems=None):
        #POST /orderSplit/doSplitOrder.html
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orderSplit/doSplitOrder.html'
        data = {
            'orderNo':orderNo,
             'splitItems':splitItems
        }
        response = session.post(url,data)
        res=json.loads(response.content)
        return res

    def getSplitOrderInfo(self,session,orderNo=None):
        #GET /orderSplit/getSplitOrderInfo.html?orderNo=243534545465
        url = 'http://' + self.dlmallhost + ':' + str(self.dlmallport) + '/orderSplit/getSplitOrderInfo.html'
        data = {'orderNo':orderNo}
        response = session.get(url,params=data)
        res=json.loads(response.content)
        return res


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    s = dlmall().login("x_2","123456")
    response = dlmall().getSellerOrdersCount(s)
    print response