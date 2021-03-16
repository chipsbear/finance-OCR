# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/15 21:38
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from old.fast_cmd.core import API_Huawei
from old.fast_cmd.core import clasify


def fast_test(img_path):

    ocr_result = API_Huawei().ocr_img(img_path) # words list

    print({
        "company": 'huawei_ocr',
        'ocr result': ocr_result
    })

    classify_result = clasify(ocr_result)

    print({
        'query path': img_path,
        'classification': classify_result
    })

    return classify_result



if __name__ == '__main__':
    img_path = r'E:\MyWorks\Work@Onlyou2020\sample\支付宝\流水\zfbls1.jpg'
    result = fast_test(img_path)

    # 支付宝流水一，失败
    # 支付宝流逝二，失败

