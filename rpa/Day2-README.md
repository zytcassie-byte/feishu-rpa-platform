# RPA 机器人说明

## OrderQueryBot（订单查询机器人）

- **输入**：order_no（订单号）
- **输出**：order_status（订单状态）、amount（金额）
- **流程**：登录影刀商城 → 进入订单列表 → 搜索订单 → 读取状态和金额
- **异常处理**：订单不存在时返回 ORDER_NOT_FOUND

## ShipBot（发货机器人）

- **输入**：order_no（订单号）
- **输出**：ship_result（执行结果）
- **流程**：登录影刀商城 → 搜索订单 → 判断状态 → 点击确认发货
- **异常处理**：订单不存在返回 ORDER_NOT_FOUND，已发货返回 ALREADY_SHIPPED

## 待接入

后续将通过 MySQL 任务队列调度这两个机器人，实现从飞书事件到 RPA 执行的完整闭环。