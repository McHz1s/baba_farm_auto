from functools import partial

from driver.baba_basic import AppiumDemo
from utils.appium_utils import get_into_app, \
    build_desired_capabilities, find_element, strBounds2list

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

desired_capabilities = build_desired_capabilities()
print(desired_capabilities)


# def try_times(func):
#     def re_func(*args, **kwargs):


class Alipay(AppiumDemo):
    def __init__(self):
        super().__init__()
        self.button2desc.update(
            {'去完成': [
                '逛15',
                '浏览15',
                # '逛好物最高得2000肥料',
                # '看精选商品得1500肥料',
                # '逛织金助农好货领肥料',
                # '逛助农好货得肥料'
            ]})
        self.button2desc.update(
            {
                '去逛逛': [
                    '浏览15',
                ]
            }
        )
        # self.button2desc.update({'去浏览': ['浏览金币小镇得肥料']})

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
