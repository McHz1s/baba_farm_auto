import time
from functools import partial

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy

from driver.baba_basic import BabaFarmBasic
from utils.appium_utils import get_into_app, \
    build_desired_capabilities

desired_capabilities = build_desired_capabilities()
print(desired_capabilities)


# def try_times(func):
#     def re_func(*args, **kwargs):


class Taobao(BabaFarmBasic):
    def __init__(self):
        super().__init__()
        self.button2desc.update(
            {'去完成': [
                '浏览15',
                '浏览最高',
            ]})
        self.button2desc.update({'去浏览': [
            '浏览15'
        ]})

    def browse_func_init(self):
        func_list = super().browse_func_init()
        func_list += [self.browse_sou_yi_sou]
        return func_list

    def get_into_baba_farm(self):
        # 设置等待时间为10秒
        wait = WebDriverWait(self.driver, 10)

        # 等待 content-desc 为 "芭芭农场" 的 FrameLayout 元素出现，并执行点击操作
        element = wait.until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "芭芭农场")))
        try:
            element.click()
        except:
            pass

    def get_into_app(self):
        get_into_app(self.driver, 'com.taobao.taobao', "com.taobao.tao.welcome.Welcome")

    def browse_sou_yi_sou(self):
        to_complet_buttons = self.find_element('button', '去完成')
        element_browse_good = self.find_element('view', f'搜一搜')
        self.browse(to_complet_buttons, element_browse_good, True)

    def click_gather_fertilizer(self):
        # 设置等待时间为10秒
        wait = WebDriverWait(self.driver, 10)

        # 等待 text 为 "集肥料" 的按钮元素出现，并执行点击操作
        element = wait.until(
            EC.presence_of_element_located(
                (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("集肥料")')))
        element.click()

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

