"""
https://data.educoder.net/api/accounts/login.json



"""

from lib.edu_request import *
from config.common_config import *


def login(login, password, autologin=True):
    url = host + '/api/accounts/login.json'
    data = {
        "login": login,
        "password": password,
        "autologin": autologin
    }
    res = req_post(url=url, params=data, desc="用户登录接口")
    return res



if __name__ == '__main__':
    login(login='18806642362',password='qqqq1111')

