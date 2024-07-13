import json
import sys
import time

import pyperclip
import requests


def check_clipboard():
    last_text = pyperclip.paste()
    print("程序运行中，选中文本并复制以发送请求...")

    while True:
        time.sleep(1)
        current_text = pyperclip.paste()
        if current_text != last_text:
            print("检测到新的剪贴板内容...")
            print(f"读取到的文本: {current_text}")

            # 定义要发送的请求数据
            data = {
                "document": current_text,
                "source": "landing",
                "writing_stats_required": True,
                "sampleTextSubmitted": False,
                "interpretability_required": False,
                "checkPlagiarism": False
            }

            try:
                # 发送POST请求
                response = requests.post("https://api.gptzero.me/v2/predict/text", json=data)

                if response.status_code == 200:
                    response_data = response.json()
                    print("接口返回结果:")
                    print(json.dumps(response_data, indent=4, ensure_ascii=False))

                    # 提取并输出result_message值
                    documents = response_data.get('documents', [])
                    if documents:
                        result_message = documents[0].get('result_message', '未找到result_message信息')
                        print(f"反馈信息: {result_message}")
                    else:
                        print("未找到documents信息")
                else:
                    print(f"请求失败，状态码: {response.status_code}")
                    response_data = response.json()
                    print("错误信息:")
                    print(json.dumps(response_data, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"请求过程中出现异常: {e}")

            last_text = current_text


if __name__ == "__main__":
    try:
        check_clipboard()
    except KeyboardInterrupt:
        print("程序已终止。")
        sys.exit(0)
