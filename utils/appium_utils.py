import re
import subprocess

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


def build_desired_capabilities():
    device_info = get_device_info()
    if device_info:
        device_name = device_info
        udid = device_info
        platform_version = "6.0.1"  # 你可以根据实际情况更改
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


def click_coor(driver, x, y):
    # 创建TouchAction对象
    action = TouchAction(driver)

    # 在屏幕上点击指定坐标
    action.tap(x=x, y=y).perform()


def get_size(driver: WebDriver = None):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return [x, y]


def swipe_up(driver: WebDriver = None, _time: int = 20000):
    if not driver:
        return False
    try:
        size = get_size(driver)
        x1 = int(size[0] * 0.5)  # 起始x坐标
        y1 = int(size[1] * 0.80)  # 起始y坐标
        y2 = int(size[1] * 0.30)  # 终点y坐标
        driver.swipe(x1, y1, x1, y2, _time)
        return True
    except:
        return False


def to_desktop(driver, back_time):
    for i in range(back_time):
        driver.back()
        if i != back_time - 1:
            time.sleep(0.5)


def get_into_app(driver: WebDriver, app_pkg: str, app_page: str):
    try:
        driver.start_activity(f'{app_pkg}', f"{app_page}")
    except:
        pass


def find_element(driver: WebDriver, by_type: str, prop: str, wait_time=0.1):
    wait = WebDriverWait(driver, wait_time)
    elements = wait.until(
        EC.visibility_of_all_elements_located((by_type, prop)))
    return elements


def strBounds2list(bounds):
    import re
    pattern = r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]'
    matches = re.findall(pattern, bounds)
    numbers = [int(num) for match in matches for num in match]
    return numbers


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