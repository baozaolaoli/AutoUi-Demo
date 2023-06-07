"""educoder首页相关业务函数"""

from api.educoder import home, users, root, accounts
from config.common_config import *


def open_home_page():
    """
    未登录状态打开(或刷新)首页
    :return: None
    """
    root.setting()
    users.get_user_info()
    users.get_navigation_info()
    home.index()


def login_educoder(username=teacher_username, password=teacher_password, headers=user_header_1):
    """
    用户登录
    :param username: 帐号 
    :param pwd: 密码
    :return: (用户基本信息，Cookie)
    """
    res = accounts.login(login=username, password=password)
    user_info = res.json()
    assert user_info is not None, '登录失败,用户信息为空'
    assert res.headers['Set-Cookie'] is not None, '登录失败,响应头中未包含cookie'
    cookie = res.headers['Set-Cookie']
    headers['Cookie'] = cookie
    return user_info, cookie





