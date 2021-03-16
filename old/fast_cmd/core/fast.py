# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/15 21:58
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from old.fast_cmd.core import dump_json_data_safe
from old.fast_cmd.core import API_Huawei
from old.fast_cmd.core import clasify

from config.settings import OUTPUT_DIR

import os



class Fast:

    def __init__(self):
        self.ocr = API_Huawei()

    def ocr_img(self, img_path: str) -> list:
        """

        :param img_path:
        :return: 返回识别出来的一串文本列表
        """
        ocr_result = self.ocr.ocr_img(img_path, region='cn-north-4', verbose=False)

        # 过滤一下识别出的单字，主要解决【sample\支付宝\流水\zfbls3.jpg】的问题
        ocr_result = list(filter(lambda x: len(x)>1, ocr_result))
        return ocr_result

    def classify_data(self, data: list) -> dict:
        """

        :param data:
        :return: 返回分类结果，根据匹配度判断，有4+1种可能
        """
        classified_result = clasify(data)
        return classified_result

    def run(self, img_path, output_name='fast.json'):
        output_path = os.path.join(OUTPUT_DIR, output_name)
        ocr_result = self.ocr_img(img_path)
        classified_result = self.classify_data(ocr_result)
        classified_result.update({'ocr_result': ocr_result})
        dump_json_data_safe(classified_result, output_path)
        print("Dumped data_api into {}".format(output_path))
        return classified_result


if __name__ == '__main__':
    test_img_path = r'E:\MyWorks\Work@Onlyou2020\sample\支付宝\流水\zfbls3.jpg'
    F = Fast()
    print(F.run(test_img_path))