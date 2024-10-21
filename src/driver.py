# -*- coding: utf-8 -*-
import json
import os
import random
import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class Driver:
    def __init__(self):
        self.get_browser()


    def get_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.page_load_strategy = 'eager'
        options.add_argument("--mute-audio")

        # options.add_argument('--headless')

        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('useAutomationExtension', False)
        service = Service('./chromedriver.exe')
        self.driver = webdriver.Chrome(options=options, service=service)
        # self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #     Object.defineProperty(navigator, 'webdriver', {
        #     get: () => undefined
        #     })
        #     """
        # })
        return

    def get_cookie(self, url):
        self.driver.get(url)
        a = input("等待登录")
        cookies = self.driver.get_cookies()
        with open('cookies.json', 'w') as file:
            json.dump(cookies, file)

    def open_browser_with_cookie(self, url, cookie_path='cookies.json'):
        self.driver.get(url)
        with open(cookie_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                if 'expiry' in cookie and isinstance(cookie['expiry'], float):
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def get_element_with_class(self, type, name, section=1):
        try:
            span_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"(//{type}[contains(@class, '{name}')])[{section}]")))
            return span_element
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def get_element_with_keyword(self, type, name, section=1):
        try:
            span_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"(//{type}[contains(text(), '{name}')])[{section}]")))
            return span_element
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def full_xpath_find(self, path):
        try:
            span_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, path)))
            return span_element
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def shut_popups(self, element, button):
        try:
            modal = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
            button = self.driver.find_element(By.CSS_SELECTOR, button)
            if button.is_displayed():
                button.click()
                logger.info("按钮已点击")
            else:
                logger.warning("按钮不可见或不存在")
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def scroll_up_and_down(self, up_pixels, down_pixels):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.driver.execute_script(f"window.scrollBy(0, {up_pixels});")
            self.driver.implicitly_wait(1)
            self.driver.execute_script(f"window.scrollBy(0, {down_pixels});")
            self.driver.implicitly_wait(1)
            logger.info("已模拟上下滑动")
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def click_button_and_jump(self, type, button_selector, section=1):
        # 生成一个0.1到0.2之间的随机浮点数
        delay = random.uniform(0.1, 0.2)

        # 打印延迟时间
        print(f"Delaying for {delay} seconds...")

        # 延迟指定的时间
        time.sleep(delay)

        try:
            button = self.get_element_with_class(type, button_selector, section)
            button.click()
            logger.info("已点击按钮")
            WebDriverWait(self.driver, 10).until(lambda driver: len(driver.window_handles) > 1)
            new_window_handles = self.driver.window_handles[1:]
            self.driver.switch_to.window(new_window_handles[-1])
            logger.info("已切换到新标签页")
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def click_button(self, type, button_selector, section=1):
        # 生成一个0.1到0.2之间的随机浮点数
        delay = random.uniform(0.1, 0.2)

        # 打印延迟时间
        logger.info(f"Delaying for {delay} seconds...")

        # 延迟指定的时间
        time.sleep(delay)

        try:
            span_element = self.get_element_with_class(type, button_selector, section)
            span_element.click()
            logger.info("已点击按钮")
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def click_button_with_keyword(self, type, key_word, section=1):
        # 生成一个0.1到0.2之间的随机浮点数
        delay = random.uniform(0.1, 0.2)

        # 打印延迟时间
        print(f"Delaying for {delay} seconds...")

        # 延迟指定的时间
        time.sleep(delay)

        try:
            span_element = self.get_element_with_keyword(type, key_word, section)
            span_element.click()
            logger.info(f"已点击按钮{key_word}")
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def get_text(self, type, where_text, section=1):
        try:
            element = self.get_element_with_class(type, where_text, section)
            logger.info(f"获取到文本：{element.text}")
            return element.text
        except Exception as e:
            logger.error(f"发生错误：{e}")
            return None

    def find_elements_with_full_xpath(self, where_to_find, what_to_find='src', section=1):
        try:
            video_img_element = self.full_xpath_find(where_to_find)
            video_link = video_img_element.get_attribute(what_to_find)
            logger.info(f"视频链接：{video_link}")
            return video_link
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def find_elements(self, type, where_to_find, what_to_find='src', section=1):
        try:
            span_element = self.get_element_with_class(type, where_to_find, section)
            video_element = span_element.find_element(By.TAG_NAME, "video")
            video_src = video_element.get_attribute(what_to_find)
            logger.info(video_src)
            return video_src
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def move_and_wait(self, type, where_to_move, section=1):
        try:
            span_element = self.get_element_with_class(type, where_to_move, section)
            # 创建ActionChains实例
            actions = ActionChains(self.driver)

            # 移动鼠标到元素上并悬停
            actions.move_to_element(span_element).perform()
            return
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def move_and_wait_with_keyword(self, type, where_to_move, section=1):
        try:
            span_element = self.get_element_with_keyword(type, where_to_move, section)
            # 创建ActionChains实例
            actions = ActionChains(self.driver)

            # 移动鼠标到元素上并悬停
            actions.move_to_element(span_element).perform()
            return
        except Exception as e:
            logger.error(f"发生错误：{e}")

    def canculate_nums(self, class_index, max_num):
        # 查找相应元素
        elements = self.driver.find_elements(By.XPATH, f"//div[contains(@class,'{class_index}')]")
        # 统计数量
        count = len(elements)
        cishu = 0
        while count < max_num and cishu <= 50:
            self.scroll_up_and_down(100, 0)
            time.sleep(0.1)
            elements = self.driver.find_elements(By.XPATH,
                                                        f"//div[contains(@class,'{class_index}')]")
            last_count = count
            count = len(elements)
            if last_count == count:
                cishu += 1

        count = min(count, max_num)
        logger.info(f'可以获取榜单中前{count}个数据')
        return count

def download_video(video_url, path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with requests.head(video_url) as response:
            if response.status_code == 200:
                file_size = int(response.headers.get('content-length', 0))
            else:
                logger.error(f"无法获取视频大小，状态码：{response.status_code}")
                return
        with requests.get(video_url, stream=True) as response:
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Downloading") as bar:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            bar.update(len(chunk))
                logger.info(f"视频已下载到：{path}")
            else:
                logger.error(f"视频下载失败，状态码：{response.status_code}")
    except Exception as e:
        logger.error(f"下载视频时发生错误：{e}")



if __name__ == '__main__':
    url = 'https://buyin.jinritemai.com/mpa/account/login'
    a = Driver()

    a.get_cookie(url)

    # a.open_browser_with_cookie(url)
    # a.driver.get('https://buyin.jinritemai.com/dashboard/inspiration-center/hot-video')

    # a.shut_popups(".browser-blocker-plugin-modal-content", ".browser-blocker-plugin-modal-footer span")
    # a.shut_popups("div.auxo-modal-content", "button.index_module__button____4693")
    # a.scroll_up_and_down(200, -100)
    # a.click_button_and_jump('div', "index__moreVideo____9474", 1)
    # a.click_button_with_keyword('span', '本地生活', 1)
    # text = a.get_text("div", "index_module__totalData____03f9", 1)
    # print(text)
    # a.click_button_and_jump('div', 'index_module__singleProductsName____03f9',1)
    # a.get_text('div', 'index_module__dataContent____0bd5')
    wait = input('don\'t complete')