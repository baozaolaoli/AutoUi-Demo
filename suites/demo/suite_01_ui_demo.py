from lib.wego_unittest import WegoUnittest
from lib.wego_webdriver import *
import re

# from business.UI.portal import PortalPage, portal_url
# from business.UI.bup import *

base_url = 'http://www.baidu.com'
kw_ch = '腾讯'
kw_en = 'Tencent'

xpath_bd_search_input = '//input[@id="kw"]'
xpath_bd_search_btn = '//input[@id="su"]'
xpath_bd_close_tool_btn = '//span[contains(.,"收起工具")]'
xpath_bd_result_count_text = '//span[starts-with(.,"百度为您找到相关结果约")]'


class TestBupSmoke(WegoUnittest):
    """UI自动化 DEMO"""
    browser = None

    def setUp(self):
        # 打开浏览器
        self.browser = Browser(port=None)
        # self.browser = Browser(port=9222)
        # self.browser.switch_to_window_by_title('统一用户管理')

    def tearDown(self):
        self.browser.save_screen('tear_down_{}'.format(self.get_title()))
        self.browser.driver.close()

    def test_001(self):
        """CASE01: 百度搜索中文关键字"""
        self.browser.open_url(url=base_url)
        self.browser.wait_element(desc='百度搜索框', value=xpath_bd_search_input, action='input', content=kw_ch)
        self.browser.wait_element(desc='搜索按钮', value=xpath_bd_search_btn, action='click')
        self.browser.wait_element(desc='收起工具按钮', value=xpath_bd_close_tool_btn, action='click')
        element = self.browser.wait_element(desc='搜索结果数量', value=xpath_bd_result_count_text)
        res_count = int(re.findall(r'相关结果约(.*?)个', element.text)[0].replace(',', ''))
        print('搜索结果数量为:{}'.format(res_count))

    def test_002(self):
        """CASE02: 百度搜索英文关键字"""
        self.browser.open_url(url=base_url)
        self.browser.wait_element(desc='百度搜索框', value=xpath_bd_search_input, action='input', content=kw_en)
        self.browser.wait_element(desc='搜索按钮', value=xpath_bd_search_btn, action='click')
        self.browser.wait_element(desc='收起工具按钮', value=xpath_bd_close_tool_btn, action='click')
        element = self.browser.wait_element(desc='搜索结果数量', value=xpath_bd_result_count_text)
        res_count = int(re.findall(r'相关结果约(.*?)个', element.text)[0].replace(',', ''))
        print('搜索结果数量为:{}'.format(res_count))




        #     # 登录 - 进入BUP
        #     self.browser = PortalPage(self.browser)
        #     assert isinstance(self.browser, PortalPage)
        #     self.browser.login(user='root', psw='123456')
        #     self.browser.open_sub_system('统一用户管理')
        #     # 打开员工管理页面 - 添加新员工
        #     self.browser = BupUserMngPage(self.browser)
        #     assert isinstance(self.browser, BupUserMngPage)
        #     self.browser.open_sub_menu(menu_name='用户管理', item_name='用户管理')
        #     user_1 = ['自动化员工1_{}'.format(time_str), 'auto_test_1_{}'.format(time_str), '1_' + time_str]
        #     user_2 = ['自动化员工2_{}'.format(time_str), 'auto_test_2_{}'.format(time_str), '2_' + time_str]
        #     self.browser.add_new_user(people_name=user_1[0], username=user_1[1], work_id=user_1[2])
        #     self.browser.add_new_user(people_name=user_2[0], username=user_2[1], work_id=user_2[2])
        #     self.browser.search_user(search_key=time_str)
        #     # 进入工作组管理 - 新建工作组 - 添加成员 - 设置管理员
        #     self.browser = BupWorkGroupPage(self.browser)
        #     assert isinstance(self.browser, BupWorkGroupPage)
        #     self.browser.open_sub_menu(menu_name='用户管理', item_name='工作组管理')
        #     group_name = "工作组_{}".format(time_str)
        #     self.browser.add_new_work_group(group_name=group_name)
        #     self.browser.add_group_member(group_name=group_name, user_search_key=time_str)
        #     self.browser.set_admin(user_name=user_1[0])
        #     # 进入系统注册页面 - 新建系统
        #     self.browser = BupSysAddPage(self.browser)
        #     assert isinstance(self.browser, BupSysAddPage)
        #     self.browser.open_sub_menu(menu_name='系统配置', item_name='系统注册')
        #     sys_name = '自动化系统_{}'.format(time_str)
        #     self.browser.add_new_system(sys_name=sys_name, sys_uri=time_str)
        #     # 进入资源配置页面 - 配置首选项 - 配置菜单
        #     self.browser = BupSysConfigPage(self.browser)
        #     assert isinstance(self.browser, BupSysConfigPage)
        #     self.browser.open_sub_menu(menu_name='系统配置', item_name='资源配置')
        #     self.browser.select_system(sys_name)
        #     org_name = "主院区"
        #     self.browser.add_first_config(name=time_str, code=time_str, org_name=org_name)
        #     self.browser.add_menu(name="目录1", code=time_str + '_1', menu_type='菜单目录')
        #     self.browser.add_menu(name="目录2", code=time_str + '_2', menu_type='菜单目录')
        #     self.browser.add_menu(name="功能1", code=time_str + '_3', menu_type='菜单功能', parent_name='目录1')
        #     self.browser.add_menu(name="功能2", code=time_str + '_4', menu_type='菜单功能', parent_name='目录1')
        #     self.browser.add_menu(name="功能3", code=time_str + '_5', menu_type='菜单功能', parent_name='目录2')
        #     self.browser.add_menu(name="功能4", code=time_str + '_6', menu_type='菜单功能', parent_name='目录2')
        #     self.browser.add_menu(name="功能5", code=time_str + '_7', menu_type='菜单功能', parent_name='目录2')
        #     # 进入角色管理页面 - 为系统新建角色
        #     self.browser = BupRoleMngPage(self.browser)
        #     assert isinstance(self.browser, BupRoleMngPage)
        #     self.browser.open_sub_menu(menu_name='系统配置', item_name='角色配置')
        #     self.browser.select_system(sys_name=sys_name)
        #     menu_list = [('目录1', '功能1'), ('目录1', '功能2'), ('目录2', '功能5')]
        #     role_name = '自动化角色'
        #     self.browser.add_role(name=role_name, code='auto_test_{}'.format(time_str), menu_list=menu_list)
        #     # 进入管理员授权页面 - 为管理员授权
        #     self.browser = BupAuthAdminPage(self.browser)
        #     assert isinstance(self.browser, BupAuthAdminPage)
        #     self.browser.open_sub_menu(menu_name='分级授权', item_name='管理员授权')
        #     self.browser.auth_system_to_group(group_name=group_name, system_name=sys_name)
        #     # 进入员工授权页面 - 将bup的权限赋给管理员
        #     self.browser = BupAuthUserPage(self.browser)
        #     assert isinstance(self.browser, BupAuthUserPage)
        #     self.browser.open_sub_menu(menu_name='分级授权', item_name='用户授权')
        #     self.browser.auth_system_to_user(user_name=user_1[0], system_name='统一用户管理')
        #     # 登录管理员用户 - 进入BUP - 给组员授权
        #     self.browser.open_url(url=portal_url)
        #     self.browser = PortalPage(self.browser)
        #     assert isinstance(self.browser, PortalPage)
        #     self.browser.login(user=user_1[1], psw='123456')
        #     self.browser.check_system_list(['统一用户管理'])
        #     self.browser.open_sub_system('统一用户管理')
        #     self.browser = BupAuthUserPage(self.browser)
        #     assert isinstance(self.browser, BupAuthUserPage)
        #     self.browser.open_sub_menu(menu_name='分级授权', item_name='用户授权')
        #     self.browser.auth_system_to_user(user_name=user_2[0], system_name=sys_name)
        #     # 登录用户 - 检查系统权限 - 检查首选项 - 检查菜单
        #     self.browser.open_url(url=portal_url)
        #     self.browser = PortalPage(self.browser)
        #     assert isinstance(self.browser, PortalPage)
        #     self.browser.login(user=user_2[1], psw='123456')
        #     self.browser.check_system_list([sys_name])
        #     self.browser.open_sub_system(sys_name)
        #     self.browser = BupSysAddPage(self.browser)
        #     assert isinstance(self.browser, BupSysAddPage)
        #     self.browser.check_first_config(expect_list=[org_name])
        #     self.browser.select_first_config(item_name=org_name)
        #     self.browser.check_menu(menu_list)
        #     # 清除测试数据 (工作站、角色、首选项、工作组)
        #     self.browser = PortalPage(self.browser)
        #     assert isinstance(self.browser, PortalPage)
        #     self.browser.open_url(url=portal_url)
        #     self.browser.login(user='root', psw='123456')
        #     self.browser.open_sub_system("统一用户管理")
        #     # 清空角色
        #     self.browser = BupRoleMngPage(self.browser)
        #     assert isinstance(self.browser, BupRoleMngPage)
        #     self.browser.open_sub_menu(menu_name='系统配置', item_name='角色配置')
        #     self.browser.clear_system_roles(sys_name)
        #     # 清空首选项
        #     self.browser = BupSysConfigPage(self.browser)
        #     assert isinstance(self.browser, BupSysConfigPage)
        #     self.browser.open_sub_menu(menu_name='系统配置', item_name='资源配置')
        #     self.browser.delete_first_config(sys_name)
        #     self.browser.clear_system_menus(sys_name)
        #     # 删除系统
        #     self.browser = BupSysAddPage(self.browser)
        #     assert isinstance(self.browser, BupSysAddPage)
        #     self.browser.open_sub_menu(menu_name='系统配置', item_name='系统注册')
        #     self.browser.delete_system(sys_name)
        #     # 删除工作组
        #     self.browser = BupWorkGroupPage(self.browser)
        #     assert isinstance(self.browser, BupWorkGroupPage)
        #     self.browser.open_sub_menu(menu_name='用户管理', item_name='工作组管理')
        #     self.browser.delete_work_group(group_name=group_name)
        #
        # def test_002(self):
        #     """页面报错信息抓取 DEBUG"""
        #     console_errors = []
        #
        #     def add_logs(page_name):
        #         logs = self.browser.get_console_logs_by_level()
        #         for log in logs:
        #             log['page_name'] = page_name
        #             console_errors.append(log)
        #
        #     # 登录
        #     self.browser.open_url(url=portal_url)
        #     add_logs('登录页面')
        #     self.browser = PortalPage(self.browser)
        #     assert isinstance(self.browser, PortalPage)
        #     self.browser.login(user='2111', psw='123456')
        #     add_logs('PORTAL页面')
        #
        #     # 遍历工作站
        #     for sys_name in sys_list:
        #         self.browser.switch_to_window_by_title('威高云智')
        #         self.browser = PortalPage(self.browser)
        #         self.browser.open_sub_system(sys_name)
        #         self.browser = MenuBarPage(self.browser)
        #         assert isinstance(self.browser, MenuBarPage)
        #         try:
        #             self.browser.select_first_config(item_name='')
        #         except:
        #             print('---无首选项')
        #         time.sleep(5)
        #         add_logs(sys_name + '-首页')
        #         menu_bar_list = self.browser.get_all_menus_bars()
        #         # 遍历目录
        #         for menu_bar in menu_bar_list:
        #             menu_item_list = self.browser.get_all_menus(bar_name=menu_bar)
        #             # 遍历菜单项
        #             for item_name in menu_item_list:
        #                 self.browser.open_sub_menu(menu_name=menu_bar, item_name=item_name, switch_to_sub_frame=False)
        #                 time.sleep(3)
        #                 add_logs(sys_name + '-' + menu_bar + '-' + item_name)
        #
        #     for err_log in console_errors:
        #         print('<pre style="color:red">\n报错页面:{}\n{}\n</pre>'.format(err_log['page_name'], err_log['message']))
        #     # assert len(console_errors) == 0, '找到console报错日志'
        #     self.assertEqual(len(console_errors), 0, '找到console报错日志')
