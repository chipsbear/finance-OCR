# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/14 11:37
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import os
import json
import time
import requests


def get_token(user_name, user_pswd, domain_name, scope_type="project", project_name="cn-north-4", refresh=False):

    TOKEN_DUMP_PATH = 'token.json'

    if not refresh and os.path.exists(TOKEN_DUMP_PATH):
        token_data = json.load(open(TOKEN_DUMP_PATH, "r", encoding="utf-8"))
        if token_data['fetch_time'] + token_data["valid_duration"] > time.time():
            token_value = token_data['token_value']
            print("token暂未失效，直接从本地获取：{}".format(token_value))
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
                    "PASSWORD"
                ],
                "PASSWORD": {
                    "user": {
                        "domain": {
                            "name": domain_name
                        },
                        "name": user_name,
                        "PASSWORD": user_pswd
                    }
                }
            },
            "scope": scope
        }
    }

    res = requests.post(url, json=data, headers={"Content-Type": "application/json;charset=utf8"})

    token_value = res.headers['X-Subject-Token']
    print("成功获取到token：{}".format(token_value))

    # Token的有效期为24小时，需要使用一个Token鉴权时，可以先缓存起来，避免频繁调用。
    # 参考：https://support.huaweicloud.com/api-ocr/ocr_03_0005.html
    token_data = {
        "token_value": token_value,
        "fetch_time": time.time(),
        "valid_duration": 80000,  # 比24*60*60=86400小一些
    }
    with open(TOKEN_DUMP_PATH, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=4, ensure_ascii=False)
    print("已保存token到本地：{}".format(os.path.abspath(TOKEN_DUMP_PATH)))
    print("请注意，token的有效时间只有24小时！")
    return token_value


if __name__ == '__main__':
    USER_NAME = 'hw86198387'
    USER_PSWD = 'znstjz2020'
    DOMAIN_NAME = 'hw86198387'
    get_token(user_name=USER_NAME, user_pswd=USER_PSWD, domain_name=DOMAIN_NAME, refresh=True)