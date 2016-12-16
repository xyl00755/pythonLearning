#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2016年4月16日

@author: Roy
'''
import urllib2
import urllib
import json
import configparser
import cookielib
import StringIO
import gzip
import logging
from www.common.other import Dict


class httpbase:
    def __init__(self):

        # 从配置文件中读取接口服务器IP、域名，端口
        from www.common.config import config
        httpConfig = config().confighttp
        self.host = httpConfig['wshost']
        self.port = httpConfig['wsport']
        self.smshost = httpConfig['smshost']
        self.smsport = httpConfig['smsport']
        self.headers = {'Content-Type': 'application/json;charset=UTF-8'}
        self.body = {}
        self.statusCode = -1

        # install cookie
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        #self.sessionId = None
        self.gltoken = None
        urllib2.install_opener(self.opener)

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def set_header(self, headers):
        self.headers = headers

    def get_status_code(self):
        return self.statusCode

    def get_body(self):
        return self.body

    def get_value(self, keys):
        try:
            return self.body[keys]
        except KeyError:
            try:
                return self.get_sec_value(keys)
            except KeyError:
                raise AttributeError(r"'Dict' object has no attribute '%s'" % keys)

                # return self.body[keys]

    def get_sec_value(self, keys):
        # secValue = Dict()
        try:
            return self.body.model[keys]
        except:
            pass
        # for key, value in self.body.model.iteritems():
        #     secValue[key] = value
        # return secValue[keys]

    # 封装HTTP GET请求方法
    def get(self, url, params):
        params = urllib.urlencode(params)  # 将参数转为url编码字符串
        url = 'http://' + self.host + ':' + str(self.port) + url + params
        request = urllib2.Request(url, headers=self.headers)

        try:
            response = urllib2.urlopen(request)
            fo = open("output.txt", "wb")
            fo.write(response.read().decode("utf-8"))
            fo.close()
            # response = response.read().decode('utf-8')  ## decode函数对获取的字节数据进行解码
            json_response = json.loads(response)  # 将返回数据转为json格式的数据
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装webservice POST请求方法
    def wspost(self, url, data, token = None):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if (token is None and self.gltoken is not None):
            data['token'] = self.gltoken
        elif (token == 'null'):
            self.gltoken = None
        elif (token is not None):
            data['token'] = token
        data = json.dumps(data, encoding="UTF-8", ensure_ascii=False).encode('utf-8')
        url = 'http://' + self.host + ':' + str(self.port) + url
        logging.info("request:\nPOST " + url + " HTTP/1.1\n" + data)
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request, data)
            if ((not self.headers.has_key('Cookie')) and response.headers.has_key('Set-Cookie')):
                self.headers['Cookie'] = response.headers['Set-Cookie'].split(';')[0]
            html = StringIO.StringIO(response.read())
            gzipper = gzip.GzipFile(fileobj=html)
            html = gzipper.read()
            json_response = json.loads(html)
            logging.info("response:\n%d\n%s%s" % (response.code, response.info(), json_response))
            self.statusCode = response.getcode()
            for key, value in json_response.iteritems():
                self.body[key] = value
            self.body = Dict(self.body.keys(), self.body.values())
            if(self.gltoken is None):
                self.gltoken = self.get_sec_value('token')
            return self.body
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装消息请求方法
    def smspost(self, url, data):
        data = json.dumps(data, encoding="UTF-8", ensure_ascii=False).encode('utf-8')
        url = 'http://' + self.smshost + ':' + str(self.smsport) + url
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request, data)
            html = StringIO.StringIO(response.read())
            json_response = json.loads(html.buf)
            self.statusCode = response.getcode()
            for key, value in json_response.iteritems():
                self.body[key] = value
            self.body = Dict(self.body.keys(), self.body.values())
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    data1 = {"username": "testlxmps113", "password": "508df4cb2f4d8f80519256258cfb975f"}
    httpbase().wspost('/login/doLogin.json', data1)
