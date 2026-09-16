"""
飞书事件处理 - 长连接模式
功能：接收用户发给机器人的消息，并自动回复一条固定文本
"""

import os
from dotenv import load_dotenv
load_dotenv()
import lark_oapi as lark
from lark_oapi.api.im.v1 import (
    P2ImMessageReceiveV1,
    CreateMessageRequest,
    CreateMessageRequestBody,
)

# ========== 1. 从环境变量读取飞书应用凭证 ==========
APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

if not APP_ID or not APP_SECRET:
    raise ValueError(
        "请先在环境变量中设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET\n"
        "或在项目根目录创建 .env 文件并填写"
    )

# ========== 2. 创建飞书客户端 ==========
client = lark.Client.builder() \
    .app_id(APP_ID) \
    .app_secret(APP_SECRET) \
    .log_level(lark.LogLevel.DEBUG) \
    .build()


# ========== 3. 处理接收到的消息 ==========
def do_message_receive(data: P2ImMessageReceiveV1) -> None:
    """收到用户消息时触发"""
    print("=" * 50)
    print("收到消息事件！")
    print(f"事件数据: {lark.JSON.marshal(data)}")

    # 获取消息相关信息
    event = data.event
    message = event.message
    chat_id = message.chat_id
    message_type = message.message_type
    message_id = message.message_id

    # 只处理文本消息
    if message_type != "text":
        print(f"非文本消息，暂不处理: {message_type}")
        return

    # 解析文本内容
    try:
        import json
        content = json.loads(message.content)
        text = content.get("text", "")
        print(f"用户发送的文本: {text}")
    except Exception as e:
        print(f"解析消息内容失败: {e}")
        return

    # ========== 4. 回复消息 ==========
    reply_text = f"收到你的消息啦！你说的是：{text}"

    # 构建回复内容
    reply_content = {"text": reply_text}

    # 构建请求
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type("text")
            .content(lark.JSON.marshal(reply_content))
            .build()
        ) \
        .build()

    # 发送回复
    response = client.im.v1.message.create(request)

    if response.success():
        print(f"回复成功，消息ID: {response.data.message_id}")
    else:
        print(f"回复失败，错误码: {response.code}, 错误信息: {response.msg}")


# ========== 5. 注册事件处理器 ==========
event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_message_receive) \
    .build()


# ========== 6. 启动长连接客户端 ==========
def main():
    print("正在启动飞书长连接客户端...")
    ws_client = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.DEBUG,
    )
    print("长连接客户端已启动，等待消息中...")
    ws_client.start()


if __name__ == "__main__":
    main()