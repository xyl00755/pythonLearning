# !/usr/bin/python
# coding:utf-8
from bs4 import BeautifulSoup
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

soup = BeautifulSoup(html_doc2, "html.parser")
tag = soup.p
# print type(tag)
# tag中最重要的属性name和attributes
#print tag.name
#print tag.attrs

print soup.html.find_all("p")
