# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/29 13:37
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import pymongo
import uuid
uri = pymongo.MongoClient("nanchuan.site:27017")
coll = uri['shenyao']['api_meta']

coll.update_one({'_id': uuid.UUID('7fb21105-54e0-3be5-a193-1f3c96a30464')}, {'$set': {'called_surplus': '$called_max'}})