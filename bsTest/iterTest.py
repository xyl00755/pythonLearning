# !/usr/bin/python
# coding:utf-8
from bs4 import BeautifulSoup
import fileinput

#迭代工具
# lst=['a','b','c','d','e']
# lst_iter=iter(lst)
#
# while True:
#     print lst_iter.next()

#文件迭代
html_doc2=open('html/test1.html')
print [line for line in html_doc2]

html_doc2.seek(0)
print list(html_doc2)

html_doc2.seek(0)
print tuple(html_doc2)

html_doc2.seek(0)
print "$$$".join(html_doc2)

a,b=open('html/test2.html')   #test2.html中要有2行
print a,b

print 'open.__doc__  表示读这个方法的说明文档，其内容为:\n'+open.__doc__