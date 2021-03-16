# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/28 22:33
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import yaml

api_dict = yaml.load(open('../config/api.yaml', 'r', encoding='utf-8').read(),
                     Loader=yaml.FullLoader)


huawei_region = 'cn-north-4'
assert api_dict['huawei']['root'].format(region=huawei_region) == 'https://ocr.cn-north-4.myhuaweicloud.com'

assert api_dict['huawei']['ocr']['/v1.0/ocr/general-text'] == '通用文字识别'

assert api_dict['baidu']['ocr']['/rest/2.0/ocr/v1/accurate'] == '通用文字识别（高精度含位置版）'