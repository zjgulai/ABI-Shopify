---
title: 中文社媒独立站案例入库 SOP
stage: 05-营销与引流
layer: 流程节点
tags: [抖音, 小红书, 中文社媒, 独立站案例, 多源入库, t6, 风控]
sources: [inbox, platform-operations-wiki, T6执行队列]
status: ready_for_intake
verification_status: source_schema_only
updated: 2026-06-29
summary: 在尚未获得抖音/小红书帖子正文或截图文字前,先定义独立站中文社媒案例的证据字段、分类规则、风控闸和 RAG/KG 入库流程。
---

# 中文社媒独立站案例入库 SOP

> 当前边界:本项目尚未收到可回溯的抖音/小红书独立站帖子正文、截图文字或评论摘要。因此本文不编写具体平台案例,只沉淀可执行的入库协议。后续可用用户粘贴正文、截图 OCR、已登录 Chrome 只读页面或官方 API 作为证据来源。

## 1. 适用场景

用于把中文社媒中的独立站、Shopify、DTC、跨境选品、内容种草、达人带货、短视频素材、评论需求和竞品案例转成 ABI 知识库资产。

可入库内容:

- 独立站案例复盘:品牌、品类、卖点、落地页、素材、渠道、转化路径。
- 选品信号:评论区求链接、痛点抱怨、替代方案、场景爆发、价格接受度。
- 素材信号:标题钩子、前三秒、脚本结构、画面证明、UGC/KOC 角度。
- 渠道信号:达人、话题、合集、搜索词、站外链接、私域承接。
- 风控信号:夸大收益、搬运素材、未披露广告、功效宣称、灰黑品类。

不入库内容:

- 无正文、无截图、无链接、无法归因的传闻。
- 私信、手机号、邮箱、订单号、用户头像等直接个人信息。
- 平台规则/算法推断,除非有一手规则或明确标注 `needs_external_verification`。

## 2. 入库字段

```json
{
  "source_id": "xhs_or_douyin_YYYYMMDD_001",
  "platform": "xiaohongshu|douyin|bilibili|wechat|other",
  "source_url": "",
  "captured_at": "2026-06-29",
  "capture_method": "user_paste|screenshot_ocr|browser_readonly|official_api",
  "author_display": "",
  "title": "",
  "post_text": "",
  "comment_summary": "",
  "product_or_niche": "",
  "shopify_relevance": "direct|DTC|cross_border|social_signal|unclear",
  "content_angle": ["pain_point", "before_after", "tutorial", "review", "deal", "founder_story"],
  "evidence_type": ["text", "screenshot", "comment", "landing_page", "video_chapter"],
  "claims": [],
  "risk_flags": [],
  "target_nodes": ["01-选品与市场调研", "04-内容与素材生产", "05-营销与引流", "91-合规与风控"],
  "verification_status": "raw_unverified|local_verified|needs_external_verification",
  "redaction_done": true
}
```

## 3. 分类规则

| 信号 | 判断问题 | 入库节点 | 产物 |
|---|---|---|---|
| 选品信号 | 用户是否反复表达同一痛点或求购买链接? | 01 | product_signal_card |
| 素材信号 | 标题、前三秒、画面证明是否能复用到广告/PDP? | 04 | creative_angle_card |
| 渠道信号 | 流量来自搜索、推荐、达人、话题还是评论扩散? | 05 | channel_case_card |
| 承接信号 | 是否有 Shopify/独立站页面、集合页、优惠、FAQ、客服入口? | 02 / 06 | landing_page_gap_card |
| 归因信号 | 是否能识别 UTM、coupon、达人 ID 或投放批次? | 07 | attribution_card |
| 风控信号 | 是否涉及夸大收益、功效、安全、未授权素材或暗广? | 91 | risk_review_card |

## 4. 操作流程

1. **采集**:优先使用用户粘贴正文/截图文字;若使用已登录 Chrome,只做只读页面查看和截图/OCR,不点赞、不评论、不私信、不发布。
2. **去敏**:移除直接个人联系方式、订单、支付、地址、私信截图中的个人信息。
3. **归因**:记录平台、作者展示名、链接、截图时间、截图来源和是否可回访。
4. **抽象**:把内容拆成产品、人群、痛点、卖点、素材、承接、数据、风险。
5. **分类**:映射到 01/04/05/06/07/91,不要只放在 90。
6. **人审**:对平台规则、广告政策、功效宣称、素材授权、收益数字做风险判断。
7. **入库**:用 `kb/tools/t6_multisource_intake.py` 生成草稿,人审后再提升到正式 Markdown 和 KG。
8. **验收**:重建 RAG/site,用关键词检索验证召回,KG 检查 0 悬挂。

## 5. 案例卡模板

```markdown
## 案例: <标题>

- 平台:
- 来源链接/截图:
- 捕获方式:
- 作者展示名:
- 证据等级:
- 产品/品类:
- 内容角度:
- 评论信号:
- 独立站/Shopify 关联:
- 可复用打法:
- 不可直接复用的部分:
- 风险与待核验:
- 节点映射:
```

## 6. 风控闸

- 抖音/小红书平台规则、广告规则、搜索/推荐算法都具时效性;未外部核验前只写成“本地观察/资料来源”,不写成官方事实。
- 不把单条爆款互动量等同于可复制销量。
- 不搬运未授权图片、视频、达人口播或评论截图进入官网/广告。
- 不把软广、种草、联盟佣金、样品置换隐藏成自然推荐。
- 不保存直接个人联系方式、私信内容、地址、订单和支付信息。
- Agent 只能做草稿、分类、风险提示和复盘,不能自动发帖、私信、刷互动或改外部账号状态。

## 7. 与 ABI 作战台的连接

| 作战台模块 | 读取字段 | 输出 |
|---|---|---|
| 市场洞察 Agent | `post_text`、`comment_summary`、`product_or_niche` | 产品信号、需求强度、竞品缺口 |
| 素材 Agent | `content_angle`、截图/OCR、评论高频词 | 图文/短视频脚本、PDP 证明点 |
| 渠道 Agent | `platform`、话题、达人、链接路径 | 渠道角色、投放/自然内容建议 |
| CRO Agent | 独立站链接、落地页截图、评论疑问 | PDP/FAQ/政策页承接缺口 |
| 风控 Agent | `claims`、`risk_flags`、授权字段 | go/revise/block 与审批清单 |

## 8. 最小验收词

新增真实案例后,至少用以下检索词验收:

- `小红书 独立站 选品 评论信号`
- `抖音 Shopify 素材角度`
- `中文社媒 独立站 风控`
- `短视频种草 PDP 承接`
- `达人内容 授权 复用`
