# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/29 0:03
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from fastapi import APIRouter
from .api_fast import api_fast


api_root = APIRouter()
api_root.include_router(api_fast, prefix='/fast', tags=['fast'])
