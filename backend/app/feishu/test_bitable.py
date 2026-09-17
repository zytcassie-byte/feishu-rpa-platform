from feishu_client import get_bitable_records, update_bitable_record

APP_TOKEN = "CXiAbelWOaRBuaswxsRcktggnWb"
TABLE_ID = "tblFVA154scj9BU0"

# 1. 读取
records = get_bitable_records(APP_TOKEN, TABLE_ID)
print(f"共读取到 {len(records)} 条记录")

if records:
    record_id = records[0].record_id
    print(f"准备更新记录: {record_id}")

    # 2. 更新：把订单状态改成“已发货”
    update_bitable_record(APP_TOKEN, TABLE_ID, record_id, {"订单状态": "已发货"})
