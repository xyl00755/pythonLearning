#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re

str = "【需求#5941】【华东环境】【交易平台】【工具栏】打开优惠券页面，点击关闭按钮，工具栏不关闭"
obj = re.match(r'【(.*?)】',str,)
if obj:
	print obj.group()