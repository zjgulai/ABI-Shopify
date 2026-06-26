---
title: Claude Code Skills(每节点可运行)
type: meta
updated: 2026-06-26
summary: 把每节点 SOP 落成的 Claude Code skill 文件;安装后在 Claude Code 里用自然语言触发。
---
# skills — 可运行的 Claude Code Skills

## 安装
把本目录下各 skill 复制到 Claude Code 的 skills 位置(任选其一):
- 项目级:`<你的项目>/.claude/skills/`
- 用户级:`~/.claude/skills/`
```bash
cp -r skills/* ~/.claude/skills/      # 或项目 .claude/skills/
```
重启 / 重载 Claude Code 后,描述任务即可自动触发对应 skill。

## 清单
| skill | 节点 | 触发场景 |
|------|------|---------|
| shopify-store-scaffold | 02 | 建站/搭主题 |
| shopify-hydrogen-scaffold | 02 | headless/Hydrogen/Oxygen |
| shopify-bulk-listing | 03 | 批量上架/Listing/多语言 |
| shopify-cro-function | 06 | 满赠/折扣/结账规则/CRO |
| shopify-fulfillment-ops | 08 | 库存/履约/退款 |
| shopify-ucp-onboarding | 10 | UCP/代理式商务/AI 渠道成交 |
| kb-rag-query | 横切 | 检索本知识库回答问题 |

## 前置与安全
- 多数 skill 依赖 **Shopify AI-Toolkit**(Claude Code 插件)+ Shopify CLI 登录;先用测试店铺。
- **execution / 真改 / 支付 / 上线 必须人审**(见各 skill 的人审闸)。
