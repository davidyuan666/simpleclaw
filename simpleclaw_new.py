#!/usr/bin/env python3
"""
SimpleClaw - Telegram 输入桥接
从 Telegram 接收命令，显示在终端，手动复制给 Claude
"""

import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "8419880332:AAGD8amX2_bISxNHua56rfWIvF7rkb3aDnU"
CHAT_ID = "751182377"
PROXY = "http://127.0.0.1:9788"
proxies = {'http': PROXY, 'https': PROXY}

class SimpleClaw:
    def __init__(self):
        self.running = True
        self.last_update_id = 0

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
        print("SimpleClaw - 手动桥接模式")
        print("=" * 50)
        print("等待 Telegram 命令...")
        print("=" * 50)
        self.send_telegram("✅ SimpleClaw 已启动（手动模式）")

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
                            print(f"\n{'='*50}")
                            print(f"[收到命令] {text}")
                            print(f"{'='*50}\n")
                            self.send_telegram(f"✅ 已接收: {text[:50]}...")
            except KeyboardInterrupt:
                self.running = False
                print("\n已停止")
            except Exception as e:
                print(f"错误: {e}")
                time.sleep(5)

if __name__ == "__main__":
    claw = SimpleClaw()
    claw.run()
