# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/2 21:58
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

# -*- coding: utf-8 -*-

import time
import uuid
import requests
import base64
import hashlib


YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '1ae4af450fc5bb6c'
APP_SECRET = 'Q16ydiHkioWWFEjjhBwMX7AZpX3so8Mu'

img_path = r'E:\MyWorks\Work@Onlyou2020\OCR\Samples\微信\流水\wxls1.jpg'


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect():
    f = open(img_path, 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['detectType'] = '识别类型'
    data['imageType'] = '1'
    data['langType'] = '合成文本的语言类型'
    data['query'] = q
    data['docType'] = 'json'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    print(response.content)


if __name__ == '__main__':
    connect()