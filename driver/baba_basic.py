import os
import time
from collections import defaultdict
from functools import partial

from appium import webdriver
from appium.webdriver.common import mobileby
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.appium_utils import click_coor, get_size, swipe_up, to_desktop, find_element, build_desired_capabilities, \
    strBounds2list, click_elem_by_coor

desired_capabilities = build_desired_capabilities()
print(desired_capabilities)


# def try_times(func):
#     def re_func(*args, **kwargs):


class BabaFarmBasic(object):
    def __init__(self):
        self.button2desc = defaultdict(list)
        self.driver = webdriver.Remote(command_executor=desired_capabilities['command_executor'],
                                       desired_capabilities=desired_capabilities)
        self.by = mobileby.MobileBy()
        self.try_time = 1
        valid_user_name = None

    def wait_find_element(self, by_type: str, value: str, driver: WebDriver = None):
        """
        获取单个元素, 显式等待
        :param driver: 驱动对象
        :param by_type: 查找元素的操作
        :param value: 查找元素的方法vsd
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
        for i in range(back_time):
            self.back()
            if i != back_time - 1:
                time.sleep(0.1)

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

    def auto_gather(self):
        while 1:
            time.sleep(2)
            self.click_and_gather()
            time.sleep(1)
            self.driver.back()
            time.sleep(1)
            self.get_into_baba_farm()
            time.sleep(1)

    def auto_browse(self):
        self.to_desktop()
        self.get_into_app()
        self.get_into_baba_farm()
        self.click_gather_fertilizer()
        func_list = self.browse_func_init()
        while self.try_time >= 0:
            flag = len(func_list)
            while flag:
                flag = 0
                for func in func_list:
                    try:
                        func()
                        flag += 1
                    except:
                        continue

    def execute(self, seed):
        if os.environ.get('GATHER', '0') == '1':
            self.auto_gather()
        elif os.environ.get('USER_NAME', None) is not None:
            self.auto_assist_all_users()
        else:
            self.auto_browse()

    def swipe_and_back(self):
        self.swipe_up()  # 向上滑动
        self.back()

    def click_gather_fertilizer(self):
        raise NotImplementedError  # 设置等待时间为10秒

    def find_element(self, xpath_type, text, attribute_type='text', do_click=False, wait_time=0.1):
        xpath_map = {'view': 'view.View', 'button': 'widget.Button', 'edittext': 'widget.EditText'}
        EC_mapping = {'frame'}
        if xpath_type in ['TextView']:
            elem = find_element(self.driver, By.XPATH,
                                f"//android.widget.TextView[@text='{text}']")
            if do_click:
                click_elem_by_coor(elem[0], self.driver)
                Warning("has multiple elem but set auto click, click the first")
            return elem
        if xpath_type in xpath_map or xpath_type.lower() in xpath_map:
            prop = f"//android.{xpath_map[xpath_type.lower()]}"
            if text is not None:
                prop += f"[contains(@{attribute_type}, '{text}')]"
            elem = find_element(self.driver, By.XPATH,
                                prop,
                                wait_time=wait_time)
        else:
            elem = find_element(self.driver, MobileBy.ACCESSIBILITY_ID, text)
        if do_click:
            click_elem_by_coor(elem[0], self.driver)
            Warning("has multiple elem but set auto click, click the first")
        return elem

    def browse(self, finish_buttons, target_descs, if_search=False):
        for desc in target_descs:
            browse_good_bound = strBounds2list(desc.get_attribute('bounds'))
            for button in finish_buttons:
                bounds = strBounds2list(button.get_attribute('bounds'))
                if abs(bounds[-1] - browse_good_bound[-1]) > 80 or \
                        (bounds[-1] > 2000 and self.try_time > 0):
                    continue
                button.click()
                search_flag = False
                if if_search:
                    try:
                        search_button = self.find_element('button', '搜索', do_click=False)[0]
                        edit_button = self.find_element('edittext', None)[0]
                        edit_button.send_keys('dd')
                        time.sleep(1)
                        search_button.click()
                    except:
                        pass
                self.swipe_up()
                try:
                    self.find_element('button', '取消', do_click=True)
                except:
                    pass
                self.back_until_elem_found('button', '去完成')

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

    def auto_assist_all_users(self):
        for u_i, user_name in enumerate(os.environ.get('USER_NAME').split()):
            self.to_desktop()
            self.get_into_app()
            self.auto_assist_user(user_name)

    def back(self):
        try:
            back_button = self.find_element('Button', '返回')[0]
            back_button.click()
        except:
            self.driver.back()

    def back_until_elem_found(self, *find_elem_args, **find_elem_kwargs):
        elem = None
        while elem is None:
            try:
                elem = self.find_element(*find_elem_args, **find_elem_kwargs)
            except:
                elem = None
            if elem is None:
                self.back()
