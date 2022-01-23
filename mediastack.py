#API Key:76605ed44844f358d5bdb3f0718274ab

import http.client, urllib.parse
import json

def get_articles():
    conn = http.client.HTTPConnection('api.mediastack.com')
    params = urllib.parse.urlencode({
        'access_key': '76605ed44844f358d5bdb3f0718274ab',
        'categories': 'general',
        'sort': 'popularity',
        'countries': 'us',
        'date':'2021-12-24,2021-12-31',
        'limit': 10,
        })

    conn.request('GET', '/v1/news?{}'.format(params))
    res = conn.getresponse()
    data = res.read()
    decoder=json.JSONDecoder()
    to_decode=data.decode('utf-8')
    result=decoder.decode(to_decode)['data']

    output=[]
    for dic in result:
        output.append((dic['title'], dic['published_at'], dic['url']))
    return output
