# -*- coding: utf-8 -*-
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Driver:
    def __init__(self):
            self.get_browser()

    def get_browser(self):
        # 设置ChromeDriver的路径
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 129.0.0.0Safari / 537.36"')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())

        # 创建一个Chrome浏览器实例
        self.driver = webdriver.Chrome(service=service, options=options)
        return



    def get_cookie(self,url):
        self.driver.get(url)  # 替换为实际的登录页面URL
        # 手动登录后，获取Cookie
        a = input("等待登录")
        cookies = self.driver.get_cookies()
        with open('cookies.json', 'w') as file:
            json.dump(cookies, file)

    def open_browser_with_cookie(self, url,cookie_path = 'cookies.json'):
        self.driver.get(url)
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                # Selenium要求Cookie的expiry时间必须为整数，如果不是，则转换为整数
                if 'expiry' in cookie and isinstance(cookie['expiry'], float):
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        self.driver.refresh()  # 刷新页面以使Cookie生效

        return

    # noinspection PyUnreachableCode
    def shut_popups(self, element, button):
        try:
            # 设置等待时间
            wait = WebDriverWait(self.driver, 10)  # 等待最多10秒

            # 等待直到元素加载完成
            modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))

            # 检查按钮是否存在并且可见
            button = self.driver.find_element(By.CSS_SELECTOR, button)

            # 如果按钮存在且可见，则点击按钮
            if button.is_displayed():
                button.click()
                print("按钮已点击")
            else:
                print("按钮不可见或不存在")
            return

        except Exception as e:
            print(f"发生错误：{e}")

        finally:
            pass

    def scroll_up_and_down(self, up_pixels, down_pixels):
        """
        模拟鼠标上下滑动操作。

        :param driver: Selenium WebDriver对象
        :param up_pixels: 向上滑动的像素值
        :param down_pixels: 向下滑动的像素值
        :return: 操作后的driver对象
        """
        try:
            # 等待页面加载完成
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # 向上滑动
            self.driver.execute_script(f"window.scrollBy(0, {up_pixels});")
            # 等待一下，确保页面滚动完成
            self.driver.implicitly_wait(1)

            # 向下滑动
            self.driver.execute_script(f"window.scrollBy(0, {down_pixels});")
            # 等待一下，确保页面滚动完成
            self.driver.implicitly_wait(1)

            print("已模拟上下滑动")

        except Exception as e:
            print(f"发生错误：{e}")

        return


    def click_button(self, button_selector):
        """
        定位并点击“更多”按钮，并在新标签页中切换窗口。

        :param button_selector: 按钮的CSS选择器
        """
        try:
            # 等待“更多”按钮出现
            more_videos_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )

            # 点击“更多”按钮
            more_videos_button.click()
            print("已点击按钮")

            # 等待新窗口出现
            original_window = self.driver.current_window_handle  # 保存当前窗口句柄
            WebDriverWait(self.driver, 10).until(
                lambda driver: len(driver.window_handles) > 1  # 等待直到有多个窗口
            )

            # 切换到新标签页
            for handle in self.driver.window_handles:
                if handle != original_window:  # 找到新窗口的句柄
                    self.driver.switch_to.window(handle)
                    print("已切换到新标签页")
                    break

        except Exception as e:
                print(f"发生错误：{e}")

    def get_text(self, where_text):
        """
        获取视频信息元素的文本内容。

        :param driver: Selenium WebDriver对象
        :return: 视频信息的文本内容
        """

        try:
            time.sleep(2)
            # 使用CSS选择器查找第一个匹配的元素
            element = self.driver.find_element(By.XPATH, "//div[@class='index_module__videoName____03f9']")
            print(element.text)  # 打印元素的文本内容

            element = self.driver.find_element(By.XPATH, "//div[@class='index_module__dataNumber____03f9']")
            print(element.text)  # 打印元素的文本内容
            element = self.driver.find_element(By.XPATH, "//div[@class='index_module__dataNumberLarge___fac0b']")
            print(element.text)  # 打印元素的文本内容
            element = self.driver.find_element(By.XPATH, "//div[@class='index_module__growData___ef986']")
            print(element.text)  # 打印元素的文本内容

            return element.text
        except Exception as e:
            print(f"发生错误：{e}")
            return None


if __name__ == '__main__':
    url = 'https://buyin.jinritemai.com/mpa/account/login'
    a = Driver()
    # a.get_cookie(url)
    a.open_browser_with_cookie(url)
    a.shut_popups(".browser-blocker-plugin-modal-content", ".browser-blocker-plugin-modal-footer span")
    a.shut_popups("div.auxo-modal-content", "button.index_module__button____4693")
    a.scroll_up_and_down(200, -100)
    a.click_button("button.auxo-btn.auxo-btn-link .index__moreVideo____9474")
    text = a.get_text("div.index_module__videoName____03f9")

    wait = input('don\'t complete')
    # driver = come_to_mainframe(driver)

