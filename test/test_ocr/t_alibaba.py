# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/2 19:50
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import urllib, urllib3, sys
import ssl


host = 'https://tongyongwe.market.alicloudapi.com'
path = '/generalrecognition/recognize'
method = 'POST'
appcode = '87673b55db7a498b95d307f1805268f9'
querys = 'type=cnen'
bodys = {}
url = host + path + '?' + querys

bodys['pic'] = '''iVBORw0KGgoAAAANSUhEUgAAAEEAAAAcCAYAAAA+59JsAAABzElEQVRYhe2XO3aDMBBFH1kF6WiyB5OKPoUoofMy4pRptBRUmh3Q4WXQwS4UNHj4xb8gnM+J3jnYeGQN0tXoyfZ0K/xzPfz0AH6DHAQ4CCQHAQ4CyUGAg0ByEOAgkBwErAChUTE8zxuuWKFZY2TfKW2hUsL879Aiq7tAnWkBE5O6tEn8zVoOoZQEACLT9SQ8BlNqSVCEZk7cLplSD+54cQPH2/xlJijH+9sMevvkTMzyLdDi7dBUh+5mE8AfxYNA0HuuiuvbolGIH1PksjSLgbqdEXYhYjXqmacI05xun57lNHdTQJkmkWG7WToTC0+oqvxk3A9uH01TKJgsMur6+FECg3ACsJ1gTRW7R/KyRdZ9AUUz9BdJNFmIr2oxBF7xufoKuUEMchceTdVUxcUePqKEKEAVBxRdGSCJbBBYQOhX/FBNyp4n1q1OgDOsJmr3M22H/tonZ1e2r5Y0BO0S+YrEjsG9Twc2LjZGNsqjkY3MrzdXEzOfT7XNngtLQ2RZQTCqyblH7j4f9MT9pZbXTgfOcQFCfzKtdBRbQ2AxjOH4up8+VaClVoMwPrNPVsRqj+HKGX572MozL5a28ufl/kDBQSA5CHAQSA5Cqw/jl78IZCtuaQAAAABJRU5ErkJggg=='''
post_data = urllib.urlencode(bodys)
request = urllib3.Request(url, post_data)
request.add_header('Authorization', 'APPCODE ' + appcode)

request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib3.urlopen(request, context=ctx)
content = response.read()
if (content):
    print(content)