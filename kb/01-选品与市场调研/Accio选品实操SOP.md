---
title: Accio Work 选品实操 SOP + 选品需求 brief 模板
stage: 01-选品与市场调研
layer: 流程阶段
tags: [accio-work, 选品, 采购, brief, 数据桥, sop]
sources: [web, 工具]
status: verified
updated: 2026-06-26
summary: 用 Accio Work 做选品/采购的逐步实操 SOP、可直接填的选品需求 brief 模板,以及把选定 SKU 一键转成 Shopify 导入的数据桥。
---

# 🛒 Accio Work 选品实操 SOP

> **边界**:本助手**不替你登录 Accio、不替你 RFQ/下单/付款/签合同**——这些必须你操作。我提供:实操步骤、brief 模板、以及可运行的 **Accio→Shopify 数据桥**(`tools/accio_to_shopify.py`)。
> 现状:Chrome 扩展未放行 accio.com 域名,故暂无法陪你走 UI;如需我"只读陪走",请在扩展放行该域名并保持登录。

## 1. 前置
- 注册/登录 Alibaba(Accio.com)账号;装 Accio Work 桌面端(mac/Win)或用 web 版。
- 业务画像配好:品类(母婴)、目标市场、预算、合规区域。

## 2. 选品需求 brief 模板(复制填好后投喂给 Accio)
```
【品类】吸奶器 / 喂养 / 睡眠 …(具体到子类)
【目标市场】US / EU / 东南亚(主+次)
【目标人群】新手妈妈 / 职场妈妈 …
【价格带】零售 $__–$__;目标毛利 ≥ __%
【成本/MOQ约束】单价 ≤ $__;可接受 MOQ ≤ __
【必备认证】CE / FDA / RoHS …(按市场)
【差异化要求】免手扶 / 静音 / App 联动 …
【排除项】侵权外观 / 高退货风险 / 受限品类
【输出要求】Top __ 候选:含供应商、成本、MOQ、认证、图片、卖点、风险
```

## 3. 实操步骤
1. 新建选品任务 → 粘贴上面的 brief。
2. 让 Accio 的 Agent 团队跑:**市场分析 → 选品候选 → 生成 RFQ → 多轮供应商谈判 → 打样建议**。
3. **人审**:核对成本/MOQ/认证/侵权风险,选定 SKU 与供应商(下单/付款/合同你来)。
4. **导出**选定产品(JSON 或 CSV;字段含 product_name/supplier/cost/price/moq/category/market/image/certifications/description)。
5. **数据桥转 Shopify**:
   ```bash
   python tools/accio_to_shopify.py 你的选品.json -o shopify_products.csv
   ```
   产出标准 Shopify 商品导入 CSV(**Status=draft**,含成本/MOQ/供应商/认证 metafields)。
6. Shopify 后台 **Products → Import** 导入 CSV → 人审后发布 → 进入 [[03-商品上架与Listing]] 用 Magic 完善 Listing。

## 4. 人审 / 合规闸(见 [[91-合规与风控]])
- 下单/付款/合同 = 资金动作,**必须你确认**;保留谈判与采购审计。
- 母婴认证(CE/FDA 等)与侵权外观必须人工复核后再发布。
- 默认导入为 `draft`,避免未审先上架。

## 5. 与全链路衔接
Accio(选品/采购/合规)→ 数据桥 → Shopify Catalog 标准化([[03-商品上架与Listing]])→ 营销/转化/会员(Shopify 原生)。编排视角见 [[10-自动化编排]]、协作总览见 [[01-选品与市场调研/AccioWork接入与协作SOP]]。
