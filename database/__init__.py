# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/30 4:45
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

import uuid
from datetime import datetime, date
from config.settings import PROJECT_DIR, os

import yaml
import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient
# uri = AsyncIOMotorClient('nanchuan.site', 27017)


data_api = yaml.load(open(os.path.join(PROJECT_DIR, 'config/api.yaml'), 'r', encoding='utf-8'), Loader=yaml.FullLoader)
data_db = yaml.load(open(os.path.join(PROJECT_DIR, 'database/database.yaml'), 'r', encoding='utf-8'), Loader=yaml.FullLoader)['database']['mongodb'] # type: dict

uri = pymongo.MongoClient('mongodb://{username}:{password}@{host}:{port}/?authSource={db_name}'.format(**data_db))
# uri = pymongo.MongoClient('nanchuan.site:2708', username='shenyao', password='shenyao', authSource='shenyao')

db = uri['shenyao']