#!/usr/bin/env python3
"""
SimpleClaw - 文件桥接方案
通过文件与 Claude 通信
"""

import os
import time
import requests
import urllib3
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "8419880332:AAGD8amX2_bISxNHua56rfWIvF7rkb3aDnU"
CHAT_ID = "751182377"
PROXY = "http://127.0.0.1:9788"
proxies = {'http': PROXY, 'https': PROXY}

# 工作目录
WORK_DIR = Path(__file__).parent / "bridge"
INPUT_FILE = WORK_DIR / "input.txt"
OUTPUT_FILE = WORK_DIR / "output.txt"

class SimpleClaw:
    def __init__(self):
        WORK_DIR.mkdir(exist_ok=True)
        self.running = True
        self.last_update_id = 0

        # 清空文件
        INPUT_FILE.write_text("", encoding='utf-8')
        OUTPUT_FILE.write_text("", encoding='utf-8')

    def send_telegram(self, message):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {'chat_id': CHAT_ID, 'text': message}
            requests.post(url, json=data, proxies=proxies, timeout=10, verify=False)
        except Exception as e:
            print(f"发送失败: {e}")

    def get_updates(self):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {'offset': self.last_update_id + 1, 'timeout': 30}
            response = requests.get(url, params=params, proxies=proxies, timeout=35, verify=False)
            data = response.json()
            if data.get('ok'):
                return data.get('result', [])
        except Exception as e:
            print(f"获取更新失败: {e}")
        return []

    def run(self):
        print("SimpleClaw - 文件桥接模式")
        print("=" * 50)
        print(f"输入文件: {INPUT_FILE}")
        print(f"输出文件: {OUTPUT_FILE}")
        print("=" * 50)
        self.send_telegram("✅ SimpleClaw 已启动（文件桥接模式）")

        while self.running:
            try:
                updates = self.get_updates()
                for update in updates:
                    self.last_update_id = update['update_id']
                    if 'message' in update:
                        text = update['message'].get('text', '')
                        if text == '/stop':
                            self.running = False
                            print("已停止")
                            self.send_telegram("🛑 已停止")
                        elif text:
                            # 写入输入文件
                            INPUT_FILE.write_text(text, encoding='utf-8')
                            print(f"\n{'='*50}")
                            print(f"[写入] {text}")
                            print(f"{'='*50}\n")
                            self.send_telegram(f"✅ 已写入文件: {text[:50]}...")
            except KeyboardInterrupt:
                self.running = False
                print("\n已停止")
            except Exception as e:
                print(f"错误: {e}")
                time.sleep(5)

if __name__ == "__main__":
    claw = SimpleClaw()
    claw.run()
