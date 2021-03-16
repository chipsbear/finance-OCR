# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/2 17:23
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import json
import base64
import datetime

""" 读取图片 """

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        else:
            return json.JSONEncoder.default(self, obj)


def read_image_bytes(img_path):
    with open(img_path, 'rb') as fp:
        return fp.read()


def read_image_base64(img_path):
    return base64.b64encode(read_image_bytes(img_path)).decode()

def img_bytes2base64(img_bytes: bytes):
    try:
        return base64.b64encode(img_bytes).decode()
    except Exception as e:
        raise e


def read_json_file(file_path):
    return json.load(open(file_path, 'r', encoding='utf-8'))


def dump_json_data_safe(json_data, file_path):
    # json导出时，不支持datetime格式
    json.dump(json_data, open(file_path, "w", encoding='utf-8'), ensure_ascii=False, indent=2, cls=DateEncoder)
