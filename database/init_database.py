# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/29 12:52
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from . import *


for cp_name, cp_data in data_api.items():

    for api_item in data_api[cp_name]['ocr']:

        db['api_meta'].update_one(
            {
              "_id": uuid.uuid3(uuid.NAMESPACE_DNS, "{}-{}".format(cp_name, api_item['path']))
            },
            {'$set':{
                "cp_name": cp_name,
                "cp_name_cn": cp_data['cp_name_cn'],
                "api_root": cp_data['root'],
                "api_path": api_item['path'],
                "recommend": api_item.get("recommend"),
                "called_max": api_item.get("called_max"),
                "called_by": api_item.get('called_by'),
                "called_surplus": api_item.get("called_max"),
                "last_update": datetime.now()
            }},
            upsert=True
        )
