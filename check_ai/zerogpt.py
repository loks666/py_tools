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
                "input_text": current_text
            }

            try:
                # 发送POST请求
                response = requests.post("https://api.zerogpt.com/api/detect/detectText", json=data)

                if response.status_code == 200:
                    response_data = response.json()
                    print("接口返回结果:")
                    print(json.dumps(response_data, indent=4, ensure_ascii=False))

                    # 提取并输出feedback值
                    feedback = response_data.get('data', {})
                    if feedback is None:
                        print("未找到反馈信息")
                    else:
                        feedback = feedback.get('feedback', '未找到反馈信息')
                        print(f"反馈信息: {feedback}")
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
