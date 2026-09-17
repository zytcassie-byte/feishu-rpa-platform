import os
import lark_oapi as lark
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

if not APP_ID or not APP_SECRET:
    raise ValueError("请先在 .env 中设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET")

client = lark.Client.builder() \
    .app_id(APP_ID) \
    .app_secret(APP_SECRET) \
    .log_level(lark.LogLevel.INFO) \
    .build()


def send_message(receive_id: str, content: str, receive_id_type: str = "chat_id"):
    """发送文本消息"""
    from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
    request = CreateMessageRequest.builder() \
        .receive_id_type(receive_id_type) \
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("text")
            .content(lark.JSON.marshal({"text": content}))
            .build()
        ).build()
    response = client.im.v1.message.create(request)
    if response.success():
        print(f"消息发送成功，message_id: {response.data.message_id}")
    else:
        print(f"消息发送失败，code: {response.code}, msg: {response.msg}")
    return response


def get_bitable_records(app_token: str, table_id: str):
    """读取多维表格记录"""
    from lark_oapi.api.bitable.v1 import ListAppTableRecordRequest
    request = ListAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .page_size(100) \
        .build()
    response = client.bitable.v1.app_table_record.list(request)
    if response.success():
        return response.data.items
    else:
        print(f"读取失败: {response.msg}")
        return []


def update_bitable_record(app_token: str, table_id: str, record_id: str, fields: dict):
    """更新多维表格记录"""
    from lark_oapi.api.bitable.v1 import UpdateAppTableRecordRequest, AppTableRecord
    request = UpdateAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .record_id(record_id) \
        .request_body(AppTableRecord.builder().fields(fields).build()) \
        .build()
    response = client.bitable.v1.app_table_record.update(request)
    if response.success():
        print("记录更新成功")
    else:
        print(f"记录更新失败: {response.msg}")
    return response