---
title: Shopify KB 网站增量设计进度
updated: 2026-06-30
---

# 进度

- 2026-06-28: 建立本轮执行计划。
- 2026-06-28: 确认当前 `HEAD=8115f053531d`,本地只有 `inbox/`、`tmp/` 未跟踪。
- 2026-06-28: 确认站点现有统计为 `14 nodes / 557 chunks / 253 entities / 776 relations`。

- 2026-06-28: 扩展 `build_site_data.py`,新增 sourceRegistry/coverageMatrix/repoPlaybooks/growthPlaybooks/agentWorkflows/riskGates/skillCatalog。
- 2026-06-28: 增量改造 `site/index.html`,新增经营作战台、工程仓库地图、增长作战室、Agent 工作流、风控闸、来源覆盖和工具包入口。
- 2026-06-28: 完整重建通过: chunks=558, docs=110, eval pass_rate=1.00, KG entities=253/relations=776。
- 2026-06-28: 静态检查通过: inline JS、kb_data.js、build_site_data.py。
- 2026-06-28: Playwright 本地静态预览通过: 桌面模块数量正确,移动端无横向溢出,控制台红项 0。
- 2026-06-28: 确认 PRD2.0 主定位为 B 经营作战台,并进入 P0 开发。
- 2026-06-28: 已扩展 `build_site_data.py`,新增 commandCenter/journeys/technicalRoutes/nodeReadiness/sopPlaybooks/executionReadiness/evidenceItems/queryPresets/contentDebt。
- 2026-06-28: 已改造 `site/index.html`,新增 Command Center、Journey Selector、Technical Decision Center、SOP 库、Execution Readiness、内容债、移动导航和上下文问答入口。
- 2026-06-28: P0 重建与检索复核通过: `kb_data.js` 792 KB, nodes=14, chunks=558, eval pass_rate=1.00。
- 2026-06-28: P0 Playwright DOM 复核通过: Journey=7, technicalRoutes=6, SOP=8, readiness=6, contentDebt=3,桌面/移动端均无横向溢出。
- 2026-06-28: 已保存 P0 截图证据到 `tmp/prd2-p0-qa/screenshots/`。
- 2026-06-28: 进入 PRD2.0 P1,目标是补齐 04/08/09 最小专题 SOP,并扩展 Growth、Agent、Evidence 页面字段。
- 2026-06-28: 已新增 `AI素材生产与授权SOP.md`、`订单履约与库存同步SOP.md`、`客户会员与VOC闭环SOP.md`。
- 2026-06-28: 已接入 P1 SOP 库、增长复盘指标、Agent 任务模板、Evidence 状态筛选和内容债空态。
- 2026-06-28: P1 重建通过:`kb_data.js` 833 KB, chunks=585, docs=113, SOP=12, contentDebt=0。
- 2026-06-28: P1 检索复核通过:三条新增 SOP 均可被关键词召回;通用 eval pass_rate=1.00。
- 2026-06-28: P1 Playwright 复核通过:SOP=12, Evidence 筛选=5,桌面/移动端均无横向溢出;截图证据在 `tmp/prd2-p1-qa/screenshots/`。
- 2026-06-28: 进入 T6 下一批视频萃取,使用 browser-harness 只读复核 Ac Hampton 清单 #21/#24/#26/#37。
- 2026-06-28: 已完成 `Y3iXtMjE4bw`、`NX-5ChIZBRQ`、`WkUkzdMnRHo` UI 转写级萃取,新增 `视频深度萃取_AcHampton_AI与履约小批次.md`。
- 2026-06-28: 已确认 `rhuYy9LP72M` 页面作者为 Mark Tilbury,从 Ac Hampton 队列移出并作为跨频道候选处理。
- 2026-06-28: 已完成 `xZjkLrHJheE`、`iwmz1sL5r9g`、`_1caEZ7t3UY`、`CYH_dRPD2B4` UI 转写级萃取,新增 `视频深度萃取_全流程长课与战略访谈.md`。
- 2026-06-28: 已确认 `iwmz1sL5r9g`/`_1caEZ7t3UY`/`CYH_dRPD2B4` 播放页作者分别为 Rihab Seb、Learn With Shopify、Emma Grede,并从 Ac Hampton/Metics 深度覆盖中按跨频道归因处理。
- 2026-06-29: 已完成 `e7oiWBn7KwU` UI 转写级 CRO 诊断萃取,新增 `视频深度萃取_CRO诊断与高收入话术识别.md`。
- 2026-06-29: 已确认 `uRHm5WpPJyU` 播放页作者为 Austin Rabin,按跨频道高收入话术识别样例处理,不计入 Ac Hampton 深度覆盖。
- 2026-06-29: 已完成 `1EgjCxk0-kM` / `aKIHLrdsv8o` Apps 页面说明级 v0.1,不写未经核实的 App 推荐清单,只沉淀 App 审计卡。
- 2026-06-29: 已确认 `okSKWf8PBNY` / `1o6cKeK24Mw` 播放页作者分别为 Code with Chris the Freelancer / 梧桐小讲堂,按跨频道 Theme 工程和中文建站教程入库。
- 2026-06-29: 已新增 `05-营销与引流/中文社媒独立站案例入库SOP.md`,抖音/小红书真实案例仍待帖子正文、截图文字或评论摘要。
- 2026-06-29: 本批重建通过: chunks=631, docs=118, KG entities=260/relations=785, site data=963KB。
- 2026-06-30: 进入 T7 前置批次,新增 `T7测试店授权前置包.md` 与 `tools/t7_test_store_preflight.py`;边界为本地只读 preflight,不登录 Shopify、不读写店铺、不输出密钥值。
- 2026-06-30: T7 前置批次重建通过: chunks=640, docs=119, KG entities=260/relations=785, site data=983KB;检索评测 5/5(pass_rate=1.00, top1=0.60, MRR=0.68)。
- 2026-06-30: T7 网站配置中心批次完成: site data=987KB, chunks=640/docs=119, KG entities=260/relations=785/dangling=0,检索评测 5/5(pass_rate=1.00, top1=0.60, MRR=0.68),Playwright 桌面/移动端配置页 smoke 通过;边界仍为不登录 Shopify、不读写店铺、不保存 Shopify token/password/private key。
- 2026-06-30: 配置中心版本已部署到腾讯云 `platform.shopify.lute-tlz-dddd.top`:release=`20260630T0815-84bde79`,远端分支 SHA=`cf23e76a0646ea6605153b51d9e43b2a2dfed48b`;线上 `/api/health` ok=true/retriever=true/server_key_set=false,生产检索日志显示 `BAAI/bge-small-zh-v1.5 + Chroma` indexed 640 chunks、Neo4j import 260 entities/785 relations;Playwright 线上配置页桌面/移动端 smoke 通过,未填 Key 的 `/api/chat` 仅返回需页面填入 DeepSeek API Key。
- 2026-06-30: 线上发布状态批次完成并部署到腾讯云:release=`20260630T1148-8043768`,commit=`8043768f39c7924a56317d62eb9b6ed0ead4c3a5`;`/api/deploy-status` 返回 status_file=true、3 个关键 sha256、runtime=`BAAI/bge-small-zh-v1.5 + Chroma + Neo4jGraphStore`、chunks_loaded=647、server_key_set=false;`#config` 页面“线上发布状态”桌面/移动端 smoke 通过。T5 provider 问答仍待页面手动录入 Key,T7 真实读写仍待测试店授权与人审。
- 2026-06-30: 进入 T6 inbox 增量来源治理批次:已复制 15 个 inbox 原件到 `_sources/inbox-independent-site/originals`,生成抽取文本、manifest 与 source_inventory;发现 `ACC&FB群组...pptx` 与 `KOL+联盟营销组合打法.pptx` 为同 SHA 重复,按 14 唯一内容处理;新增 `05-营销与引流/站外全域增长组合SOP.md` 与 `07-数据与归因/广告诊断SOP.md`,边界为本地资料来源、无 provider call、平台规则/算法/业绩数字待外部核验。
- 2026-06-30: T6 inbox 增量本地重建通过:Markdown=126,RAG docs=123,chunks=672,KG entities=260/relations=785/dangling=0,site data=1053KB;默认检索评测 5/5(pass_rate=1.00,top1=0.60,MRR=0.68);定向检索可召回 `站外全域增长组合SOP`、`广告诊断SOP`、`inbox-independent-site 来源包` 和 `站外渠道风控SOP`。
- 2026-06-30: T6 `listing优化模板.xlsx` 全量关键词资产导出完成:从 `5.关键词库` 结构化 801 行、42 个原始字段,识别 row_layout=`rich_top_asin_col33` 218 / `compact_metric_col6_top_asin_col25` 228 / `compact_type_col6_top_asin_col25` 355,生成 `keyword_assets_full.csv/jsonl`、流量词 bridge/summary、12 个上下文 sheet CSV 和 `Listing关键词资产库_全量导出.md`;本地重建通过 chunks=688/docs=125/site data=1073KB,检索评测 5/5(pass_rate=1.00,top1=0.60,MRR=0.68),定向检索可召回 Listing 关键词资产专题与来源 README。边界:本地来源快照,无 provider call,未登录/读取/写入 Shopify。
