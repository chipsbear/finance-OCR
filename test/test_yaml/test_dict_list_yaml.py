# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/29 11:40
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import yaml


data = yaml.load(open('./test_dict_list_yaml.yaml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)


assert isinstance(data['ocr'], list)
assert data['ocr'][0]['max'] == 500
assert data['ocr'][0]['recommend'] is True