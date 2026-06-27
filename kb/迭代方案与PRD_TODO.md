---
title: ABI 智能化独立站 · 迭代方案 / PRD 核心 / TODO
type: plan
updated: 2026-06-27
summary: 盘点 T1–T7 当前执行状态,给出未完成任务计划;含每节点主-副工具 × 实现方法 PRD 核心表与 TODO。
---

# 🧭 ABI 智能化独立站 · 迭代方案 / PRD 核心 / TODO

## A. 未完成事项盘点(现状)
| 编号 | 事项 | 现状 |
|---|---|---|
| T1 | 商业图堆叠修复 | 已完成脚本坐标修复与 5 张商业图输出;本轮将 RAG 块统计改为动态读取并重建核验 |
| T2 | 网站迭代 | 已完成节点专题文档 modal、P0/P1/P2 路线图、页脚 8 源、页面手动录入 API Key;本轮修正旧知识块数量文案 |
| T3 | 完整 PRD | 本轮新增 `PRD_ABI智能化独立站.md`,覆盖 14 节点与横切层 |
| T4 | 检索生产化 | T4a/T4b 已完成;线上启用 `BAAI/bge-small-zh-v1.5 + Chroma + Neo4j`,A/B smoke 通过 pass/top1 无退化;`bge-m3` 在轻量 CPU 上未上线 |
| T5 | 网站上线 | 已上线到 `platform.shopify.lute-tlz-dddd.top`;服务器不保存 API Key;真实 provider 问答需用户页面录入 Key |
| T6 | 多源深挖 | 已有 2 条精选内容级萃取;T6 执行队列与离线入库工具已落地;其余视频需字幕;抖音/小红书待用户粘贴清单 |
| T7 | 接 AI-Toolkit/UCP | 测试店受控写验收 Runbook 已落地;真实读写仍待测试店授权与人审批准 |

## B. 各项执行方案
**T1 · 图堆叠修复(P0,0.5 天)**
- 做法:架构图「商业价值」条宽 150→140(让出人审栏 x147);4 个价值块重排进 x33–143;人审栏顶部降到 96.5、标签下移。全景图信息源改 3 块、标签移到块上方不压块。逐张(5 图)截图核验无堆叠。
- 验收:5 张图均无重叠/出血,文字与边框留白充足。

**T2 · 网站迭代(P0,0.5 天)**
- 做法:`build_site_data.py` 已加 `node.docs`(各节点专题文档);再(a)前端节点详情渲染「专题文档」可点开 modal;(b)路线图换 P0/P1/P2;(c)页脚改「8 源 + ABI」;(d)`sources` 注入页脚。重建 `kb_data.js` + `node --check` JS。
- 验收:点节点能看到并打开其专题文档;下一步/页脚为最新;站点统计 298/213/593。

**T3 · 完整 PRD(P0,0.5 天)**
- 做法:基于 §C 的「每节点主-副工具×实现方法」核心表,补全 PRD 文档(背景/定位/用户/范围/架构/各节点功能需求/非功能需求/验收/里程碑/风险)。
- 验收:PRD 覆盖 14 节点 + 横切层,每节点含 主/副工具、实现方法、输入输出、人审闸、验收标准。

**T4 · 检索生产化(P1,已完成基础代码与线上后端启用)**
- 已做:`retriever.py` 可选 `LSA/ST/OpenAI` 嵌入、`numpy/Chroma` store、`JSON/Neo4j` graph backend;`mcp_server` 暴露 `kb_status/kb_search/kb_ask`;新增 `eval_retrieval.py` 和 `neo4j_export.py`。
- T4b 已补:`docker-compose.vector.yml`、`requirements.vector.txt`、`entrypoint.sh`、`compare_retrieval.py` 与 `T4b生产检索启用TODO.md`。
- 本地验收:默认 LSA `eval_retrieval.py` 5/5;vector compose config 已确认;Neo4j dry-run 213 实体 / 593 关系并可导出 Cypher。
- 线上验收:腾讯云启用 `BAAI/bge-small-zh-v1.5 + Chroma + Neo4j`;manifest 为 `embedder=st/store=chroma/vector_dim=512/graph_backend=Neo4jGraphStore`;eval `pass_rate=1.00(5/5)`;A/B smoke 与 LSA baseline 的 pass/top1 持平、MRR 略低,因此只记录“生产后端已启用且关键 smoke 无 pass/top1 退化”。`bge-m3` 因轻量 CPU 前台构建超过 7 分钟未上线。

**T5 · 网站上线(P1,0.5 天,用户侧)**
- 做法:DNS A 记录 → 防火墙 80/443 → `cp .env.example .env`(仅模型配置,不填 Key)→ `docker compose -p shopify-kb up -d --build` → 浏览器页面手动录入 DeepSeek API Key → 验证 https 问答(详见 `site/部署SOP.md`)。
- 验收:`https://platform.shopify.lute-tlz-dddd.top` 可访问且问答可用。

**T6 · 多源深挖(P1,持续)**
- 已补:新增 `90-AI能力地图/T6多源深挖执行队列.md` 与 `tools/t6_multisource_intake.py`,支持把用户粘贴的字幕/帖子/清单转成带 frontmatter 的草稿 Markdown。
- 做法:按「粘贴字幕/清单→离线草稿→8 段结构深度萃取→入图谱/RAG/站点」逐条做高价值视频;抖音/小红书同「粘贴清单→归类」。
- 验收:高价值视频有内容级萃取(非仅标题);新增源进图谱与检索。

**T7 · 接 AI-Toolkit/UCP(P2,1–2 周,用户侧+陪跑)**
- 已补:新增 `10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md`,明确测试店、人审批准、回滚和证据台账。
- 做法:装 `shopify-ai-kb` 插件 + `claude mcp add ... @shopify/dev-mcp` + `shopify auth login`(测试店);跑「读店铺→受控写(人审)」;注册 UCP Agent profile 进 AI 渠道。
- 验收:测试店完成一次 AI 受控上架/改价(人审通过)。

## C. PRD 核心 · 每节点「主-副工具 × 实现方法」
| 节点 | 主工具 | 副工具 | 实现方法 | 人审闸 | 验收 |
|------|--------|--------|----------|--------|------|
| 00 战略定位 | Claude/ChatGPT 研判 | Perplexity · Catalog 可见性 | 季度战略评审 → 写「宪法层」(赛道/区域/红线) | 赛道·红线 | 战略基线+人群画像+单位经济 |
| 01 选品调研 | Helium10/JungleScout + Catalog | Trends/Perplexity · Claude 竞品 · **Accio** 采购 | 数据层(价带/市占/VOC)→ 多视角 Agent → 评分卡;Accio RFQ → 数据桥导入 | 终审选品·下单 | 选品评分卡+候选清单 |
| 02 建站基建 | **AI Toolkit + Dev MCP**(Claude Code) | 主题/OS2.0 · **Hydrogen** · Functions | `claude mcp add` → 自然语言建站/改店;长期 headless 用 Hydrogen→Oxygen | 支付·域名·合规 | 可上线站点+多站点发布流水线 |
| 03 上架 Listing | **Shopify Magic** + Catalog | ChatGPT/DeepSeek · DeepL/Gemini · custom-data | 查 → Magic 文案 → metafields → admin-execution 批量(预演 mutation) | 卖点·措辞·上架 | PDP/集合页/多语言 |
| 04 内容素材 | **Sidekick 出图** + 视频工作流 | Midjourney/Canva/PS · ElevenLabs · Suno · Kling/Runway | 脚本/情绪公式 → 图生图/图生视频 → 配音配乐 → 审片 | 调性·版权 | 素材库+广告视频流水线 |
| 05 营销引流 | **Campaign Autopilot** | Klaviyo/Omnisend · 红人 · 活动页 · Sidekick 扩展 | 设预算 → Autopilot 建活动/分配/优化;邮件流;UTM 打标 | 预算闸·素材合规 | 多渠道闭环+UTM |
| 06 转化 CRO | **Shopify Functions** + Sidekick Pulse | AB 测试 · checkout UI 扩展 · IP 识别 | Pulse 发现机会 → Functions 落地(满赠/折扣/结账校验)→ AB → 复盘 | 实验上线 | 转化提升+实验记录 |
| 07 数据归因 | **GA4/GTM** + Sidekick Pulse | UTM 工具 · BigQuery · 看板 · Magic 多步分析 | 埋点规范 → 采集 → 归因 → 看板/每日简报 | 指标口径 | 归因看板+CLV+自动简报 |
| 08 履约供应链 | **Shopify Flow** + 库存同步 | 菜鸟/FBA/WFS 海外仓 · Storefront MCP 查单 · admin-execution | 阈值 → Flow 告警/自动推单;海外仓对接;退款 | 异常·退款 | 库存同步+自动推单+对话查单 |
| 09 客户会员 | **Store AI + Storefront MCP** | Sidekick 扩展(Loop/Klaviyo)· SCRM · 舆情 · VOC | Store AI 答疑 → VOC/舆情 → 自动分群召回 | 高危工单·升级 | AI 客服+会员体系+召回 |
| 10 自动化编排 | **Claude Code + AI Toolkit + MCP + Flow** | Zapier/Make · **UCP** · 自建编排(CLAUDE.md/Trellis/Skill 库) | 节点 skill 化 → 编排层调度 → 人审兜底 → 监控回滚 | 不可逆写 | 端到端跑通(测试店) |
| 90 AI 能力地图 | 能力清单 + 选型表 | 术语表 | 随 Editions 更新 | — | 选型表+10 步映射 |
| 91 合规风控 | 权限分级 + 操作审计 + 审批闸 | 版权/采集校验 · 拒付控制 | Agent 写操作留痕 + 人审 | 红线操作 | 审计日志+护栏清单 |
| 92 组织 SOP | Agent 工程三件套(CLAUDE.md/AGENTS.md + 记忆 + 人审) | Editions 跟新 SOP | 评审-联调-提测-验收-上线 | — | SOP+运维流水线 |

## D. 里程碑
- **P0(今天–明天)**:T1 修图 · T2 网站迭代 · T3 完整 PRD。
- **P1(1–2 周)**:T5 上线 · T6 多源深挖。
- **P2(1 月+)**:T7 AI-Toolkit/UCP 测试店受控写 → 按《全自动运营蓝图》编排化。

## E. TODO(勾选清单)
- [x] T1 修复全部商业图堆叠(架构/全景)并逐图核验
- [x] T2 网站迭代:节点专题文档渲染 + 下一步P0P1P2 + 页脚8源 + 重建 kb_data
- [x] T3 输出完整 PRD 文档(基于 §C 扩写)
- [x] T4a 检索生产化基础代码(ST/OpenAI + Chroma adapter + Neo4j export/query + MCP status + eval)
- [x] T4b 启用生产后端(BAAI/bge-small-zh-v1.5 + Chroma + 真实 Neo4j + A/B 评测)
- [x] T5 网站上线腾讯云(页面手动录入 Key;服务器不保存 Key)
- [x] T6 多源深挖执行队列 + 离线入库工具
- [ ] T6 视频字幕深度萃取 + 抖音/小红书多源内容入库(待用户提供字幕/清单)
- [x] T7 测试店受控写验收 Runbook
- [ ] T7 接 AI-Toolkit/UCP 测试店真实读写(待授权+人审)

## F. 风险与对策
- 外部站点直抓受限 → 维持「粘贴→归类」流程;不绕过。
- AI 收入类素材夸大 → 仅作打法参考,合规/选型把关(91)。
- execution 真改店铺 → 一律测试店先行 + 人审闸 + 操作日志。
