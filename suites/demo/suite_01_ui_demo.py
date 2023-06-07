from lib.wego_unittest import WegoUnittest
from lib.wego_webdriver import *
from config.common_config import *

base_url = 'https://www.educoder.net/'
xpath_open_login_box_button = "//span[.='登录 / 注册']"
xpath_username_input = "//input[@id='login']"
xpath_password_input = "//input[@id='password']"
xpath_login_button = "//button[@type='submit' and contains(.,'登 录')]"
xpath_user_logo = "//section[contains(@class,'ant-dropdown-trigger')]"
xpath_my_classroom_label = "//a[.='教学课堂']"
xpath_start_create_classroom_button = "//div[.='新建教学课堂']"
xpath_course_name_input = "//input[@id='course']"
xpath_classroom_name_input = "//input[@id='classroom']"
xpath_period_input = "//input[@id='period']"
xpath_credit_input = "//input[@id='credit']"
xpath_endTime_input = "//input[@id='endTime']"
xpath_commit_create_classroom_button = "//button[.='提 交']"


# xpath_bd_search_btn = '//input[@id="su"]'
# xpath_bd_close_tool_btn = '//span[contains(.,"收起工具")]'
# xpath_bd_result_count_text = '//span[starts-with(.,"百度为您找到相关结果约")]'


class TestDemo(WegoUnittest):
    """UI自动化 DEMO"""
    browser = None

    def setUp(self):
        # 打开浏览器
        self.timestr = get_time_str('_%Y%m%d_%H_%M_%S')
        self.browser = Browser(port=None)
        # self.browser = Browser(port=9222)
        # self.browser.switch_to_window_by_title('统一用户管理')

    def tearDown(self):
        self.browser.save_screen('tear_down_{}'.format(self.get_title()))
        self.browser.driver.close()

    def test_001(self):
        """CASE01:(UI) 助教登录并创建新课堂"""
        self.browser.open_url(url=base_url)
        self.browser.wait_element(desc='打开登录框按钮', value=xpath_open_login_box_button, action='click')
        self.browser.wait_element(desc='用户名输入框', value=xpath_username_input, action='input', content=teacher_username)
        self.browser.wait_element(desc='用户名输入框', value=xpath_password_input, action='input', content=teacher_password)
        self.browser.wait_element(desc='登录按钮', value=xpath_login_button, action='click')
        self.browser.wait_element(desc='用户头像', value=xpath_user_logo, action='click')
        self.browser.wait_element(desc='我的教学课堂列表', value=xpath_my_classroom_label, action='move_to')
        self.browser.wait_element(desc='开始创建课堂按钮', value=xpath_start_create_classroom_button, action='click')
        self.browser.wait_element(desc='课程名称输入框', value=xpath_course_name_input, action='input', content=ui_name_root)
        self.browser.wait_element(desc='课堂名称输入框', value=xpath_classroom_name_input, action='input',
                                  content=self.timestr)
        self.browser.wait_element(desc='学时输入框', value=xpath_period_input, action='input', content='80')
        self.browser.wait_element(desc='学分输入框', value=xpath_credit_input, action='input', content='3')
        self.browser.wait_element(desc='结束时间输入框', value=xpath_endTime_input, action='input', content='2024-10-10',
                                  send_enter=True)
        self.browser.wait_element(desc='确认提交创建课堂按钮', value=xpath_commit_create_classroom_button, action='click')