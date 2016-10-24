# !/usr/bin/python
# coding:utf-8
from bs4 import BeautifulSoup
import fileinput

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.
</p>

<p class="story">...</p>
</body>
</html>
"""
html_doc2=open('html/test1.html')  #自当前路径开始算,相当于'./html/test1.html'

#打开文件的方式
nf = open('html/test2.html','w') #p127 打开模式有很多种，常用r,w,a..
print nf
nf.write('test22,create new file\nxxx')
nf.close()  #无论哪种打开模式，写完内容后要及时关闭。如果不关闭，会停留在内存中，浪费内存空间，页增加了文件安全的风险

#readline
# while True:
#     line=html_doc2.readline()
#     if not line:
#         break
#     print html_doc2.tell(),line,
# # seek 让指针移动
# html_doc2.seek(2)
# print html_doc2.tell()

#fileinput模块
# for line in fileinput.input('html/test1.html'):
# for line in html_doc2:   #此处与上一行等同
#     print line,




# soup = BeautifulSoup(html_doc2, "html.parser")
# tag = soup.p
# # print type(tag)
# # tag中最重要的属性name和attributes
# #print tag.name
# #print tag.attrs
#
# print soup.html.find_all("p")
