# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/26 19:32
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
import re

from fastapi import FastAPI
from api.api_root import api_root


readme_fp = 'readme-out.md'


with open(readme_fp, 'r', encoding='utf-8') as f:
    TITLE = f.readline()
    DESCRIPTION = f.read()
    PROJECT_NAME = re.search('# (\w+)', TITLE).groups()[0]
    LATEST_VERSION = re.search('### V([\d.]+)', DESCRIPTION).groups()[0]


app = FastAPI(
    title=PROJECT_NAME,
    description=DESCRIPTION,
    version=LATEST_VERSION
)
app.include_router(api_root, prefix='/api/v1')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=666, reload=True)
