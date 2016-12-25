#/usr/bin/env python
#coding=utf8
 
import http.client
import hashlib
import urllib
import random

def translate(words):
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'

    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = words
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf8"))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
     
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
     
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = eval(response.read().decode())
        #print(result["trans_result"][0]['dst'])
        return(result["trans_result"][0]['dst'])
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
