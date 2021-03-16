# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/28 12:46
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import os
import json
import base64
import requests


API_ROOT = 'https://nanchuan.site:666'

def img_bytes2base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode()

def img_path2name(img_path: str) -> str:
    return os.path.basename(img_path)

def json_dump(data: [dict, list], file_path: str):
    json.dump(data, open(file_path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


def fast(api_path, img_path, verbose=False, prefix='', suffix='_fast'):
    """
    :param api_path: 以 / 开头的路径，在API页面可以看到，例如华为的 '/api/v1/fast/huawei-img'
    :param img_path: 如果不熟悉相对路径，可以直接传入一个绝对路径，windows平台下记得引号前加上 r 以转义
    :param verbose: 在结果中是否包含原api给出的所有信息，比如位置等，推荐不需要
    :param prefix: 保存数据结果的前缀。如果希望数据结果存放在一起，可以使用前缀
    :param suffix: 保存数据结果的后缀。如果希望数据结果与文件紧邻，可以只写后缀
    :return: 返回一个json结果
    """
    img_name = img_path2name(img_path)

    # 获取原文件的文件夹地址，使数据保存到同目录，你也可以自定义一个保存路径
    img_dir = os.path.dirname(img_path)
    data_save_name = prefix + img_name.split('.')[0] + suffix + '.json'
    data_path = os.path.join(img_dir, data_save_name)

    # 请求数据结果
    response = requests.post(
        url=API_ROOT + api_path,
        params={'verbose': verbose},
        files=[('img', (img_name, open(img_path, 'rb')))]
    )
    if response.status_code == 200:
        # 保存数据结果
        data = response.json()
        json_dump(data, data_path)
        return data
    else:
        raise Exception("请求状态异常")


if __name__ == '__main__':

    # 以下是单张图片脚本示例
    api_path = '/api/v1/fast/huawei-img'
    img_path = r'C:\Users\mark\Desktop\测试图片.jpg' # 换成自己的本地图片
    data = fast(api_path, img_path, verbose=False)
    print(data)

    # 多张图片请自行使用for循环，不过后台暂时没有做任务调度优化，如有必要请联系我
