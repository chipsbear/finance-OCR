# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/28 11:02
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import requests

API_KUANGSHI = 'https://api-cn.faceplusplus.com/imagepp/v1/recognizetext'
API_KEY = '18tefDf5qeuEZaEyuWGABhR_9WiinYxQ'
API_SECRET = 'js9OUgiSC4zru-O-SHQ8L348BUlPyIMg'


def kuangshi_ocr(img_bytes: bytes, verbose=False):
    """
    图片尺寸：最小48*48像素，最大800*800像素

    这个最大像素实在有点苛刻，手机截图出去的一般都在1k+的高度

    因此，如果要使用旷视的api，必须要写一个图片尺寸转换的wrapper
    """
    res = requests.post(
        API_KUANGSHI,
        params={
            'api_key': API_KEY,
            'api_secret': API_SECRET
        },
        files=[
            ('image_file', img_bytes),
        ]
    )

    data = res.json()
    result = data['result']
    words = [i['value'] for i in result]
    return {'words': words, 'raw_ocr_result': result} if verbose else {'words': words}


if __name__ == '__main__':
    fp = r'C:\Users\mark\Desktop\m-失效图片.png'

    kuangshi_ocr(open(fp, 'rb').read())