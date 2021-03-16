# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/4 19:45
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import os
import time

filename = '微信图片_20200704194814.jpg'  # 当前路径
filemt = time.localtime(os.stat(filename).st_mtime)
print(time.strftime("%Y-%m-%d %H:%M:%S", filemt))

# 输出
"""
2019-09-11
"""