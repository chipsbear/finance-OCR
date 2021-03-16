# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/26 20:55
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from . import *

cp_name = 'huawei'

"""
华为使用token方式进行登录，token会被缓存
"""

def get_token(user_name, user_pswd, domain_name, scope_type, project_name, refresh=False):

    TOKEN_PATH =  os.path.join(os.path.dirname(__file__), '.huawei-ocr-token.txt')

    if not refresh and os.path.exists(TOKEN_PATH):
        token_data = json.load(open(TOKEN_PATH, "r", encoding="utf-8"))
        valid_surplus = (token_data['dead_time'] - time.time()) / 3600
        if valid_surplus > 0:
            token_value = token_data['token_value']
            print("token从本地获取成功，剩余有效时间：{:.1f}小时".format(valid_surplus))
            return token_value

    scope = {"domain": {"name": domain_name}} if scope_type=='global' else {"project": {"name": project_name}}

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

    # Token的有效期为24小时，需要使用一个Token鉴权时，可以先缓存起来，避免频繁调用。
    # 参考：https://support.huaweicloud.com/api-ocr/ocr_03_0005.html
    token_data = {
        "token_value": token_value,
        "fetch_time": time.time(),
        "dead_time": time.time() + 24 * 60 * 60 - 60
    }
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=4, ensure_ascii=False)
    print("已保存token到本地：{}".format(os.path.abspath(TOKEN_PATH)))
    print("请注意，token的有效时间只有24小时！")
    return token_value


def huawei_ocr(api_path: str, img_base64: str, verbose: bool=False):
    USERNAME = api_dict[cp_name]['app']['username']
    PASSWORD = api_dict[cp_name]['app']['password']
    DOMAIN_NAME = api_dict[cp_name]['app']['domain_name']
    REGION = 'cn-north-4'
    PROJECT_NAME = REGION

    url = api_dict[cp_name]['root'].format(region=REGION) + api_path
    params = {"image": img_base64}
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": get_token(USERNAME, PASSWORD, DOMAIN_NAME, scope_type='project', project_name=PROJECT_NAME)
    }

    data = requests.post(url, json=params, headers=headers).json()
    words = [i['words'] for i in data['result']['words_block_list']]
    return {'words': words, 'raw': data['result']} if verbose else {'words': words}

