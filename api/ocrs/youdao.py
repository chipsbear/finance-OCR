# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/28 11:27
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import uuid
import hashlib
from . import *

cp_name = 'youdao'

AK = api_dict[cp_name]['app']['AK']
SK = api_dict[cp_name]['app']['SK']
api_root = api_dict[cp_name]['root']



def youdao_ocr(api_path: str, img_base64: str, verbose=False):

    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def encrypt(signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    data = {
        'img': img_base64,      # 图片的base64格式
        'imageType': '1',       # 1代表base64类型，目前仅支持这种
        'detectType': '10012',  # 按行识别
        'langType': 'zh-CHS',   # 中文简体，选‘auto’也可以
        'docType': 'json',      # 目前只支持json的响应格式
        'signType': 'v3',       # 签名类型
        'appKey': AK,
    }

    curtime = str(int(time.time()))
    data['curtime'] = curtime
    data['salt'] = salt = str(uuid.uuid1())
    data['sign'] = sign = encrypt(AK + truncate(img_base64) + salt + curtime + SK)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(api_root+api_path, data=data, headers=headers)
    data = res.json()

    result = data['Result']['regions']
    words = [line['text'] for item in result for line in item['lines']]
    return {'words': words, 'raw': result} if verbose else {'words': words}

