import os
import time
from functools import partial

from driver.baba_basic import BabaFarmBasic
from utils.appium_utils import get_into_app, \
    build_desired_capabilities, find_element, strBounds2list, click_elem_by_coor

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

desired_capabilities = build_desired_capabilities()
print(desired_capabilities)


# def try_times(func):
#     def re_func(*args, **kwargs):


class Alipay(BabaFarmBasic):
    def __init__(self):
        super().__init__()
        self.button2desc.update(
            {'去完成': [
                '逛15',
                '浏览15',
            ]})
        self.button2desc.update(
            {
                '去逛逛': [
                    '浏览15',
                    '连续浏览'
                ]
            }
        )

    def get_into_baba_farm(self):
        elem = find_element(self.driver, By.XPATH,
                            f"//android.widget.TextView[@text='芭芭农场']")[0]
        loc = elem.location
        self.click_coor(**loc)

    def get_into_app(self):
        get_into_app(self.driver, 'com.eg.android.AlipayGphone', "AlipayLogin")

    def click_gather_fertilizer(self):
        elem = find_element(self.driver, By.XPATH,
                            f"//android.widget.Button[@text='任务列表']", wait_time=10)[0]
        loc = elem.location
        self.click_coor(**loc)

    def click_msg(self):
        self.find_element('TextView', f'消息', do_click=True)
        time.sleep(1)

    def click_user_msg_box(self, user_name):
        self.find_element('TextView', f'{user_name}', do_click=True)
        time.sleep(2)

    def swipe_click_into_assist_page(self):
        assist_boxs = self.find_element('TextView', f'帮我助力，你也有奖励')
        for box in assist_boxs:
            click_elem_by_coor(box, self.driver)
            time.sleep(5)
            self.alipay_click_assist_right_now()
            time.sleep(1)
            self.driver.back()
            time.sleep(1)

    def alipay_click_assist_right_now(self):
        assist_rn = self.find_element('button', '为Ta助力', wait_time=1)[0]
        assist_rn.click()

    def click_assist_right_now(self):
        pass

    def auto_assist_user(self, user_name):
        self.click_msg()
        try:
            self.click_user_msg_box(user_name)
        except:
            return
        self.swipe_click_into_assist_page()
        self.click_assist_right_now()

    def auto_assist_all_users(self):
        for user_name in os.environ.get('USER_NAME').split():
            self.to_desktop()
            self.get_into_app()
            self.auto_assist_user(user_name)
