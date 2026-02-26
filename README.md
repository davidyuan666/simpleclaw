# SimpleClaw

通过 Telegram 远程控制 Claude Code 的轻量级桥接工具

## 核心架构

SimpleClaw 的核心思路是**接管 Claude Code 的 stdin 和 stdout**，通过 Telegram Bot 实现远程交互：

```
Telegram Bot <---> SimpleClaw <---> Claude Code (stdin/stdout)
```

### 工作原理

1. **输入接管**: 从 Telegram 接收命令，通过管道或文件传递给 Claude Code 的 stdin
2. **输出透传**: Claude Code 的 stdout 直接显示在终端，保持原生体验
3. **状态同步**: 关键操作通过 Telegram 反馈执行状态

## 三种实现模式

### 1. 自动模式 (simpleclaw.py)
直接通过管道将 Telegram 命令发送给 Claude Code

```bash
python simpleclaw.py
```

**特点**:
- 全自动执行
- Windows 使用临时文件，Unix 使用 echo 管道
- 防命令注入保护

### 2. 手动模式 (simpleclaw_new.py)
在终端显示 Telegram 命令，手动复制给 Claude

```bash
python simpleclaw_new.py
```

**特点**:
- 人工审核每条命令
- 适合敏感操作
- 完全可控

### 3. 文件桥接模式 (simpleclaw_bridge.py)
将 Telegram 命令写入文件，通过文件与 Claude 通信

```bash
python simpleclaw_bridge.py
```

**特点**:
- 异步通信
- 命令持久化
- 便于调试

## 快速开始

### 安装依赖

```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

### 启动

```bash
# Windows
start.bat

# Linux/Mac
python simpleclaw.py
```

## Telegram 命令

- `/status` - 查看运行状态
- `/stop` - 停止服务
- `/help` - 帮助信息
- 直接发送文本 - 发送给 Claude Code

## 配置

编辑脚本中的配置：

```python
BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
PROXY = "http://127.0.0.1:9788"  # 可选代理
```

## 注意事项

- 必须在外部终端运行，不能在 Claude Code 内部运行
- 确保 Claude Code CLI 已安装并在 PATH 中
- Windows 系统会使用临时文件方式传递命令
- 代理配置根据网络环境调整

## 技术栈

- Python 3.7+
- requests - HTTP 请求
- urllib3 - HTTP 客户端
- Telegram Bot API

## 安全性

- 命令注入防护
- 文本转义处理
- 临时文件自动清理
- SSL 证书验证可选

## License

MIT
