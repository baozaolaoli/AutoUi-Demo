from lib.edu_request import *
from config.common_config import *


def get_user_info(school=None, headers=user_header_1):
    url = host + '/api/users/get_user_info.json'
    data = {
        'school': school
    }
    res = req_get(url=url, params=data, headers=headers, desc="获取用户信息接口")
    return res


def get_navigation_info(school=None, headers=user_header_1):
    url = host + '/api/users/get_navigation_info.json'
    data = {
        'school': school
    }
    res = req_get(url=url, params=data, headers=headers, desc="获取导航信息接口")
    return res



def homepage_info(login, headers=user_header_1):
    url = host + '/api/users/{}/homepage_info.json'.format(login)
    data = {}
    res = req_get(url=url, params=data, desc="获取个人主页信息", headers=headers)
    return res


if __name__ == '__main__':
    pass
    # get_user_info()
    # get_navigation_info()
    # homepage_info(user_id='p49hjcek8')
