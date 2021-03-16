# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/27 15:57
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import re
import json
import yaml
import datetime
import os
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONST_FILE_PATH = os.path.join(PROJECT_DIR, 'config/keywords.yaml')
CONST_DICT = yaml.load(open(CONST_FILE_PATH, 'r', encoding="UTF-8").read(), Loader=yaml.FullLoader)


def is_float(s):
    return re.sub('[,.]', '', s).isdigit()


"""
一下几个涉及到时间的函数，都存在风险
"""
NOW = datetime.datetime.now()
YEAR = NOW.year
MONTH = NOW.month
DAY = NOW.day


def get_today():
    return NOW.today()
def get_yesterday():
    return NOW.today() - datetime.timedelta(days=1)


def get_trade_time_wx(trade_time, year=2020):
    TRADE_TIME_FORMAT_WX = "%Y年%m月%d日%H:%M"
    trade_time = trade_time.replace(" ", '') # 去除空格
    return datetime.datetime.strptime("{}年{}".format(year, trade_time), TRADE_TIME_FORMAT_WX)


def algo_wx_history(data):
    KEYWORD_TRADE_BACK = '已全额退还'

    def get_trade_time_wx(trade_time, year=2020):
        TRADE_TIME_FORMAT_WX = "%Y年%m月%d日%H:%M"
        trade_time = trade_time.replace(" ", '')  # 去除空格
        return datetime.datetime.strptime("{}年{}".format(year, trade_time), TRADE_TIME_FORMAT_WX)

    for K1, K2, K3, K4 in zip(data, data[1:], data[2:], data[3:]):
        """
        7-27：更新：
        不再使用右侧的统计字样，因为可能引发问题

        Sample:
        '2020年1月', '支出￥29419.60收入￥13663.29', '统计>',
        """
        if re.match("\d+年\d+月", K1) and re.match("支出", K2):
            YEAR, MONTH = re.match("(\d+)年(\d+)月", K1).groups()

        elif is_float(K2):
            if re.match("\d*月\d*日\s*\d*:\d*", K3):
                item = {
                    "trade_name": K1,
                    "trade_amount": K2,
                    "trade_time": get_trade_time_wx(K3, year=YEAR),
                    "trade_status": KEYWORD_TRADE_BACK if K4 == KEYWORD_TRADE_BACK else None,
                }
                yield item


def algo_zfb_history(data):
    def get_trade_time_zfb(date, time, YEAR=2020):
        if '今天' in date:
            the_day = get_today()
            YEAR = the_day.year
            MONTH = the_day.month
            DAY = the_day.day
        elif '昨天' in date:
            the_day = get_yesterday()
            YEAR = the_day.year
            MONTH = the_day.month
            DAY = the_day.day
        elif re.match("\d{2}-\d{2}", date):
            MONTH, DAY = re.match("(\d{2})-(\d{2})", date).groups()

        HOUR, MINUTE = re.match("(\d{2}):(\d{2})", time).groups()
        return datetime.datetime(*map(int, [YEAR, MONTH, DAY, HOUR, MINUTE]))

    for K1, K2, K3, K4 in zip(data, data[1:], data[2:], data[3:]):
        """
        Sample:
        "支出￥6907.35", "2020-05", "收入￥2.93",    
        """
        if re.match("^支出", K2) and re.match("^收入", K4):
            if re.match("(\d{4})-(\d{2})", K3):
                YEAR, MONTH = re.match("(\d{4})-(\d{2})", K3).groups()
            elif re.match("(\d+)", K3):
                MONTH = re.match("(\d+)", K3).group()
            elif '本月' in K3:
                pass

        elif is_float(K2):
            if re.match("(今天|昨天|\d{2}-\d{2})\s*(\d{2}:\d{2})", K4):
                date, time = re.match("(今天|昨天|\d{2}-\d{2})\s*(\d{2}:\d{2})", K4).groups()
                item = {
                    "trade_name": K1,
                    "trade_amount": K2,
                    "trade_type": K3,
                    "trade_time": get_trade_time_zfb(date=date, time=time, YEAR=YEAR),
                }
                yield item


def algo_wx_detail(data):
    STATUS = 0
    temp = ""
    item = None
    TRADE_DETAIL_KEYS = CONST_DICT['WX_TRADE_DETAIL_KEYS']
    for K1, K2 in zip(data, data[1:]):
        if STATUS == 0:
            if is_float(K2):
                STATUS = 1
                yield {"name": K1, "amount": K2}
        elif STATUS == 1:
            if K1 in TRADE_DETAIL_KEYS:
                item = {"key": K1, "val": K2}
            elif K2 in TRADE_DETAIL_KEYS:
                if item is not None:
                    item['val'] += temp
                    temp = ""
                    yield item
            else:
                temp += "\n" + K2
    yield item


def algo_zfb_detail(data):
    STATUS = 0
    temp = ""
    item = None
    TRADE_DETAIL_KEYS = CONST_DICT['ZFB_TRADE_DETAIL_KEYS']
    for K1, K2 in zip(data, data[1:]):
        if STATUS == 0:
            # 注意，如果单纯匹配浮点数，可能会匹配到状态栏的一些信息
            if is_float(K2):
                STATUS = 1
                yield {"name": K1, "amount": K2}
        elif STATUS == 1:
            if K1 in TRADE_DETAIL_KEYS:
                item = {"key": K1, "val": K2}
            elif K2 in TRADE_DETAIL_KEYS:
                if item is not None:
                    item['val'] += temp
                    temp = ""
                    yield item
            elif re.match('标签分类|更多', K2):
                break
            elif K2 == "交易成功":
                pass
            else:
                temp += "\n" + K2
    yield item