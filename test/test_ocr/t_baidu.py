# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/3 15:39
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

# encoding:utf-8

import requests
import base64
from pprint import pprint

API_KEY = 'zsZBR5PX8GlH4oiyhh9GjXqG'
SECRET_KEY = 'p14oSmCQZnf55ORuBXTxkO5goafb01Fq'

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?' \
       'grant_type=client_credentials&client_id={AK}&client_secret={SK}'.format(AK=API_KEY, SK=SECRET_KEY)
response = requests.get(host)
ACCESS_TOKEN = response.json()['access_token']

IMG_PATH = r'D:\PythonProjects\ProjectShenyaoZhineng\main\samples\微信\流水\wxls1.jpg'

'''
网络图片文字识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage_loc"
# 二进制方式打开图片文件
f = open(IMG_PATH, 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + ACCESS_TOKEN
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    result = response.json()
    words = [i['words'] for i in result['words_result']]
    pprint({
        "output": result,
        "words": words
    })