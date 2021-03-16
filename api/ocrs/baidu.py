# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/26 20:56
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from . import *

cp_name = 'baidu'


def get_token():
    AK = api_dict[cp_name]['app']['AK']
    SK = api_dict[cp_name]['app']['SK']
    response = requests.get(API_HOST + api_dict[cp_name]['api_oauth'], params={
        "grant_type": 'client_credentials',
        "client_id": AK,
        "client_secret": SK,
    })
    return response.json()['access_token']


def baidu_ocr(api_path: str, img_base64: str, verbose=False):
    params = {"image": img_base64, 'access_token': ACCESS_TOKEN}
    request_url = API_HOST + api_path
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.status_code != 200:
        raise Exception("失败！状态码：{}，返回内容：\n{}".format(response.status_code, response.text))

    result = response.json()
    words = [i['words'] for i in result['words_result']]
    return {'words': words, 'raw_ocr_result': result} if verbose else {'words': words}


API_HOST = api_dict[cp_name]['root']
ACCESS_TOKEN = get_token()
