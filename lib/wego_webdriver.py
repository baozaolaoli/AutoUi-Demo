from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from lib.data_convert import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import os, time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config.common_config import headless, err_xpath
import platform

real_path = os.path.split(os.path.realpath(__file__))[0]

if platform.system().lower() == 'windows':
    driver_path = '{}{}chromedriver.exe'.format(real_path, os.sep)
else:  # linux
    driver_path = '{}{}chromedriver'.format(real_path, os.sep)
    cmd = 'chmod 777 {}'.format(driver_path)
    res = os.popen(cmd).read()
    print(cmd, '\n', res)


def open_browser(dp=driver_path, port=None):
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    if headless is True:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    if port is not None:
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(port))
    else:
        chrome_options.add_experimental_option('detach', True)
    new_driver = webdriver.Chrome(executable_path=dp, options=chrome_options, desired_capabilities=capabilities)
    if headless is True:
        new_driver.set_window_rect(0, 0, 1920, 1080)
    return new_driver


class Browser(object):
    def __init__(self, dp=driver_path, port=None):
        self.driver = open_browser(dp=dp, port=port)
        self.pic_path = '{}{}..{}report{}picture'.format(real_path, os.sep, os.sep, os.sep)
        if not os.path.exists(self.pic_path):
            os.mkdir(self.pic_path)

    def open_url(self, url):
        self.driver.get(url=url)

    def check_error_alert(self):
        err_eles = self.get_elements(by=By.XPATH, value=err_xpath)
        if err_eles:
            self.save_screen('发现报错_{}'.format(get_time_str()))
            err_msg = err_eles[0].get_attribute('textContent')
            assert False, '发现错误提示:{}'.format(err_msg)

    def check_error_alert_hold(self, time_out=10):
        t0 = time.time()
        while time.time() - t0 < time_out:
            self.check_error_alert()

    def get_elements(self, value, by=By.XPATH):
        time.sleep(0.1)
        ele_list = []
        element_list = self.driver.find_elements(by=by, value=value)
        for ele in element_list:
            if ele.is_displayed():
                ele_list.append(ele)
        return ele_list

    def wait_elements(self, value, by=By.XPATH, time_out=10):
        t0 = time.time()
        ele_list = []
        while not ele_list and time.time() - t0 < time_out:
            self.check_error_alert()
            ele_list = self.get_elements(by=by, value=value)
        return ele_list

    def wait_element(self, value, desc=None, by=By.XPATH, time_out=10, action=None, content='', send_enter=False):
        element_list = self.wait_elements(value=value, by=by, time_out=time_out)
        element = element_list[0] if element_list else None
        if element is None:
            print('没有找到元素{}({})'.format(desc, value))
        else:
            print('找到元素:{} ({})'.format(desc, value))
        if action is None:
            return element
        else:
            self.check_element(element, desc)
            if action == 'click':
                element.click()
            if action == 'input':
                try:
                    element.clear()
                except:
                    print('clear failed')
                    pass
                content = str(content)
                element.send_keys(content)
                if send_enter is True:
                    element.send_keys(Keys.ENTER)
            if action == 'move_to':
                ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(0.5)
        self.check_error_alert()
        return element

    def wait_element_not_exist(self, value, desc=None, by=By.XPATH, time_out=10):
        t0 = time.time()
        self.check_error_alert_hold(time_out=2)
        ele_list = True
        while ele_list and time.time() - t0 < time_out:
            self.check_error_alert()
            ele_list = self.get_elements(by=by, value=value)
        assert not ele_list, "等待元素消失超时: {}({})".format(desc, value)
        print("等待元素消失完成: {}({})".format(desc, value))

    def check_element(self, element, desc):
        assert element is not None, '等待元素{} 失败:{}'.format(desc, element)
        try:
            origin_style = element.get_attribute('style')
            self.set_element_attr(element, 'style', 'border:3px solid red;{}'.format(origin_style))
            self.save_screen('{}_{}'.format(desc, get_time_str(format='_%Y%m%d_%H_%M_%S')))
            time.sleep(0.5)
            self.set_element_attr(element, 'style', origin_style)
        except Exception as e:
            print('修改样式失败:{}'.format(str(e)))

    def set_element_attr(self, element, attr, value):
        self.execute_js("arguments[0].setAttribute('{}','{}')".format(attr, value), element)

    def execute_js(self, scriptStr, *args):
        return self.driver.execute_script(scriptStr, *args)

    def save_screen(self, file_name):
        try:
            file_path = '{}{}{}.png'.format(self.pic_path, os.sep, file_name)
            self.driver.save_screenshot(filename=file_path)
            print("<details><summary>▼{}</summary><img width=1400 height=800 src='{}.png'/></details>".format(file_name, file_name))
        except Exception as e:
            print('截图失败:{}'.format(str(e)))

    def switch_to_window_by_title(self, title, condition='eq'):
        time.sleep(3)
        window_list = self.driver.window_handles
        for win in window_list:
            self.driver.switch_to.window(win)
            if condition == 'contain':
                if title in self.driver.title:
                    return True
            else:
                if self.driver.title == title:
                    if headless is True:
                        self.driver.set_window_rect(0, 0, 1920, 1080)
                    return True
        assert False, '没有找到窗口标题为{}'.format(title)

    def get_console_logs(self):
        logs = self.driver.get_log('browser')
        self.execute_js('console.clear()')
        return logs

    def get_console_logs_by_level(self, level='SEVERE'):
        logs = self.get_console_logs()
        level_list = []
        for log in logs:
            if log.get('level') == level:
                level_list.append(log)
                print('find console log:\n{}\n'.format(log))
        return level_list

    def click_element(self, element, desc):
        assert isinstance(element, WebElement), '点击元素错误'
        self.check_element(element=element, desc=desc)
        element.click()


if __name__ == '__main__':
    bro = Browser()
    bro.open_url('https://www.baidu.com')
    bro.save_screen(file_name='test')
