from lib.wego_unittest import WegoUnittest
import biz.home_page, biz.shixun
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
        biz.home_page.root.get_courses()

    def test_004(self):
        """CASE_05:(API) 编程实践基础流程demo"""
        # 教师登录、并获取个人信息
        biz.home_page.login_educoder(teacher_username, teacher_password, user_header_1)
        # 学生登录、并获取个人信息
        biz.home_page.login_educoder(student_username, student_password, user_header_2)
        biz.home_page.login_educoder(student_username_2, student_password_2, user_header_3)

        # 教师操作：
        # 1、新建一个实训 python3.6环境,设置好仓库及关卡并发布
        git_files = [('auto_test/src/step1/case01.py', 'print("XXX")\r\nprint("YYY")'),
                     ('auto_test/src/step2/case02.py', 'print("ZZZ")\r\nprint("AAA")')]
        challenges = [
            ('第1关: 计算最大值、最小值',
             '输入多个数字以空格分隔\n输出最大值与最小值',
             git_files[0][0],
             git_files[0][0],
             [
                 {"hidden": 0, "input": "1 2 3 4 5", "output": "1\n5\n", "score": 33, "is_file": False},
                 {"hidden": 0, "input": "1 2 5 7 44 84 95 45 86 54 86 44 33 3", "output": "1\n95\n",
                  "score": 33, "is_file": False},
                 {"hidden": 0, "input": "1", "output": "1\n1\n", "score": 34, "is_file": False}
             ]),
            ('第2关: 计算总数,平均数',
             '输入多个数字以空格分隔\n输出总和与平均数(保留两位小数)',
             git_files[1][0],
             git_files[1][0],
             [
                 {"hidden": 0, "input": "1 2 3 4 5", "output": "15\n3.00\n", "score": 33, "is_file": False},
                 {"hidden": 0, "input": "1 2 5 7 44 84 95 45 86 54 86 44 33 3", "output": "589\n42.07\n",
                  "score": 33, "is_file": False},
                 {"hidden": 0, "input": "1", "output": "1\n1.00\n", "score": 34, "is_file": False}
             ])
        ]
        shixun_create_info, git_info = biz.shixun.create_shixun(environment_name='Python3.6',
                                                                shixun_name=api_name_root + self.timestr,
                                                                git_file_list=git_files,
                                                                challenge_list=challenges,
                                                                headers=user_header_1)

        # 学生操作
        # 1、获取实训信息
        shixun_info = biz.shixun.shixuns.get_shixun_info(shixun_id=shixun_create_info['data']['identifier'],
                                                         headers=user_header_2)
        assert shixun_info.get('identifier') == shixun_create_info['data']['identifier'], '学生获取实训信息失败'
        # 2、挑战实训
        file_content_list = [("N_list = list(map(int,input().split()));print(min(N_list));print(max(N_list))", 2),
                             ("N_list = list(map(int,input().split()));print(sum(N_list));"
                              "print('{:.2f}'.format(sum(N_list)/len(N_list)))", 2)]
        suc_urls = biz.shixun.start_challenge(shixun_id=shixun_create_info['data']['identifier'],
                                              file_content_list=file_content_list,
                                              headers=user_header_2)

        file_content_list = [("print(456)", 0),
                             ("print(123)", 0)]
        fail_urls = biz.shixun.start_challenge(shixun_id=shixun_create_info['data']['identifier'],
                                               file_content_list=file_content_list,
                                               headers=user_header_3)

        print('<pre style="color:green">闯关成功链接:')
        for url in suc_urls:
            print(url)
        print('</pre>')
        print('<pre style="color:red">闯关失败链接:')
        for url in fail_urls:
            print(url)
        print('</pre>')

