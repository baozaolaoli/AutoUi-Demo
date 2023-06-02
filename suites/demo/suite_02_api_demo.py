from lib.wego_unittest import WegoUnittest
import biz.home_page
from config.common_config import *
from lib.data_convert import *


class TestDemoApi(WegoUnittest):
    """接口自动化 DEMO"""
    browser = None

    def setUp(self):
        self.timestr = get_time_str('_%Y%m%d_%H_%M_%S')

    def tearDown(self):
        pass

    def test_001(self):
        """CASE02:(API) 打开首页"""
        biz.home_page.open_home_page()

    def test_002(self):
        """CASE03:(API) 学生用户登录并获取个人主页信息"""
        user_info, cookie = biz.home_page.login_educoder(student_username, student_password, user_header_2)
        biz.home_page.users.homepage_info(login=user_info['login'], headers=user_header_2)

    def test_003(self):
        """CASE04:(API) 讲师用户登录并创建新课堂"""
        user_info, cookie = biz.home_page.login_educoder(teacher_username, teacher_password, user_header_1)
        biz.home_page.users.homepage_info(login=user_info['login'], headers=user_header_1)
        user_info = biz.home_page.users.get_user_info(school=1, headers=user_header_1).json()
        courses = biz.home_page.root.courses(course_list_name=api_name_root, name=api_name_root + self.timestr,
                                             school=user_info['user_school'])
        assert courses.json().get('course_id')
        assert courses.json().get('invite_code')
        print('课程id:', courses.json().get('course_id'))
        print('邀请码:', courses.json().get('invite_code'))
