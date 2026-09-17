# Day 3 开发记录

## 1. 飞书消息发送

### 目标
用飞书 Python SDK 实现机器人发送文本消息，为后续 RPA 执行结果通知做准备。

### 操作
- 安装 `lark-oapi` 和 `python-dotenv`
- 新建 `backend/app/feishu/feishu_client.py`
- 实现 `send_message()` 函数，支持向群聊（chat_id）或用户（open_id）发送文本消息

### 结论
- 飞书群能正常收到机器人发送的消息

## 2. 多维表格读写

### 目标
用飞书 SDK 读取和更新多维表格的记录，为后续把 RPA 执行结果回写到飞书表格做准备。

### 操作
- 在 `feishu_client.py` 中实现：
  - `get_bitable_records(app_token, table_id)`：读取多维表格记录
  - `update_bitable_record(app_token, table_id, record_id, fields)`：更新指定记录的字段
- 新建 `test_bitable.py` 进行测试

### 遇到的问题及解决
- `FieldNameNotFound`：代码里字段名和表格实际列名不一致
  - 解决：先打印 `records[0].fields.keys()`，用实际字段名更新
- `TableIdNotFound`：应用没有被添加为多维表格的协作者
  - 解决：在表格右上角 → 更多 → 添加文档应用 → 添加为"可编辑"
- `bitable:app` 权限已开通，但需要重新发布应用版本才生效

### 测试结果
- 成功读取到 5 条记录，字段列表：`['订单号', '订单状态']`
- 成功更新指定记录的"订单状态"字段

## 3. 相关文件
