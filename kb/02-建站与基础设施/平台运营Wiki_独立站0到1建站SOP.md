---
title: 平台运营 Wiki 萃取 · 独立站 0 到 1 建站 SOP
stage: 02-建站与基础设施
layer: 流程阶段
tags: [platform-operations-wiki, 独立站, Shopify, 建站, 收款, 物流]
sources: [platform-operations-wiki, E003, E106, E104]
status: verified
updated: 2026-06-27
summary: 将独立站 0-1 拆成市场确认、品牌域名、Shopify建站、政策页、收款、物流和基础运营检查。
verification_status: local_source_only
---

# 平台运营 Wiki 萃取 · 独立站 0 到 1 建站 SOP

## 1. 抽取边界

本篇聚合平台运营 Wiki 中的独立站 0-1 资料,用于补强 ABI 的建站与基础设施节点。涉及 Shopify 价格、优惠、PayPal 规则、平台后台配置等信息具时效性,本篇只按本地资料记录方法,不作为官方当前规则。

核心来源:
- E106: `纯小白如何做一个跨境独立站项目？（全流程详解）.docx`
- E003: `FLOW-独立站1V1小白陪跑服务.pptx`
- E104: `独立站HOME页SEO最强布局（实用干货）.docx`

## 2. 建站前置条件

源资料把独立站启动前置拆成四件事:

1. 市场与类目确认:用 Google Trends、搜索结果、竞品数量、Amazon/TikTok/1688 榜单等判断是否值得进入。〔来源:platform-operations-wiki · E106〕
2. 品牌名与域名:品牌名应与类目相关、有记忆点,并避免侵权；优先确认 `.com` 等通用域名可用性。〔来源:platform-operations-wiki · E106〕
3. 主体与付款工具:注册公司、准备信用卡或其他可支付 Shopify/月租/插件的工具。〔来源:platform-operations-wiki · E106〕
4. 收款准备:注册 PayPal 商家账号或其他收款工具,资料和登录环境需稳定、真实、可追溯。〔来源:platform-operations-wiki · E106〕

对 ABI 的落地:
- `02` 节点的建站 Agent 不应从主题选择开始,而应先检查 `01` 是否已有市场假设、品牌名、域名、主体、收款和物流约束。
- 若主体、收款或品类合规不清,建站输出应标记为 `draft_requires_manual_review`,不直接进入上线。

## 3. 建站平台取舍

源资料给出的平台取舍可以抽象为:

| 平台 | 适配场景 | 风险/限制 |
|---|---|---|
| Shopify | 小白友好、插件生态完整、适合标准 C 端交易 | 月租、插件费、平台规则、敏感品类限制需核验 |
| WooCommerce | 基于 WordPress,可定制性高 | 需要更强技术维护和性能/安全治理 |
| Wix | 操作简单 | 功能扩展和复杂电商能力相对有限 |
| 国内建站平台 | 某些敏感或灰色类目可能更容易起站 | 支付、海外体验、SEO、合规与长期资产风险需评估 |

本项目当前以 Shopify 为主线,因此上述信息只用于比较和前置决策,不改变 ABI 的 Shopify-first 架构。

## 4. Shopify 基础搭建检查表

建站 Agent 或人工操盘手应按以下顺序检查:

| 阶段 | 检查项 | 输出 |
|---|---|---|
| 账号与域名 | Shopify 账号、域名解析、品牌邮箱 | `site_identity_ready` |
| 主题与导航 | Dawn/付费主题、首页、类目、PDP、导航、页脚 | `site_structure_ready` |
| 信任页 | About、Contact、FAQ、Privacy、Terms、Shipping、Return/Refund | `trust_pages_ready` |
| 市场与物流 | 市场国家、币种、税费提示、运费规则、满包邮门槛 | `market_shipping_ready` |
| 商品上架 | 类目架构、产品标题、描述、图片、价格、库存 | `catalog_ready` |
| 收款 | PayPal/信用卡/本地收款方式,测试下单 | `payment_ready` |
| 跟踪 | GA4、GSC、Meta Pixel、UTM、基础事件 | `tracking_ready` |

政策页不要直接照搬模板。源资料强调联系方式、品牌故事、隐私政策、运输/退货退款政策要尽可能真实可信,避免使用与实际主体不一致的地址或承诺。〔来源:platform-operations-wiki · E106〕

## 5. 首单前闭环测试

上线推广前必须跑一次最小闭环:

1. 访问首页和类目页,确认移动端可浏览。
2. 打开 PDP,确认图片、价格、变体、库存、配送和退换货说明一致。
3. 加购、进入结账、测试支付入口。
4. 生成测试订单或沙盒订单后,确认订单通知、ERP/店小秘/物流商对接路径。
5. 检查售后邮箱、聊天入口、FAQ 和退货政策。
6. 确认 GA4/GSC/Pixel 等基础跟踪能采集到浏览、加购和结账事件。

对 `10-自动化编排` 的衔接:
- 建站 Agent 只生成配置草案。
- 支付、物流、政策页和真实订单流必须人审。
- 任何 production 写操作均走 `draft -> review -> approve -> execute -> audit`。

## 6. 与其他节点的接口

- 输入自 `01`:目标市场、品类、竞品、价格带、供应链约束。
- 输出到 `03`:商品类目架构、PDP 模板、图片/视频素材需求。
- 输出到 `05`:SEO、社媒账号、广告像素、KOL/联盟链接承接。
- 输出到 `06`:首页、落地页、PDP、信任状和速度优化。
- 输出到 `07`:GA/GSC/UTM/广告像素和渠道复盘字段。
- 输出到 `91`:品类合规、支付/物流/隐私/退款政策风险。
