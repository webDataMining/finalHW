# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/12/2016   11:03

import requests as r
import urllib
import environmentVar as env


url = 'http://api.ltp-cloud.com/analysis/' + '?api_key=' + env.ltp_api_key + \
      '&pattern=sdp&format=plain' + '&text=' + urllib.parse.quote_plus('百度公司总部在哪里？')
text = '到2012年为止，联合国共有193个成员国。'
pay_load = {'api_key': env.ltp_api_key,
            'pattern': 'sdp',
            'format': 'json',
            'text': text}
rr = r.get(url, params=pay_load)
print(rr.text)