# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/15 20:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import os
import json
import datetime
from config.settings import PROJECT_DIR, OUTPUT_DIR


OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'clasify.json')

ALGO_DICT = {
    'algo_wx_history': "微信流水",
    'algo_wx_detail': "微信详情",
    'algo_zfb_history': "支付宝流水",
    'algo_zfb_detail': "支付宝详情",
}

THRESHOLD = 3


def get_max_index_of_list(c: list):
    return c.index(max(c))


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        else:
            return json.JSONEncoder.default(self, obj)



def clasify(raw_data: list):

    from old.fast_cmd.core import algo_wx_detail, algo_wx_history, algo_zfb_detail, algo_zfb_history

    result = {
        "raw_data": raw_data,
        "result": []
    }
    for algo in [algo_wx_detail, algo_wx_history, algo_zfb_detail, algo_zfb_history]:
        data = [i for i in algo(raw_data)]
        item = {
            "algo": algo.__name__,
            "result": data,
            "len": len(data)
        }
        print('Finished Algo {}'.format(algo.__name__))
        result['result'].append(item)

    json.dump(result, open(OUTPUT_PATH, 'w', encoding='utf-8'), indent=2, ensure_ascii=False, cls=DateEncoder)
    print("Dumped data_api to {}".format(OUTPUT_PATH))

    max_item = result['result'][get_max_index_of_list([item['len'] for item in result['result']])]

    if max_item['len'] > THRESHOLD:
        max_item.update({
            'img_type': ALGO_DICT[max_item['algo']],
            'status': 'success'
        })
    else:
        max_item.update({
            'img_type': None,
            'status': 'failed'
        })

    return max_item


if __name__ == '__main__':
    test_data_path = '../output.json'

    json_data = json.load(open(test_data_path, 'r', encoding='utf-8'))

    test_data = json_data['data_api'][0]['data_api']

    assert isinstance(test_data, list)

    clasify(test_data)
