# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/30 5:23
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import requests
import json


def check_ip(ip):
    url = 'http://ip.chinaz.com/ajaxsync.aspx?at=AiWenBaseData'

    data = {
        'ip': ip,
        'aiWenType': '区县级数据'
    }

    res = requests.post(url, data=data)

    return json.loads(res.text[1:-1])['Body'][0]


if __name__ == '__main__':
    ip = '115.171.230.141'
    print(check_ip(ip))