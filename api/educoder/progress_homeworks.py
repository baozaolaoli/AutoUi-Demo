"""
https://data.educoder.net
"""

from lib.edu_request import *
from config.common_config import *


def progress_homeworks_get(shixun_id_num, headers=user_header_1):
    new_headers=headers.copy()
    new_headers['Content-Type'] = 'application/json; charset=utf-8'
    new_headers['Accept'] = '*/*'
    url = host + '/api/progress_homeworks/{}'.format(shixun_id_num)
    data = {}
    res = req_get(url=url, params=data, headers=new_headers, desc="获取实训所在作业")
    return res.json()