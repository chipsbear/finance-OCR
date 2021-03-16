# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/29 12:23
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from . import *
from fastapi import HTTPException


def _reset_api_called(api_called):
    if api_called:
        api_last = api_called[0]['call_time'] # type: datetime
        if api_last.day != datetime.now().day:
            api_called.clear()


def _db_insert_record(cp_name, api_path, client_host):
    db['api_called'].insert_one({"client_host": client_host, "cp_name": cp_name, "api_path": api_path,  'call_time': datetime.now()})


def _db_check_meta(cp_name, api_path):
    api_meta = db['api_meta'].find_one({'cp_name': cp_name, 'api_path': api_path})

    if api_meta['last_update'].date() != date.today():
        db['api_meta'].update_one({'_id': api_meta['_id']},
                                  {'$set': {'called_surplus': api_meta['called_max'], 'last_update': datetime.now()}})

    elif api_meta['called_surplus'] <= 0:
        raise HTTPException(400, detail="exceed max request per day!")

    return api_meta


def _db_update_meta(cp_name, api_path):

    api_meta = db['api_meta'].find_one_and_update({'cp_name': cp_name, 'api_path': api_path}, {'$inc': {'called_surplus': -1}},
                                                  return_document=True)
    return api_meta['called_surplus']


def record_api_called(cp_name, client_host):
    def wrapper_1(func):
        def wrapper(company_api_path, *args, **kwargs):
            _db_check_meta(cp_name, company_api_path)
            res = func(company_api_path, *args, **kwargs)
            _db_insert_record(cp_name, company_api_path, client_host)
            res['called_surplus'] = _db_update_meta(cp_name, company_api_path)
            return res
        return wrapper
    return wrapper_1