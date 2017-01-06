#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from pytesser.pytesser import *
import requests

import urllib
import re
import sys
import cookielib


dlmall='www.danlu.com'
dlsso='sso.danlu.com'

class testContentSheet(Exception):
    def loginPara(self):
        url = 'http://'+dlsso+'/login?service=http://'+dlmall+'/common/caslogin.html'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.body.prettify())
        # print soup.title
        lt=soup.find("input",{"name":"lt"})['value']
        # imgName=downLoadImg(dlsso+'/validateCode.html',1)
        # validateCode = openAndSet(imgName)
        execution = str(soup.find("input", {"name": "execution"})['value'])
        playdata = {'username': 'xyl_zd7',
                    'password': 'CCxx1111',
                    # 'validateCode': validateCode,
                    'lt': lt,
                    'execution': execution,
                    '_eventId': 'submit'}
        return playdata

    def downLoadImg(self,url, num):
        for i in range(num):
            # url = 'http://sso.danlu.com/validateCode.html' #验证码的地址
            print "download", i
            file("./pic/%04d.gif" % i, "wb").write(urllib2.urlopen(url).read())
            # print "./pic/%04d.gif" % i
            return "./pic/%04d.gif" % i

    def openAndSet(self,filename):
        im = Image.open(filename)
        # im.show()
        imgry = im.convert('L')
        # imgry.show()
        # 二值化图象的时候把大于某个临界灰度值的像素灰度设为灰度极大值，把小于这个值的像素灰度设为灰度极小值
        # 固定阈值：
        threshold = 30
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        out = imgry.point(table, '1')
        # out.show()  #直接打开图片
        # im = Image.open('1.jpg')
        # print filename,image_to_string(out,config="-psm nobatch digits")
        img = image_to_string(out)
        return img

    def sessionLogin(self, username, password):
        s = requests.Session()
        # GET请求，加载登陆页面，获取到lt,executio
        url = 'http://' + dlsso + '/login?service=http://' + dlmall + '/common/caslogin.html'
        response = s.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        lt = str(soup.find("input", {"name": "lt"})['value'])
        execution = str(soup.find("input", {"name": "execution"})['value'])

        # GET请求，请求验证码
        imgName = self.downLoadImg('http://'+dlsso + '/validateCode.html', 1)
        # print imgName
        validateCode= self.openAndSet(imgName)
        print validateCode

        # PORT请求，登陆, url3 = 'http://123.57.152.182:9002/login?service=http://123.57.244.205:9003/common/caslogin.html'
        playdata = {'username': username,
                    'password': password,
                    'validateCode': validateCode,
                    'lt': lt,
                    'execution': execution,
                    '_eventId': 'submit'}
        s.post(url, data=playdata, allow_redirects=True)
        return s


    def handlerLogin(self,username, password):
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        # 将cookies绑定到一个opener cookie由cookielib自动管理


if __name__=='__main__':
    tc=testContentSheet()
    s1=tc.sessionLogin('xyl_ps1','CCxx1111')
    print s1.get('http://www.danlu.com/main/province.html').content

