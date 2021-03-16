# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/2 16:54
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

"""
本API集成开发原则：
1. 尽量使用requests模拟各大平台的SDK
2. 尽量提供良好的封装与一致的响应
3. 尽量提高程序的稳健性、兼容性与可扩展性
"""

import os
import time
import json
import yaml
import base64
import requests
from pprint import pprint


from old.fast_cmd.core import read_image_bytes, read_image_base64

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
ACCOUNT_PATH = os.path.join(PROJECT_DIR, 'config/accounts.yaml')
accounts_dict = yaml.load(open(ACCOUNT_PATH, 'r', encoding='utf-8'), Loader=yaml.Loader)


class API_Baidu:
    """
    目前使用的是南川个人申请的APP
    APP相关的配置：https://console.bce.baidu.com/ai/?_=1593679186660&fromai=1#/ai/ocr/app/detail~appId=1784047
    API的使用说明：https://cloud.baidu.com/doc/OCR/s/3k3h7yeqa
    目前使用的API接口为 basicAccurate，即高精度版本，500次/天免费
    """

    name = "百度"

    def __init__(self):
        self.API_HOST = "https://aip.baidubce.com"
        self.API_OAUTH = '/oauth/2.0/token'
        self.API_WEBIMAGE_LOC = '/rest/2.0/ocr/v1/webimage_loc'
        self.API_OCR = self.API_HOST + self.API_WEBIMAGE_LOC

        self.APP_ID = accounts_dict['baidu']['APP_ID']
        self.AK = accounts_dict['baidu']['AK']
        self.SK = accounts_dict['baidu']['SK']
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        response = requests.get(self.API_HOST+self.API_OAUTH, params={
            "grant_type": 'client_credentials',
            "client_id": self.AK,
            "client_secret": self.SK,
        })
        self.ACCESS_TOKEN = response.json()['access_token']

    def ocr_img(self, img_path, verbose=False):
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read())

        params = {"image": img}
        request_url = self.API_OCR + "?access_token=" + self.ACCESS_TOKEN
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response.status_code != 200:
            raise Exception("失败！状态码：{}，返回内容：\n{}".format(response.status_code, response.text))

        result = response.json()
        words = [i['words'] for i in result['words_result']]
        if verbose:
            return {
                "output": result,
                "words": words
             }
        else:
            return words


class API_Huawei:

    # 调用接口：https://console.huaweicloud.com/ocr/?locale=zh-cn&region=cn-north-4#/ocr/management/serviceList/web-image
    # API概览：https://support.huaweicloud.com/api-ocr/ocr_03_0047.html

    name = "华为"

    @staticmethod
    def get_token(user_name, user_pswd, domain_name, scope_type="project", project_name="cn-north-4", refresh=False):

        TOKEN_PATH = os.path.join(PROJECT_DIR, "cache/.huawei-token.txt")

        if not refresh and os.path.exists(TOKEN_PATH):
            token_data = json.load(open(TOKEN_PATH, "r", encoding="utf-8"))
            valid_surplus = (token_data['dead_time'] - time.time()) / 3600
            if valid_surplus > 0:
                token_value = token_data['token_value']
                print("token从本地获取成功，剩余有效时间：{:.1f}小时".format(valid_surplus))
                return token_value

        if scope_type == "global":
            scope = {"domain": {"name": domain_name}}
        else:
            scope = {"project": {"name": project_name}}

        url = 'https://iam.myhuaweicloud.com/v3/auth/tokens?nocatalog=true'

        data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": domain_name
                            },
                            "name": user_name,
                            "password": user_pswd
                        }
                    }
                },
                "scope": scope
            }
        }

        res = requests.post(url, json=data, headers={"Content-Type": "application/json;charset=utf8"})

        token_value = res.headers['X-Subject-Token']
        print("获取token（华为）成功")

        # Token的有效期为24小时，需要使用一个Token鉴权时，可以先缓存起来，避免频繁调用。
        # 参考：https://support.huaweicloud.com/api-ocr/ocr_03_0005.html
        token_data = {
            "token_value": token_value,
            "fetch_time": time.time(),
            "dead_time": time.time() + 24*60*60 - 60
        }
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=4, ensure_ascii=False)
        print("已保存token到本地：{}".format(os.path.abspath(TOKEN_PATH)))
        print("请注意，token的有效时间只有24小时！")
        return token_value

    def __init__(self):
        self.api_web_image = '/v1.0/ocr/web-image'
        self.api_general_text = '/v1.0/ocr/general-text'
        self.api = self.api_web_image
        
        # Token Request
        self.username = accounts_dict['huawei']['username']
        self.password = accounts_dict['huawei']['password']
        self.domain_name = accounts_dict['huawei']['domain_name']
        self.project_name = "cn-north-4"

        # AKSK Request
        self.AK = accounts_dict['huawei']['AK']
        self.SK = accounts_dict['huawei']['SK']

    def ocr_img(self, img_path, region="cn-north-4", verbose=False):

        def get_endpoint_from_region(region):
            return 'ocr.{}.myhuaweicloud.com'.format(region)

        url = 'https://{endpoint}/v1.0/ocr/web-image'.format(endpoint=get_endpoint_from_region(region))
        data = {"image": read_image_base64(img_path)}
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.get_token(self.username, self.password, self.domain_name)
        }

        response = requests.post(url, json=data, headers=headers)
        try:
            words = [i['words'] for i in response.json()['result']['words_block_list']]
        except KeyError:
            pprint(response.json())
        else:

            if verbose:
                return {"output": response.json(), "words": words}
            else:
                return words


class API_Alibaba:

    # 没有测试通过

    name = "阿里巴巴"

    def __init__(self):
        APP_CODE = '87673b55db7a498b95d307f1805268f9'
        AK = '203833897'
        SK = '73nBzMa8wff0RM1mSEgeD9nrKNmdustL'

        # url = 'http://tongyongwe.market.alicloudapi.com/generalrecognition/recognize'
        host = 'https://tongyongwe.market.alicloudapi.com'
        path = '/generalrecognition/recognize'

        self.url = host + path
        self.params = {
            "type": "cnen",
            "Authorization": "APPCODE " + APP_CODE,
        }
        self.headers = {
            "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def ocr_img(self, img_path):
        res = requests.post(self.url,
                            params=self.params,
                            data=read_image_base64(img_path),
                            headers=self.headers,
                            verify=False
                            )
        return res.json()


class API_FacePlusPlus:

    name = "旷视"

    AK = '18tefDf5qeuEZaEyuWGABhR_9WiinYxQ'
    SK = 'js9OUgiSC4zru-O-SHQ8L348BUlPyIMg'

    url = 'https://api-cn.faceplusplus.com/imagepp/v1/recognizetext'

    def ocr_img(self, img_path):
        params = {
            "api_key": self.AK,
            "api_secret": self.SK,
            # "image_file": read_image_bytes(IMG_PATH),
            # "image_base64": read_image_base64(IMG_PATH),
        }
        res = requests.post(self.url, json=params, file=read_image_bytes(img_path))
        return res.json()


