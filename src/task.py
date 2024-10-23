# -*- coding: utf-8 -*-
import logging
import time

import pandas as pd
import pyperclip
from selenium.webdriver.common.by import By
from tqdm import tqdm

import driver
from loguru import logger
from datetime import datetime

# 获取当前时间并格式化为字符串，格式为 YYYY-MM-DD
current_time = datetime.now().strftime("%Y-%m-%d")

# 配置loguru日志记录器，将日志保存到 log 目录下，并以当前日期为文件名
logger.add(f"../log/task_log_{current_time}.txt", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO")


class Task:
    def __init__(self):
        url = 'https://buyin.jinritemai.com/mpa/account/login'
        self.driver = driver.Driver()
        # a.get_cookie(url)
        self.driver.open_browser_with_cookie(url)
        # #self.driver.shut_popups(".browser-blocker-plugin-modal-content", ".browser-blocker-plugin-footer span")
        # self.driver.shut_popups("div.auxo-modal-content", "button.index_module__button____4693")
        # self.driver.scroll_up_and_down(200, -100)
        # self.driver.click_button_and_jump('div', "index__moreVideo____9474", 1)

        self.driver.driver.get('https://buyin.jinritemai.com/dashboard/inspiration-center/hot-video')


        self.data = {}
        self.topic_data = {}

    def get_video_list(self, time_to_sort, category, sort_by, max_num):
        '''
        :param time: 1,2,3,4分别对应1小时，24小时，1周，1个月
        :param category: 1,2分别对应销量榜和热度榜
        :param sort_by: 传入所需选择的类目文本即可
        :param max_num: 获取最上面的多少数量的数据
        :return:
        '''
        video_name = [] #视频名
        commodity_name = [] # 商品名
        time_of_video = [] # 视频时间
        length_of_video = [] # 视频时长
        video_url = [] # 视频链接
        up_name = [] # up名
        total_plays = [] # 总播放量
        sales = [] # 销售量
        deals = [] # 成交量
        stars = [] # 点赞量
        price = [] # 价格
        commission = [] # 佣金
        positive_rating = [] # 好评率
        sold_num = [] # 出售量
        up_num = [] # 带货人数
        commodity_link = [] # 商品链接


        self.driver.click_button_with_keyword('span', '爆款视频', 1)
        if time_to_sort == '1小时':
            self.driver.click_button_with_keyword('div', '近1小时', 1)
        elif time_to_sort == '24小时':
            pass
            #self.driver.click_button_with_keyword('div', '近24小时', 1)
        elif time_to_sort == '1周':
            self.driver.click_button_with_keyword('div', '近1周', 1)
        elif time_to_sort == '1个月':
            self.driver.click_button_with_keyword('div', '近1个月', 1)
        else:
            logger.error('time_to_sort must be in 4 options')


        if category == '销量榜':
            self.driver.click_button_with_keyword('div', '新增销售额', 1)
        elif category == '热度榜':
            self.driver.click_button_with_keyword('div', '新增播放量', 1)
        else:
            logger.error('category must be 1 or 2')



        self.driver.click_button_with_keyword('span', sort_by, 1)


        self.driver.click_button('div', 'index_module__valueItem____42a3', 1)



        count = self.driver.canculate_nums('index_module__videoCard_item____03f9', max_num)

        # 使用tqdm创建进度条
        for i in tqdm(range(count), desc="循环进度"):
            # 执行常规操作
            logger.info(f"执行榜单数据查询... {i + 1}")

            video_name.append(self.driver.get_text('div', 'index_module__videoName____03f9', i+1))
            commodity_name.append(self.driver.get_text('div', 'index_module__singleProductsName____03f9', i+1))
            time_of_video.append(self.driver.get_text('div', 'index_module__startTime____03f9', i+1))
            length_of_video.append(self.driver.get_text('div', 'index_module__endTime____03f9', i + 1))
            up_name.append(self.driver.get_text('div', 'index_module__authorName____03f9', i+1))

            total_plays.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+1).replace('\n',' ')))

            sales.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+2).replace('\n',' ')))

            deals.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+3).replace('\n',' ')))

            stars.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+4).replace('\n',' ')))

            self.driver.scroll_up_and_down(-100000, 0)
            self.driver.click_button('div', 'index_module__startIcon____03f9', i+1)
            url = self.driver.find_elements('div', 'index_module__videoPlayer___af17d', "src", 1)
            self.driver.click_button('img', 'index_module__closeButton___b0824', 1) # 关闭视频
            video_url.append(url)

            self.driver.click_button_and_jump('div', 'index_module__singleProductsName____03f9', i+1)
            price.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 1))
            commission.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 2))
            positive_rating.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 3))
            sold_num.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 4))
            up_num.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 5))
            self.driver.click_button_with_keyword('div', '复制链接', 1)
            commodity_link.append(pyperclip.paste())
            # 关闭当前标签页
            self.driver.driver.close()

            # 切换回上一个标签页
            self.driver.driver.switch_to.window(self.driver.driver.window_handles[0])



            yield  i+1

        self.data.update({
            'Commodity Name': commodity_name,
            'Time of Video': time_of_video,
            'Length of Video': length_of_video,
            'UP Name': up_name,
            'Video Name': video_name,
            'Total Plays': total_plays,
            'Sales': sales,
            'Deals': deals,
            'Stars': stars,
            'Video URL': video_url,
            'Price': price,
            'Commission': commission,
            'Positive Rating': positive_rating,
            'Sold Number': sold_num,
            'Up Number': up_num,
            'Commodity Link': commodity_link
        })

        return



    def get_video_list_fast(self, time_to_sort, category, sort_by, max_num):
        '''
        :param time: 1,2,3,4分别对应1小时，24小时，1周，1个月
        :param category: 1,2分别对应销量榜和热度榜
        :param sort_by: 传入所需选择的类目文本即可
        :param max_num: 获取最上面的多少数量的数据
        :return:
        '''
        video_name = [] #视频名
        commodity_name = [] # 商品名
        time_of_video = [] # 视频时间
        length_of_video = [] # 视频时长
        video_url = [] # 视频链接
        up_name = [] # up名
        total_plays = [] # 总播放量
        sales = [] # 销售量
        deals = [] # 成交量
        stars = [] # 点赞量
        price = [] # 价格
        commission = [] # 佣金
        positive_rating = [] # 好评率
        sold_num = [] # 出售量
        up_num = [] # 带货人数
        commodity_link = [] # 商品链接


        self.driver.click_button_with_keyword('span', '爆款视频', 1)
        if time_to_sort == '1小时':
            self.driver.click_button_with_keyword('div', '近1小时', 1)
        elif time_to_sort == '24小时':
            pass
            #self.driver.click_button_with_keyword('div', '近24小时', 1)
        elif time_to_sort == '1周':
            self.driver.click_button_with_keyword('div', '近1周', 1)
        elif time_to_sort == '1个月':
            self.driver.click_button_with_keyword('div', '近1个月', 1)
        else:
            logger.error('time_to_sort must be in 4 options')


        if category == '销量榜':
            self.driver.click_button_with_keyword('div', '新增销售额', 1)
        elif category == '热度榜':
            self.driver.click_button_with_keyword('div', '新增播放量', 1)
        else:
            logger.error('category must be 1 or 2')



        self.driver.click_button_with_keyword('span', sort_by, 1)


        self.driver.click_button('div', 'index_module__valueItem____42a3', 1)



        count = self.driver.canculate_nums('index_module__videoCard_item____03f9', max_num)

        # 使用tqdm创建进度条
        for i in tqdm(range(count), desc="循环进度"):
            # 执行常规操作
            logger.info(f"执行榜单数据查询... {i + 1}")

            video_name.append(self.driver.get_text('div', 'index_module__videoName____03f9', i+1))
            commodity_name.append(self.driver.get_text('div', 'index_module__singleProductsName____03f9', i+1))
            time_of_video.append(self.driver.get_text('div', 'index_module__startTime____03f9', i+1))
            length_of_video.append(self.driver.get_text('div', 'index_module__endTime____03f9', i + 1))
            up_name.append(self.driver.get_text('div', 'index_module__authorName____03f9', i+1))

            total_plays.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+1).replace('\n',' ')))

            sales.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+2).replace('\n',' ')))

            deals.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+3).replace('\n',' ')))

            stars.append((self.driver.get_text('div', 'index_module__totalData____03f9',i*4+4).replace('\n',' ')))

            self.driver.scroll_up_and_down(-100000, 0)
            self.driver.click_button('div', 'index_module__startIcon____03f9', i+1)
            url = self.driver.find_elements('div', 'index_module__videoPlayer___af17d', "src", 1)
            self.driver.click_button('img', 'index_module__closeButton___b0824', 1) # 关闭视频
            video_url.append(url)

            # self.driver.click_button_and_jump('div', 'index_module__singleProductsName____03f9', i+1)
            # price.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 1))
            # commission.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 2))
            # positive_rating.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 3))
            # sold_num.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 4))
            # up_num.append(self.driver.get_text('div', 'index_module__dataContent____0bd5', 5))
            # self.driver.click_button_with_keyword('div', '复制链接', 1)
            # commodity_link.append(pyperclip.paste())
            # # 关闭当前标签页
            # self.driver.driver.close()
            #
            # # 切换回上一个标签页
            # self.driver.driver.switch_to.window(self.driver.driver.window_handles[0])

            yield  i+1

        self.data.update({
            'Commodity Name': commodity_name,
            'Time of Video': time_of_video,
            'Length of Video': length_of_video,
            'UP Name': up_name,
            'Video Name': video_name,
            'Total Plays': total_plays,
            'Sales': sales,
            'Deals': deals,
            'Stars': stars,
            'Video URL': video_url,
            # 'Price': price,
            # 'Commission': commission,
            # 'Positive Rating': positive_rating,
            # 'Sold Number': sold_num,
            # 'Up Number': up_num,
            # 'Commodity Link': commodity_link
        })

        return



    def download_data(self, path):
        # 使用pandas创建DataFrame
        df = pd.DataFrame(self.data)

        # 将DataFrame写入CSV文件
        df.to_csv(path, index=False, encoding='utf-8-sig')
        logger.info(f'data saved to csv file {path}')

    def download_video(self, path):
        i = 0
        for url in self.data['Video URL']:
            driver.download_video(url, path+str(i)+'.mp4')
            i += 1



    def get_topic_list_category(self, position, sort_by):
        '''

        :param position: 话题榜的第几个
        :param sort_by: 分类类目
        :return:
        '''
        self.driver.click_button_with_keyword('span', '热点话题', 1)
        # self.driver.move_and_wait('button', 'auxo-tabs-nav-more', 1)
        # self.driver.move_and_wait('span', 'auxo-dropdown-trigger', 1)
        # self.driver.click_button_with_keyword('div', sort_by, 1)
        self.driver.click_button('div', 'index_module__topicTitle____70a3', position)
        time.sleep(3)
        # 查找相应元素
        elements = self.driver.driver.find_elements(By.XPATH, "//div[contains(@class,'index_module__valueItem____42a3')]")
        # 统计数量
        count = len(elements)
        category = []
        for i in range(count):
            category.append(self.driver.get_text('div', 'index_module__valueItem____42a3', i + 1))
        return category

    def get_topic_list_data(self, category, max_num):
        self.driver.click_button_with_keyword('div', category, 1)

        count = self.driver.canculate_nums('index_module__videoCardContainer____6017', max_num)

        topic_video_name = []
        topic_sales = []
        # 使用tqdm创建进度条
        for i in tqdm(range(count), desc="循环进度"): # 执行常规操作
            num = i*2
            topic_video_name.append(self.driver.get_text('div', 'index_module__commodityInfo____6017', num + 1))
            topic_sales.append(self.driver.get_text('div', 'index_module__commodityInfo____6017', num + 2).replace('\n', ' '))
            yield i+1

        self.topic_data.update({
            'Topic Name': topic_video_name,
            'Sales': topic_sales,
        })

        return




if __name__ == '__main__':
    a = Task()
    a.get_video_list(3,1,'本地生活',2)
    a.download_data('..//download//data//test.csv')
    # #a.download_video('..//download//video//test')
    # wait = input('don\'t complete')
    # cate = a.get_topic_list_category(2, '本地生活')
    # a.get_topic_list_data('服饰内衣', 2)
    input()

