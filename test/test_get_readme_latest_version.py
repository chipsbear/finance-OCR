# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/28 23:36
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

with open('../readme.md', 'r', encoding='utf-8') as f:
    API_FAST_DESCRIPTION = f.read()


import re

assert re.search('### V([\d\.]+)', API_FAST_DESCRIPTION).groups()[0] == '0.7.2'