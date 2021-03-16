# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/15 21:34
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

from scripts.hook import get_one_data_from_ocr_result
from old.fast_cmd.core import clasify


data = get_one_data_from_ocr_result(ocr_name='ocr.json')

result = clasify(data)

print(result)
