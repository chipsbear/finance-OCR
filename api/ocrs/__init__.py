# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/26 20:54
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import os
import time
import yaml
import json
import requests

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
api_dict = yaml.load(open(os.path.join(PROJECT_DIR, 'config/api.yaml'), 'r', encoding='utf-8'), Loader=yaml.FullLoader)

