import os
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

from utils.appium_utils import click_coor, get_size, swipe_up, to_desktop, get_into_app, \
    find_element, build_desired_capabilities, strBounds2list

desired_capabilities = build_desired_capabilities()
print(desired_capabilities)


# def try_times(func):
#     def re_func(*args, **kwargs):


class AppiumDemo(object):
    def __init__(self):
        self.button2desc = defaultdict(list)
        self.driver = webdriver.Remote(command_executor=desired_capabilities['command_executor'],
                                       desired_capabilities=desired_capabilities)
        self.by = mobileby.MobileBy()
        self.try_time = 1

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
        return click_coor(self.driver, x, y)

    def get_size(self):
        return get_size(self.driver)

    def swipe_up(self, swipe_time: int = 20000):
        return swipe_up(self.driver, swipe_time)

    def to_desktop(self, back_time=20):
        to_desktop(self.driver, back_time)

    def get_into_app(self):
        raise NotImplementedError

    def browse_func_init(self):
        func_list = []
        for key_button, desc_list in self.button2desc.items():
            cur_func_list = [partial(self.browse_guan_hao_huo,
                                     item_desc=desc, to_complete_text=key_button)
                             for desc in desc_list]
            func_list.extend(cur_func_list)
        return func_list

    def execute(self, seed):
        self.to_desktop()
        self.get_into_app()
        self.get_into_baba_farm()
        if os.environ.get('GATHER', '0') == '1':
            while 1:
                time.sleep(2)
                self.click_and_gather()
                time.sleep(1)
                self.driver.back()
                time.sleep(1)
                self.get_into_baba_farm()
                time.sleep(1)
        self.click_gather_fertilizer()
        func_list = self.browse_func_init()
        while self.try_time >= 0:
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
            if flag == 0:
                self.swipe_up(1000)
                self.try_time -= 1

    def swipe_and_back(self):
        self.swipe_up()  # 向上滑动
        self.driver.back()

    def click_gather_fertilizer(self):
        raise  NotImplementedError # 设置等待时间为10秒

    def find_element(self, type_str, text):
        mapping = {'view': 'view.View', 'button': 'widget.Button'}
        elem = find_element(self.driver, By.XPATH,
                            f"//android.{mapping[type_str]}[contains(@text, '{text}')]",
                            wait_time=10)
        return elem

    def browse(self, finish_buttons, target_descs, if_search=False):
        for desc in target_descs:
            browse_good_bound = strBounds2list(target_descs.get_attribute('bounds'))
            for button in finish_buttons:
                bounds = strBounds2list(button.get_attribute('bounds'))
                if abs(bounds[-1] - browse_good_bound[-1]) > 80 or \
                        (bounds[-1] > 2000 and self.try_time <= 0):
                    continue
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
        raise ModuleNotFoundError

    def browse_guan_hao_huo(self, item_desc, to_complete_text='去完成'):
        to_complet_buttons = self.find_element('button', f'{to_complete_text}')
        element_browse_goods = self.find_element('view', f'{item_desc}')
        self.browse(to_complet_buttons, element_browse_goods)

    def browse_sou_yi_sou(self):
        to_complet_buttons = self.find_element('button', '去完成')
        element_browse_good = self.find_element('view', f'搜一搜你喜欢的商品')[0]
        self.browse(to_complet_buttons, element_browse_good, True)

    def click_and_gather(self):
            self.click_coor(x=549, y=1868)
            # time.sleep(1)
            # self.click_coor(x=554, y=1463)
            # time.sleep(1)
            # self.click_coor(525, 1463)
            # time.sleep(1)
            # self.click_coor(551, 1551)
            time.sleep(1)