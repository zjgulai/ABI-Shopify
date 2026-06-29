---
title: AI-Toolkit / UCP 测试店受控写验收 Runbook
stage: 10-自动化编排
layer: 流程阶段
tags: [ai-toolkit, ucp, shopify-dev-mcp, test-store, controlled-write, approval]
sources: [shopify官方, 执行说明, T7测试店授权前置包]
status: blocked_auth_preflight_ready
updated: 2026-06-30
summary: 在测试店验证 Claude/AI Toolkit/UCP 的读店铺与受控写能力;定义授权、人审、回滚和证据台账,禁止直接改生产店。
---

# AI-Toolkit / UCP 测试店受控写验收 Runbook

## 1. 当前状态
- 已准备:本知识库已提供 `shopify-ai-kb` 本地插件、UCP 接入 SOP、AI Toolkit 技能 SOP、[`T7 测试店授权前置包`](T7测试店授权前置包.md) 与本地 preflight 脚本。
- 已验证:2026-06-30 核对 Shopify 官方资料后,本地前置要求按 Node.js 22.12+、Git 2.28+、npm/npx、development store/test store 和 AI Toolkit/Dev MCP 入口处理。
- 未执行:尚未登录用户 Shopify 测试店,未读取真实店铺数据,未执行任何写操作。
- 阻塞项:需要用户提供或现场完成测试店授权,并明确批准一次低风险 mutation。

## 2. 红线
- 只允许测试店;不对生产店执行写操作。
- 不执行支付、退款、履约、真实投放预算等资金或不可逆动作。
- 不把 access token、private app key、API secret 写入仓库、前端、截图或聊天正文。
- 每次写操作必须有人审批准、可回滚、可复查。

## 3. 环境准备
建议先打开网站 `#config` 配置与授权中心,确认测试店域名、人审文本和本地 preflight 输出。配置中心生成的文本只是执行前准备,不代表 Shopify 已授权。

先做本地只读 preflight:

```bash
python3 kb/tools/t7_test_store_preflight.py --store-domain your-dev-store.myshopify.com
```

脚本不会登录 Shopify、不会访问网络、不会读取或写入店铺、不会输出密钥值。通过后再进入以下人工授权步骤:

```bash
/plugin marketplace add /Users/pray/project/shopify/kb/marketplace
/plugin install shopify-ai-kb@shopify-ai-kb-marketplace
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest
shopify auth login
```

登录时必须选择测试店或 development store。若 CLI 展示多个 store,先停止并由用户确认目标店铺域名。

测试店尚未创建时,先由用户在 Shopify Partner / Dev Dashboard 创建 development store,建议启用测试数据,命名为 `abi-t7-smoke-YYYYMMDD` 一类可回溯名称。

## 4. 验收流程
| 步骤 | 动作 | 证据 | 通过条件 |
|---|---|---|---|
| 1 | 只读连接检查 | `shopify auth whoami` 或 Dev MCP 只读响应 | 目标店铺为测试店 |
| 2 | 读取店铺基础信息 | products/count、themes/list 或 policies read | 能读到测试店数据,无写入 |
| 3 | 生成写入预案 | mutation preview / draft payload | 明确对象、字段、前后值、回滚方式 |
| 4 | 人审批准 | 审批台账记录 | 用户明确批准本次 mutation |
| 5 | 执行低风险写入 | Dev MCP/Admin mutation 输出 | 仅改测试对象,无资金动作 |
| 6 | 写后只读复查 | 再读同一对象 | 字段与预案一致 |
| 7 | 回滚或保留决定 | 回滚命令/保留理由 | 用户确认 |

推荐首个写入目标:测试商品的非公开字段或测试价格,例如 `title` 后缀、`tags`、`metafield`。避免订单、支付、库存扣减和真实渠道发布。

## 5. 审批台账模板
```json
{
  "run_id": "t7-test-store-YYYYMMDD-HHMM",
  "store_domain": "example-dev.myshopify.com",
  "environment": "test_store",
  "operator": "user-approved-codex",
  "action": "product_update",
  "target": {
    "type": "product",
    "id": "gid://shopify/Product/...",
    "title_before": "Test Product"
  },
  "planned_change": {
    "field": "tags",
    "before": ["abi-smoke"],
    "after": ["abi-smoke", "ai-toolkit-controlled-write"]
  },
  "approval": {
    "approved_by": "user",
    "approved_at": "YYYY-MM-DDTHH:MM:SS+08:00",
    "approval_text": "同意仅在测试店执行本次写入"
  },
  "rollback": {
    "method": "restore previous tags",
    "required": true
  },
  "evidence": {
    "pre_read": "path-or-command-output-summary",
    "mutation_result": "path-or-command-output-summary",
    "post_read": "path-or-command-output-summary"
  }
}
```

台账可放在 `tmp/t7_controlled_write/`。不要把 token 或完整认证响应写入台账。

## 6. UCP 后续验收
测试店受控写通过后,再进入 UCP/Catalog:
1. 在 Shopify Developer Dashboard 注册 agent profile。
2. 用公共 MCP/Catalog 端点验证 product search / lookup。
3. 仅在测试链路验证 cart / checkout;支付 mandate 需单独人工审批。
4. 将通过证据回写到 `UCP接入SOP.md` 与本 Runbook。

## 7. 完成定义
- 读店铺数据通过。
- 一次低风险测试店写入通过人审、执行、复查。
- 有审批台账与回滚记录。
- 明确记录没有生产店写入、没有资金动作、没有凭据入库。
