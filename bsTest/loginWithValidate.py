#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import cookielib
import urllib
import re
import sys

dlmall='http://www.danlu.com'
dlsso='http://sso.danlu.com'


def loginPara(username,password):
    url = dlsso + '/login?service=' + dlmall + '/common/caslogin.html'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    lt = soup.find("input", {"name": "lt"})['value']
    # imgName=downLoadImg(dlsso+'/validateCode.html',1)
    # validateCode = openAndSet(imgName)
    execution = str(soup.find("input", {"name": "execution"})['value'])
    playdata = {'username': username,
                'password': password,
                # 'validateCode': validateCode,
                'lt': lt,
                'execution': execution,
                '_eventId': 'submit'}
    return playdata

'''模拟登录'''
CaptchaUrl = dlsso+'/validateCode.html'
PostUrl = "http://sso.danlu.com/login?service=http://www.danlu.com/common/caslogin.html"
# 验证码地址和post地址

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
# 将cookies绑定到一个opener cookie由cookielib自动管理

username = 'xyl_ps1'
password = 'CCxx1111'
# 用户名和密码

picture = opener.open(CaptchaUrl).read()
# 用openr访问验证码地址,获取cookie

local = open('./pic/0001.gif', 'wb')
local.write(picture)
local.close()
# 保存验证码到本地

# SecretCode = raw_input('输入验证码： ')
# 打开保存的验证码图片 输入

postData = loginPara(username,password)
# 根据抓包信息 构造表单

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Host':'sso.danlu.com',
    'Origin':'http://sso.danlu.com',
    'Referer' :'http://sso.danlu.com/login?service=http://www.danlu.com/common/caslogin.html'
}
# 根据抓包信息 构造headers

data = urllib.urlencode(postData)
# 生成post数据 ?key1=value1&key2=value2的形式
request = urllib2.Request(PostUrl, data, headers)
# 构造request请求
try:
    response = opener.open(request)
    result = response.read()
    # 由于该网页是gb2312的编码，所以需要解码
    print result
    # 打印登录后的页面
except urllib2.HTTPError, e:
    print e.code
# 利用之前存有cookie的opener登录页面
