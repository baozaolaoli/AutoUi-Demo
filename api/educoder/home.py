from lib.edu_request import *
from config.common_config import host


def index():
    url = host + '/api/home/index.json'
    data = {}
    res = req_get(url=url, params=data, desc="首页索引接口")
    return res


if __name__ == '__main__':
    pass
    # res = index()

