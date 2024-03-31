from functools import partial

from driver.baba_basic import BabaFarmBasic
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


class Alipay(BabaFarmBasic):
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

    def click_msg(self):
        msg_box = self.find_element('frame', f'消息')[0]
        msg_box.click()
        time.sleep(1)

    def click_user_msg_box(self, user_name):
        msg_box = self.find_element('view', user_name, 'content-desc')[0]
        msg_box.click()
        time.sleep(2)

    def swipe_click_into_assist_page(self):
        assist_box = self.find_element('frame', '拜托帮我助力一下吧～你也可以领免费水果！')[0]
        assist_box.click()
        time.sleep(2)

    def click_assist_right_now(self):
        assist_rn = self.find_element('button', '立即助力')[0]
        assist_rn.click()

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
