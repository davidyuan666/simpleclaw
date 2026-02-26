#!/usr/bin/env python3
"""
SimpleClaw - 只接管输入，不接管输出
让 Claude 直接输出到终端
"""

import subprocess
import threading
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "8419880332:AAGD8amX2_bISxNHua56rfWIvF7rkb3aDnU"
CHAT_ID = "751182377"
PROXY = "http://127.0.0.1:9788"
proxies = {'http': PROXY, 'https': PROXY}

class ClaudeController:
    def __init__(self):
        self.process = None
        self.running = False
        self.last_update_id = 0

    def start_claude(self):
        """启动 Claude - 使用 echo 管道"""
        try:
            print("SimpleClaw 已启动")
            print("=" * 50)
            print("等待 Telegram 命令...")
            print("=" * 50)

            self.running = True
            self.send_telegram("✅ SimpleClaw 已启动")

        except Exception as e:
            print(f"启动失败: {e}")

    def send_input(self, text):
        """通过 echo 管道发送到 Claude"""
        try:
            import subprocess
            import shlex

            # 安全地转义文本，防止命令注入
            escaped_text = text.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

            print(f"\n{'='*50}")
            print(f"[执行] {text}")
            print(f"{'='*50}\n")

            # Windows 使用不同的命令格式
            if subprocess.os.name == 'nt':
                # Windows: 使用临时文件方式更可靠
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                    f.write(text)
                    temp_file = f.name

                try:
                    cmd = f'type "{temp_file}" | claude --dangerously-skip-permissions --print'
                    result = subprocess.run(cmd, shell=True, timeout=60)
                finally:
                    import os
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
            else:
                # Unix/Linux: 使用 echo
                cmd = f'echo "{escaped_text}" | claude --dangerously-skip-permissions --print'
                result = subprocess.run(cmd, shell=True, timeout=60)

            print(f"\n{'='*50}")
            print(f"[完成] 返回码: {result.returncode}")
            print(f"{'='*50}\n")

            return True
        except Exception as e:
            print(f"执行失败: {e}")
            return False

    def send_telegram(self, message):
        """发送消息到 Telegram"""
        for i in range(3):  # 重试3次
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = {'chat_id': CHAT_ID, 'text': message}
                response = requests.post(url, json=data, proxies=proxies, timeout=10, verify=False)
                if response.json().get('ok'):
                    return True
            except Exception as e:
                if i == 2:  # 最后一次才打印错误
                    print(f"Telegram发送失败: {e}")
                time.sleep(1)
        return False

    def get_telegram_updates(self):
        """获取 Telegram 更新"""
        for i in range(3):  # 重试3次
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
                params = {'offset': self.last_update_id + 1, 'timeout': 30}
                response = requests.get(url, params=params, proxies=proxies, timeout=35, verify=False)
                data = response.json()
                if data.get('ok'):
                    return data.get('result', [])
            except Exception as e:
                if i == 2:  # 最后一次才打印错误
                    print(f"获取更新失败: {e}")
                time.sleep(1)
        return []

    def process_telegram_message(self, message):
        """处理 Telegram 消息"""
        text = message.get('text', '')

        if text.startswith('/'):
            if text == '/status':
                status = "🟢 运行中" if self.running else "🔴 已停止"
                self.send_telegram(f"状态: {status}")
            elif text == '/stop':
                self.stop()
            elif text == '/help':
                self.send_telegram("SimpleClaw\n\n直接发送文本将发送给 Claude\n/status - 状态\n/stop - 停止")
        else:
            # 发送给 Claude
            if self.send_input(text):
                self.send_telegram(f"✅ 已发送: {text[:50]}...")
                print(f"[发送] {text}")

    def telegram_listener(self):
        """监听 Telegram 消息"""
        while self.running:
            try:
                updates = self.get_telegram_updates()
                for update in updates:
                    self.last_update_id = update['update_id']
                    if 'message' in update:
                        self.process_telegram_message(update['message'])
            except Exception as e:
                print(f"监听错误: {e}")
                time.sleep(5)

    def stop(self):
        """停止"""
        self.running = False
        if self.process:
            self.process.terminate()
        print("已停止")

    def run(self):
        """运行主循环"""
        self.start_claude()
        threading.Thread(target=self.telegram_listener, daemon=True).start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


if __name__ == "__main__":
    print("SimpleClaw - 只接管输入版本")
    print("=" * 50)
    controller = ClaudeController()
    controller.run()
