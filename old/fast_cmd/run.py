# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/14 13:11
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import os
import json
import logging
logging.basicConfig(format="%(asctime)15s [%(levelname)s]: %(message)s", level=logging.INFO)

import click

from config.settings import OUTPUT_DIR
from old.fast_cmd.core import API_Baidu, API_Huawei


SUPPORTIVE_IMG_TYPES = ['png', 'jpg']
SUPPORTIVE_COMPANIES = {
    "huawei_ocr": API_Huawei,
    "_baidu": API_Baidu
}

OCR_OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'ocr.json')



def is_img_valid(file_name):
    return file_name.rsplit('.', 1)[-1] in SUPPORTIVE_IMG_TYPES


def gen_output_path(img_path, company, ):
    img_name = os.path.basename(img_path).rsplit(".", 1)[0]
    output_name = "{}-{}.json".format(img_name, company)
    return os.path.join(OUTPUT_DIR, output_name)


@click.command()
@click.option('-o', '--output', help="输出路径", default=OCR_OUTPUT_PATH,
              type=click.File(mode='w', encoding="utf-8"))
@click.option('-c', '--company', default="huawei_ocr", help="API选用的厂家",
              type=click.Choice(list(SUPPORTIVE_COMPANIES), case_sensitive=False))
@click.argument('path_list', nargs=-1, type=click.Path(exists=True))
def ocr_img(path_list, company, output):
    data = []

    logging.info("开始识别……")
    api_ocr = SUPPORTIVE_COMPANIES[company]()

    files = []
    for path in path_list:
        if os.path.isdir(path):
            for file in os.listdir(path):
                if is_img_valid(file):
                    files.append(os.path.join(path, file))
        elif is_img_valid(path):
            files.append(path)
        else:
            raise Exception("File {} is a not valid type of {}".format(path, "|".join(SUPPORTIVE_IMG_TYPES)))

    logging.info("一共检测到{}张图片".format(len(files)))

    for i, img_path in enumerate(files, start=1):
        item = {
                "index": i,
                "path": img_path,
                "data_api": None,
                "status": "prepare",
            }
        logging.info("正在识别第{}张图片：{}".format(i, img_path))
        try:
            res = api_ocr.ocr_img(img_path)
            logging.info("识别成功：{}".format(img_path))
            item.update({
                "data_api": res,
                "status": "success"
            })
        except Exception as e:
            item.update({
                "status": "failed"
            })
            logging.error(e)
        finally:
            data.append(item)
    logging.info("识别结束！")

    data = {
        "company": company,
        "type": "ocr",
        "total": len(files),
        "data_api": data
    }
    json.dump(data, output, indent=4, ensure_ascii=False)
    logging.info("已保存输出结果到{}".format(os.path.abspath(output.name)))
    return data



@click.command()
@click.option('-o', '--output_name', help="输出路径", default='fast.json',
              type=click.File(mode='w', encoding="utf-8"))
@click.argument('img_path')
def fast(img_path, output_name):
    from old.fast_cmd.core import Fast
    F= Fast()
    data = F.run(img_path, output_name.name)  # 已经自动保存数据了
    print(data)
    return data



if __name__ == '__main__':
    ocr_img()
