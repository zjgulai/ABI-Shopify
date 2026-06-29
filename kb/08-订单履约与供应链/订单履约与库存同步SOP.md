---
title: 订单履约与库存同步 SOP
stage: 08-订单履约与供应链
layer: 流程阶段
tags: [订单履约, 库存同步, 3PL, 海外仓, 退款, 客服联动]
sources: [周报, shopify官方, inbox, platform-operations-wiki]
status: local_material_needs_external_verification
updated: 2026-06-28
summary: 把 Shopify 订单、库存、海外仓/3PL、退款售后和客服承接组织成可审计的履约闭环。
---

# 订单履约与库存同步 SOP

> 适用范围:Shopify 独立站的可售库存、订单推送、海外仓/3PL/FBA/WMS 对接、退款退货和站外活动前库存准备。
> 边界:本 SOP 不执行店铺读写;真实库存、订单、退款、履约 API 均需要测试店或授权环境验证。

## 1. 输入

| 输入 | 最小字段 | 风险 |
|---|---|---|
| SKU 主数据 | SKU、barcode、variant、箱规、重量、供应商 | 主数据不一致会导致错发 |
| 库存口径 | 可售、在途、锁定、预留、安全库存、仓库维度 | 口径混用会导致超卖 |
| 仓库/3PL 信息 | warehouse_id、服务商、国家、时效、费用、截单时间 | 承诺时效需要校验 |
| Shopify 订单 | order_id、line_items、shipping address、payment status、risk status | 客户和支付数据敏感 |
| 售后政策 | 退款、退货、换货、保修、拒付处理 | 政策页必须与客服一致 |

## 2. 履约闭环

### 2.1 库存同步

库存同步至少拆成四层:

1. `source_inventory`:ERP/WMS/3PL 原始库存。
2. `available_inventory`:扣减锁定、预留、异常仓后的可售库存。
3. `shopify_inventory`:同步到 Shopify location/variant 的库存。
4. `channel_inventory`:Deal、联盟、广告活动前预留或限量库存。

每次同步要记录:
- `sync_time`
- `source_system`
- `sku_count`
- `delta_count`
- `blocked_sku`
- `operator_or_agent`
- `rollback_plan`

### 2.2 订单推送

| 状态 | 动作 |
|---|---|
| paid + low risk | 进入待履约队列 |
| paid + medium/high risk | 人审后推送 |
| unpaid / pending | 不推送仓库 |
| address issue | 客服确认后推送 |
| inventory shortage | 触发补货/拆单/取消预案 |

订单推送到 3PL/海外仓前必须完成:
- 地址格式校验。
- 库存锁定。
- 风险订单筛查。
- 物流服务选择。
- 客服可见的订单状态同步。

### 2.3 异常与售后

| 异常 | 处理 |
|---|---|
| 超卖 | 停止相关活动,客服通知,补货或替代方案 |
| 仓库拒单 | 回查 SKU/地址/物流服务,重新推送或人工处理 |
| 延迟发货 | 更新承诺时效,给客服和营销活动同步 |
| 退款退货 | 按政策页和订单状态走审批 |
| Deal/红人爆量 | 启动库存水位监控和客服高峰预案 |

## 3. 输出物

| 输出物 | 说明 |
|---|---|
| `inventory_sync_policy` | 库存口径、同步频率、安全库存和回滚规则 |
| `fulfillment_queue` | 待履约、待人审、异常、已推送队列 |
| `warehouse_mapping` | Shopify location 与仓库/3PL 的映射 |
| `activity_stock_guard` | 广告、Deal、红人活动前库存水位检查 |
| `after_sales_playbook` | 退款、退货、换货、拒付处理流程 |
| `customer_status_feed` | 客服可用的订单状态说明 |

## 4. 验收

- 库存同步前后 SKU 差异可解释,且支持回滚。
- Shopify、ERP/WMS/3PL 对同一 SKU 的库存口径有明确映射。
- 高风险订单不会自动推送仓库。
- 站外活动前完成库存、客服、物流、优惠码和政策页检查。
- 售后政策与页面、客服话术和仓库动作一致。
- 任何真实订单、退款或库存写入都留审批和审计记录。

## 5. 风险闸

| 风险 | 处理 |
|---|---|
| 测试环境与真实仓库混用 | 测试店、沙箱、真实仓库账号分离 |
| 自动推单导致错发 | 高风险订单和地址异常进入人审 |
| 活动爆量导致超卖 | 活动前设置 `activity_stock_guard` |
| 客服不知道履约异常 | 订单状态同步到客服视图 |
| 退款/拒付自动化过度 | 退款、拒付、补偿动作保持人审 |

## 6. 与站点作战台的连接

- Journey `站外全域增长` 在活动前读取 `activity_stock_guard`。
- Agent `经营复盘 Agent` 汇总库存、订单、客服和渠道数据。
- T7 写入链路进入前,库存和订单相关动作必须保持 `test_store_only` 与人审。

## 7. 来源

- `kb/08-订单履约与供应链/README.md`
- `kb/05-营销与引流/平台运营Wiki_独立站全域流量增长SOP.md`
- `kb/07-数据与归因/平台运营Wiki_全域增长数据归因SOP.md`
- `kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md`
- `kb/90-AI能力地图/内部资料萃取_独立站实操资料包.md`
