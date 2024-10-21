import pandas as pd
import streamlit as st

import task
from src import driver

# 检查函数是否已经在会话状态中
if 'function_executed' not in st.session_state:
    # 设置应用的布局为宽模式
    st.set_page_config(layout="wide")
    st.write('正在初始化中，请稍后......')
    # 执行函数
    a = task.Task()

    # 将结果存储在会话状态中

    st.session_state.function_executed = a
    st.experimental_rerun()

else:
    # 如果函数已经执行过，直接从会话状态获取结果
    a = st.session_state.function_executed



# 定义函数
def get_video_list(time_to_sort, category, sort_by, max_num):
    '''
    :param time_to_sort: 1,2,3,4分别对应1小时，24小时，1周，1个月
    :param category: 1,2分别对应销量榜和热度榜
    :param sort_by: 传入所需选择的类目文本即可
    :param max_num: 获取最上面的多少数量的数据
    :return: DataFrame
    '''
    try:
        # 这里可以添加你的逻辑代码
        progress = st.progress(0)
        progress_bar = st.empty()  # 创建一个占位符用于显示进度条
        percent_text = st.empty()  # 创建一个占位符用于显示百分比数字

        for percent in a.get_video_list(time_to_sort, category, sort_by, max_num):
            p = percent / max_num
            progress.progress(p)  # 更新进度条
            percent_text.metric("进度", f"{p*100}%")  # 更新百分比数字


        df = pd.DataFrame(a.data)
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# 在侧边栏创建功能选择
with st.sidebar:

    st.title('功能选择')
    # 功能选择栏
    function_options = ['视频榜单设置', '话题榜单设置']
    selected_function = st.selectbox('选择功能', function_options)


# 初始化session state变量
if 'show_execute_button' not in st.session_state:
    st.session_state.show_execute_button = False





if selected_function == '视频榜单设置':
    with st.sidebar:
        st.title('视频榜单设置')

        # 时间选择栏
        time_options = {'1小时': 1, '24小时': 2, '1周': 3, '1个月': 4}
        time_to_sort = st.selectbox('选择时间范围', list(time_options.keys()), format_func=lambda x: x)

        # 类别选择栏
        category_options = {'销量榜': 1, '热度榜': 2}
        category = st.radio('选择类别', list(category_options.keys()), format_func=lambda x: x)

        # 排序依据选择栏
        sort_by_options = [
            '智能家居', '食品饮料', '个护家清', '服饰内衣', '美妆',
            '图书教育', '母婴宠物', '运动户外', '生鲜', '3C数码家电',
            '鞋靴箱包', '钟表配饰', '礼品文创', '玩具乐器', '珠宝文玩',
            '鲜花园艺', '本地生活'
        ]
        sort_by = st.selectbox('排序依据', sort_by_options)

        # 最大数量选择栏
        max_num = st.slider('选择最大数量', min_value=1, max_value=100, value=10)

    params = (time_to_sort, category, sort_by, max_num)

    if 'df' not in st.session_state or 'params' not in st.session_state or st.session_state.params != params:
        if st.button('查询'):
            st.write('正在查询中！')
            st.session_state.df = get_video_list(time_to_sort, category, sort_by, max_num)
            st.session_state.params = params

    df = st.session_state.get('df', None)

    if df is not None:
        st.write(df)

        # 一键下载所有选中视频
        if st.button("下载所有视频"):
            # 创建一个进度条
            progress_bar = st.progress(0)
            total_videos = len(df)

            for i, (index, row) in enumerate(df.iterrows()):
                video_url = row['Video URL']
                try:
                    driver.download_video(video_url, f'..//download//video//{row["Video Name"]}.mp4')
                    st.success(f"视频下载完成: download//video//{row["Video Name"]}.mp4")
                    # 下载成功后，从选中列表中移除
                    if index in st.session_state.selected_rows:
                        st.session_state.selected_rows.remove(index)
                except Exception as e:
                    st.error(f"下载失败: {row['Video Name']} - 错误: {e}")

                # 更新进度条
                progress = (i + 1) / total_videos
                progress_bar.progress(progress)

            st.success("所有视频下载完成！")

        if 'selected_rows' not in st.session_state:
            st.session_state.selected_rows = []

        selected_rows = st.multiselect('选择视频进行下载', df.index, default=st.session_state.selected_rows)
        st.session_state.selected_rows = selected_rows

        if selected_rows:
            selected_df = df.loc[selected_rows]

            # 一键下载所有选中视频
            if st.button("下载所有选中的视频"):
                # 创建一个进度条
                progress_bar = st.progress(0)
                total_videos = len(selected_df)

                for i, (index, row) in enumerate(selected_df.iterrows()):
                    video_url = row['Video URL']
                    try:
                        driver.download_video(video_url, f'..//download//video//{row["Video Name"]}.mp4')
                        st.success(f"视频下载完成: download//video//{row["Video Name"]}.mp4")
                        # 下载成功后，从选中列表中移除
                        if index in st.session_state.selected_rows:
                            st.session_state.selected_rows.remove(index)
                    except Exception as e:
                        st.error(f"下载失败: {row['Video Name']} - 错误: {e}")

                    # 更新进度条
                    progress = (i + 1) / total_videos
                    progress_bar.progress(progress)

                st.success("所有视频下载完成！")


            # 单个视频下载
            for index, row in selected_df.iterrows():
                video_url = row['Video URL']
                if st.button(f"下载视频: {row['Video Name']}"):  # 触发下载按钮
                    driver.download_video(video_url, f'..//download//video//{row["Video Name"]}.mp4')
                    st.success(f"视频下载完成: download//video//{row["Video Name"]}.mp4")
                    # 下载成功后，从选中列表中移除
                    if index in st.session_state.selected_rows:
                        st.session_state.selected_rows.remove(index)







if selected_function == '话题榜单设置':
    with st.sidebar:
        st.title('话题榜单设置')

        # 最大数量选择栏
        position = st.slider('选择话题榜第几位', min_value=1, max_value=10, value=1)

        if st.button('寻找'):
            st.write('稍等...')
            # 这里不再重新获取 category，因为我们已经存储在 session state 中了
            if 'category' not in st.session_state:
                # 如果 session state 中没有 category，那么获取并存储它
                st.session_state.category = a.get_topic_list_category(position, None)

        if 'category' in st.session_state:
            sort_by = st.selectbox('具体类目', st.session_state.category)
            # 最大数量选择栏
            max_num = st.slider('选择最大数量', min_value=1, max_value=100, value=10)
            # 设置session state变量，以便显示执行按钮
            st.session_state.show_execute_button = True


    if st.session_state.show_execute_button:
        if st.button('开始查询'):
            st.write('正在查询中！')


            # 这里可以添加你的逻辑代码
            progress = st.progress(0)
            progress_bar = st.empty()  # 创建一个占位符用于显示进度条
            percent_text = st.empty()  # 创建一个占位符用于显示百分比数字

            # 使用存储在 session state 中的 category 来获取数据
            for percent in a.get_topic_list_data(st.session_state.category, max_num):
                p = percent / max_num
                progress.progress(p)  # 更新进度条
                percent_text.metric("进度", f"{p * 100}%")  # 更新百分比数字

            if a.topic_data is not None:
                st.write(pd.DataFrame(a.topic_data))
