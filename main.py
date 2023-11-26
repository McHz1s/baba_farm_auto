import time
from collections import defaultdict

from appium import webdriver
from appium.webdriver.common import mobileby
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functools import wraps, partial

import subprocess
import re


# 获取设备信息
def get_device_info():
    adb_output = subprocess.check_output("adb devices", shell=True).decode("utf-8")
    devices = re.findall(r"(\S+)\s+device", adb_output)
    if devices:
        return devices[1]
    else:
        return None


# 获取应用信息
def get_app_info(package_name, app_activity):
    app_info = {
        'appPackage': package_name,
        'appActivity': app_activity
    }
    return app_info


def retry_n(n, sleep=1):
    def retry_wrapper(func):
        def re_func(*args, **kwargs):
            cnt = 0
            try:
                func(*args, **kwargs)
            except:
                if cnt == n:
                    return
                cnt += 1
                time.sleep(sleep)

        return re_func
    return retry_wrapper

# 构建desired_capabilities字典
def build_desired_capabilities():
    device_info = get_device_info()
    if device_info:
        device_name = device_info
        udid = device_info
        platform_version = "6.0.1"  # 你可以根据实际情况更改
        app_info = get_app_info("com.taobao.taobao", "com.taobao.tao.welcome.Welcome")  # 你的应用程序信息
        desired_capabilities = {
            'platformName': 'Android',
            'deviceName': device_name,
            'platformVersion': platform_version,
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'dontStopAppOnReset': True,
            'autoGrantPermissions': True,
            'noReset': True,
            'automationName': 'uiautomator2',
            'newCommandTimeout': '36000',
            'systemPort': '8202',
            'udid': udid,
            'command_executor': 'http://127.0.0.1:4723/wd/hub'  # Appium服务器地址
        }
        # desired_capabilities.update(app_info)
        return desired_capabilities
    else:
        return None


desired_capabilities = build_desired_capabilities()
print(desired_capabilities)


# def try_times(func):
#     def re_func(*args, **kwargs):


class AppiumDemo(object):
    def __init__(self):
        self.driver = webdriver.Remote(command_executor=desired_capabilities['command_executor'],
                                       desired_capabilities=desired_capabilities)
        self.by = mobileby.MobileBy()

    def wait_find_element(self, by_type: str, value: str, driver: WebDriver = None):
        """
        获取单个元素, 显式等待
        :param driver: 驱动对象
        :param by_type: 查找元素的操作
        :param value: 查找元素的方法
        :return:
        """
        driver = driver or self.driver
        if not driver:
            return driver
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(locator=(by_type, value)))
            return driver.find_element(by_type, value)
        except:
            # self.logger.warning(traceback.format_exc())
            return False

    def click_coor(self, x, y):
        # 创建TouchAction对象
        action = TouchAction(self.driver)

        # 在屏幕上点击指定坐标
        action.tap(x=x, y=y).perform()


    def get_size(self, driver: WebDriver = None):
        driver = driver or self.driver
        if not driver:
            return driver

        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        return [x, y]

    def swipe_up(self, driver: WebDriver = None, _time: int = 20000):
        driver = driver or self.driver
        if not driver:
            return driver
        try:
            size = self.get_size(driver)
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.80)  # 起始y坐标
            y2 = int(size[1] * 0.30)  # 终点y坐标
            driver.swipe(x1, y1, x1, y2, _time)
            return True
        except:
            return False

    def to_desktop(self):
        back_time = 20
        for i in range(back_time):
            self.driver.back()
            if i != back_time - 1:
                time.sleep(0.5)

    def get_into_taobao(self):
        try:
            self.driver.start_activity('com.taobao.taobao', "com.taobao.tao.welcome.Welcome")
        except:
            pass

    def execute(self, seed):
        self.to_desktop()
        self.get_into_taobao()
        self.get_into_baba_farm()
        self.click_gather_fertilizer()
        button2desc = defaultdict(list)
        button2desc.update({'去完成': ['逛精选好货', '逛精选好物', '逛逛养生保健品', '浏览趣味视频得现金']})
        button2desc.update({'去浏览': ['浏览金币小镇得肥料']})
        func_list = []
        for key_button, desc_list in button2desc.items():
            cur_func_list = [partial(self.browse_guan_hao_huo,
                                     item_desc=desc, to_complete_text=key_button)
                             for desc in desc_list]
            func_list.extend(cur_func_list)
        func_list += [self.browse_sou_yi_sou]
        flag = len(func_list)
        while flag:
            flag = 0
            for func in func_list:
                while 1:
                    try:
                        func()
                        flag += 1
                    except:
                        break

    def swipe_and_back(self):
        self.swipe_up()  # 向上滑动
        self.driver.back()

    def get_into_baba_farm(self):
        # 设置等待时间为10秒
        wait = WebDriverWait(self.driver, 10)

        # 等待 content-desc 为 "芭芭农场" 的 FrameLayout 元素出现，并执行点击操作
        element = wait.until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "芭芭农场")))
        element.click()

    def click_gather_fertilizer(self):
        # 设置等待时间为10秒
        wait = WebDriverWait(self.driver, 10)

        # 等待 text 为 "集肥料" 的按钮元素出现，并执行点击操作
        element = wait.until(
            EC.presence_of_element_located(
                (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("集肥料")')))
        element.click()

    def find_element(self, type_str, text):
        wait = WebDriverWait(self.driver, 10)
        mapping = {'view': 'view.View', 'button': 'widget.Button'}
        elements = wait.until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   f"//android.{mapping[type_str]}[contains(@text, '{text}')]")))
        return elements

    def browse(self, finish_buttons, target_button, if_search=False):
        browse_good_bound = self.strBounds2list(target_button.get_attribute('bounds'))
        for button in finish_buttons:
            bounds = self.strBounds2list(button.get_attribute('bounds'))
            if abs(bounds[-1] - browse_good_bound[-1]) <= 80:
                button.click()
                if if_search:
                    try:
                        self.find_element('button', '搜索')
                        self.click_coor(x=546, y=632)
                    except:
                        self.driver.back()
                self.swipe_and_back()
                if if_search:
                    time.sleep(1)
                    self.driver.back()
                return

    def browse_guan_hao_huo(self, item_desc, to_complete_text='去完成'):
        to_complet_buttons = self.find_element('button', f'{to_complete_text}')
        element_browse_good = self.find_element('view', f'{item_desc}')[0]
        self.browse(to_complet_buttons, element_browse_good)

    def browse_sou_yi_sou(self):
        to_complet_buttons = self.find_element('button', '去完成')
        element_browse_good = self.find_element('view', f'搜一搜你喜欢的商品')[0]
        self.browse(to_complet_buttons, element_browse_good, True)

    def strBounds2list(self, bounds):
        import re
        pattern = r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]'
        matches = re.findall(pattern, bounds)

        numbers = [int(num) for match in matches for num in match]
        return numbers


@retry_n(5)
def main():
    seed = {
        'keyword': 'Python 书'
    }
    spider = AppiumDemo()
    while True:
        spider.execute(seed=seed)


if __name__ == '__main__':
    main()
