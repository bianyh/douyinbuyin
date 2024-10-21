import subprocess


def run_streamlit_app():
    # 定义Streamlit脚本的路径
    streamlit_script = 'ui.py'

    # 使用subprocess.run来启动Streamlit脚本
    try:
        print(f"Starting Streamlit app: {streamlit_script}")
        result = subprocess.run(['streamlit', 'run', streamlit_script], check=True)
        print("Streamlit app has started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while starting the Streamlit app: {e}")


if __name__ == "__main__":
    run_streamlit_app()