import urllib2

url = "http://idanlu.com:8000/api/v3/projects/81/repository/commits/Web_V2%2E1%2E5?private_token=oGmBRCQXj9tXzLCQiVCu"
print url
query_req = urllib2.Request(url)
query_resp = urllib2.urlopen(query_req)
print query_resp.read()