"""
API 调用示例 — 分别用 SDK 和原始 HTTP 两种方式调用 Anthropic Claude API。
核心概念: API 密钥管理、HTTP 请求/响应、Token 计费。
AI 对应: 调用 LLM API 是构建 AI Agent、聊天机器人的基础技能。
"""
import os
import json
import urllib.request


def call_with_sdk():
    """使用 Anthropic SDK 调用 Claude API（推荐方式）。"""
    try:
        import anthropic
    except ImportError:
        print("Install the SDK: pip install anthropic")  # SDK 未安装
        return

    client = anthropic.Anthropic()  # 自动从环境变量读取密钥
    response = client.messages.create(
        model="claude-sonnet-4-20250514",  # 指定模型
        max_tokens=256,  # 最大输出 token 数
        messages=[{"role": "user", "content": "What is a neural network in one sentence?"}]  # 用户消息
    )
    print(f"SDK response: {response.content[0].text}")  # 打印模型回复
    print(f"Tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out")  # Token 用量


def call_raw_http():
    """使用原始 HTTP 请求调用 Claude API（理解底层原理）。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")  # 从环境变量获取密钥
    if not api_key:
        print("Set ANTHROPIC_API_KEY environment variable first")  # 密钥未设置
        return

    url = "https://api.anthropic.com/v1/messages"  # API 端点
    headers = {
        "Content-Type": "application/json",  # JSON 格式
        "x-api-key": api_key,  # 密钥认证
        "anthropic-version": "2023-06-01",  # API 版本
    }
    body = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
    }).encode()  # 编码为字节

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")  # 构造 POST 请求
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())  # 解析 JSON 响应
        print(f"Raw HTTP response: {result['content'][0]['text']}")  # 打印回复
        print(f"Tokens used: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")  # Token 用量


if __name__ == "__main__":
    print("=== API Calls ===\n")
    print("1. Using the SDK:")  # 方式一: 使用 SDK
    call_with_sdk()
    print("\n2. Using raw HTTP:")  # 方式二: 原始 HTTP
    call_raw_http()
