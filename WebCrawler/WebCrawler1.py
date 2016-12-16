import requests
from bs4 import BeautifulSoup
stockList=[]
crawlSite="http://www.baidu.com"
res=requests.get(crawlSite)
data=res.content
stockList=data.split(',')
# print stockList

html = requests.get(crawlSite).text
soup =BeautifulSoup(html,'html.parser').decode('utf-8')
print soup

# href=soup.xpath('/html')
# print href