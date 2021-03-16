# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/14 15:09
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

"""bash
pip install --editable .
"""

from setuptools import setup, find_packages

setup(
    name="mark-ocr",
    version="0.5.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'openpyxl==3.0.4',
        'pandas==1.0.5',
        'PyYAML==5.3.1',
        'requests==2.24.0',
        'click==7.1.2',
        'fastapi==0.60.1',
        'uvicorn',
        'python-multipart'
    ],
    entry_points='''
    [console_scripts]
    ocr=run:huawei_ocr
    fast=run:fast
    '''
)