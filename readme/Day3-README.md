# Day 3 开发记录

## 1. 飞书消息发送
- 基于飞书 Python SDK 实现 `send_message()`
- 支持向群聊（chat_id）或用户（open_id）发送文本消息

## 2. 多维表格读写
- `get_bitable_records()`：读取多维表格记录
- `update_bitable_record()`：更新指定记录的字段
- 已通过测试：能读取订单号、订单状态，并能更新状态字段

## 3. 相关文件
- `backend/app/feishu/feishu_client.py`
- `backend/app/feishu/test_feishu.py`
- `backend/app/feishu/test_bitable.py`