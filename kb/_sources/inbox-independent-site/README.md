---
title: inbox-independent-site 来源包
type: source_package
updated: 2026-06-30
summary: 记录 /Users/pray/project/shopify/inbox 独立站实操资料包的受控复制、去重、抽取文本和入库边界。
verification_status: local_source_only
---

# inbox-independent-site 来源包

## 1. 来源与用途

本目录是 `/Users/pray/project/shopify/inbox/` 的受控来源区,用于把用户新增的独立站、站外流量、Listing、广告诊断和 Agent 工作流资料接入 Shopify KB。

本轮动作:
- 复制原件到 `originals/`。
- 抽取可检索文本到 `extracts/`。
- 生成 `manifest.json` 与 `source_inventory.csv`。
- 去重后把高价值内容归类到 `03/05/07/90/91` 等节点。

边界:
- 本轮仅做本地只读复制、解析、归类和知识库重建。
- 未调用外部 provider,未登录外部平台,未对 Shopify 店铺或广告平台做任何读写。
- 资料中的业绩数字、平台算法、社区规则、广告后台字段与课程宣称均保留 `needs_external_verification` 边界,不升级为官方事实。

## 2. 文件清单

| extract_id | 原文件 | sha256 前缀 | 状态 | 主要落点 | 风险边界 |
|---|---|---:|---|---|---|
| inbox:S01 | `ACC&FB群组&Deal站&KOL&站外CPC&联盟营销社媒.pptx` | `262ecc8c80c8` | imported | `05-营销与引流` | 站外打法和业绩数字需外部核验 |
| inbox:S02 | `KOL+联盟营销组合打法.pptx` | `262ecc8c80c8` | merged_duplicate | `05-营销与引流` | 与 S01 完全重复,仅作别名 |
| inbox:S03 | `独立站从0-1搭建高流量店铺.pptx` | `657f8e6924bb` | imported | `02-建站与基础设施`,`05-营销与引流` | 工具取舍和广告规则需外部核验 |
| inbox:S04 | `独立站网红+全域社媒流量增长.pptx` | `f935785aec01` | imported | `05-营销与引流` | Reddit/社媒运营规则需外部核验 |
| inbox:S05 | `listing优化模板.xlsx` | `6a39b95bb34d` | imported | `03-商品上架与Listing`,`07-数据与归因` | 大体积表格为结构与样本级抽取 |
| inbox:S06 | `【06产品开发】亚马逊选品干货：社交媒体掘金选品.docx` | `e5928be71ac2` | imported | `01-选品与市场调研` | Amazon 专属规则不改写成 Shopify 规则 |
| inbox:S07 | `产品力提升x爆品创新，单SKU年销破2000W.pptx` | `d1f9ad1e079f` | imported | `01-选品与市场调研`,`04-内容与素材生产` | 年销数字为资料标题/课程宣称,不作事实背书 |
| inbox:S08 | `【0718站外】Slickdeals使用指南..docx` | `bd708e217253` | imported | `05-营销与引流`,`91-合规与风控` | Deal 站规则和发帖路径需执行前复核 |
| inbox:S09 | `【08独立站】独立站大卖实操干货：Facebook矩阵长效养号完整攻略.docx` | `a8668560c0a3` | imported | `05-营销与引流`,`91-合规与风控` | 账号/IP/设备建议为本地资料观点,需合规复核 |
| inbox:S10 | `GMV千万美金广告作战方案(1).xmind` | `93a813725130` | imported | `07-数据与归因` | GMV 目标和 SA/DSP 指标口径为资料口径 |
| inbox:S11 | `广告高阶打法&数据分析.docx` | `231a118ed006` | imported | `07-数据与归因` | COSMO/算法表述需外部核验 |
| inbox:S12 | `手把手带你做广告报告分析.docx` | `d288d1b1e8a8` | imported | `07-数据与归因` | Amazon 报表字段不可直接等同 Shopify 后台 |
| inbox:S13 | `推测规律总结&广告拆解逻辑.xmind` | `455f0452228d` | imported | `07-数据与归因` | 搜索词推断为经验规则,需样本验证 |
| inbox:S14 | `独立站新手高频问题解答.pdf` | `fcacef135e25` | imported | `02-建站与基础设施` | 建站成本/工具推荐随时间变化 |
| inbox:S15 | `workflow01.png` | `5ef34c8c0aba` | imported | `90-AI能力地图`,`10-自动化编排` | OCR 有噪声,只保留可复核工作流结构 |

## 3. 入库专题

本来源包当前已形成或补强以下专题:

- [`内部资料萃取_独立站实操资料包`](../../90-AI能力地图/内部资料萃取_独立站实操资料包.md)
- [`Listing内容工厂SOP`](../../03-商品上架与Listing/Listing内容工厂SOP.md)
- [`站外渠道风控SOP`](../../91-合规与风控/站外渠道风控SOP.md)
- [`站外全域增长组合SOP`](../../05-营销与引流/站外全域增长组合SOP.md)
- [`广告诊断SOP`](../../07-数据与归因/广告诊断SOP.md)

## 4. 证据文件

- `manifest.json`:机器可读来源清单、SHA256、去重状态、抽取路径和入库状态。
- `source_inventory.csv`:表格化来源清单,便于人工审查。
- `originals/`:原件复制件。
- `extracts/`:本地抽取文本快照。
