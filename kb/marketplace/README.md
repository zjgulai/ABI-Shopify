---
title: shopify-ai-kb · Claude Code 插件市场
type: meta
updated: 2026-06-26
summary: 一键安装 Shopify AI 经营技能包(7 个 skill + 2 个命令 + 可选检索 MCP)。
---
# shopify-ai-kb · Claude Code 插件(一键安装)

## 安装
```text
/plugin marketplace add /Users/pray/project/shopify/kb/marketplace
/plugin install shopify-ai-kb@shopify-ai-kb-marketplace
```
(或把 marketplace 推到 git 仓库后 `/plugin marketplace add <git-url>`。)

安装后即可:
- **自然语言触发 7 个 skill**:建站 / Hydrogen / 批量上架 / CRO / 履约 / UCP / 知识库检索。
- **slash 命令**:`/kb-ask <问题>`(检索知识库作答)、`/shopify-plan <目标>`(路由到节点 SOP)。

## 可选:启用知识库检索 MCP
```bash
export SHOPIFY_KB_DIR=/Users/pray/project/shopify/kb
cd "$SHOPIFY_KB_DIR/_rag/kb_index" && python cli.py build      # 建索引(一次)
cp plugins/shopify-ai-kb/.mcp.json.example plugins/shopify-ai-kb/.mcp.json
```
重载 Claude Code 后,`shopify-kb` MCP 提供 `kb_search` / `kb_ask`。

## 内容
| 类型 | 项 |
|---|---|
| skills | shopify-store-scaffold · shopify-hydrogen-scaffold · shopify-bulk-listing · shopify-cro-function · shopify-fulfillment-ops · shopify-ucp-onboarding · kb-rag-query |
| commands | /kb-ask · /shopify-plan |
| mcp(可选) | shopify-kb(检索) |

## 安全
所有 execution / 真改 / 支付 / 上线 **必须人审**(见各 skill 的人审闸);先测试店铺后生产。
