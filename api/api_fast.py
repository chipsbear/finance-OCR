# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/26 21:04
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import base64
from fastapi import APIRouter, File, Query, UploadFile, Request
from .ocrs.baidu import baidu_ocr
from .ocrs.huawei import huawei_ocr
from .ocrs.youdao import youdao_ocr
from .algos.classify import clasify
from .ocrs import *
from database.api_record import record_api_called

api_fast = APIRouter()


def output(ocr_result: dict) -> dict:
    classify_result = clasify(ocr_result['words'])
    classify_result['ocr_result'] = ocr_result
    return classify_result


def img_bytes2base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode('utf-8')


def gen_tags(company_name: str, is_recommended: bool = False) -> list:
    if is_recommended:
        return ['recommend', 'fast', company_name]
    else:
        return ['fast', company_name]


def gen_fast_function(company_name, company_api_name, company_api_path, our_api_path, is_recommended=False):
    @api_fast.post(our_api_path, tags=gen_tags(company_name, is_recommended), summary=company_api_name, )
    def fast_ocr(
            request: Request,
            img: UploadFile = File(..., description='选择上传并识别的图片'),
            verbose: bool = Query(False, description='是否打印原API调用的完整返回信息（默认：否）'),
            classify: bool = Query(False, description='是否对识别结果进行算法分类（默认：否，暂时不成熟）'),
    ) -> dict:
        @record_api_called(company_name, client_host=request.client.host)
        def wrapper(company_api_path, company_name, img, classify, verbose):
            ocr_result = globals()['{}_ocr'.format(company_name)](
                api_path=company_api_path, img_base64=img_bytes2base64(img.file.read()), verbose=verbose)
            return output(ocr_result) if classify else ocr_result
        return wrapper(company_api_path, company_name, img, classify, verbose)


for company_name, company_dict in api_dict.items():
    for api_item in company_dict['ocr']:
        our_api_path = '/{}{}'.format(company_name, api_item['path'])
        gen_fast_function(company_name, api_item['name'], api_item['path'], our_api_path, api_item.get('recommend'))



