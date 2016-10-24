import urllib2
from bs4 import BeautifulSoup

url = 'http://123.57.152.182:9002/login?service=http://123.57.244.205:9003/common/caslogin.html'
req = urllib2.Request(url)
response = urllib2.urlopen(req)
html = response.read()
soup = BeautifulSoup(html, "html.parser")
print soup.title
print soup.find("input",{"name":"lt"})['value']
