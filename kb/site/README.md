# Shopify AI 经营知识库 · 网站

## 两种打开方式

### A. 直接看(静态,双击即可)
双击 `index.html` 即可浏览:Command Center、经营路径选择、技术选型中心、全景图、AI 开店 10 步、全流程节点(点击展开 + 完整文档)、能力地图、SOP 库、工程仓库地图、增长作战室、Agent 工作流库、配置与授权中心、执行准备度、风控闸、信息源覆盖与筛选、工具包入口、知识库本地检索、下一步路线图与内容债。
> 此模式下「DeepSeek 问答」使用页面手动录入的 API Key 从浏览器直连 DeepSeek;若浏览器拦截跨域请求,请用 B 模式。

### B. 完整版(含 RAG 代理,推荐)
```bash
cd ../_rag/kb_index && python cli.py build      # 1) 建检索索引(一次)
cd ../../site
pip install -r requirements.txt                  # 2) 装 flask
python server.py                                 # 3) 打开 http://localhost:8000
```
问答流程:页面手动录入 API Key → 你的问题 → 服务端 RAG 检索知识库 top-6 → 拼上下文 → 用本次请求的 API Key 调用 DeepSeek(`deepseek-v4-flash`)→ 返回答案 + 来源。

## 安全
- **Key 不写进任何文件**,部署默认不需要在服务器 `.env` 中配置 `DEEPSEEK_API_KEY`。
- B 模式下 Key 由页面随单次请求发给本服务端,服务端只用于转发 DeepSeek 请求,不落盘、不写日志。
- 勾选“记住到本浏览器”时,Key 仅保存在当前浏览器 localStorage;不勾选则只保留在当前页面内存中。
- Shopify 配置中心只保存测试店域名、审批人、计划变更和证据摘要等非敏感字段到当前浏览器;不要在其中写入 Shopify token、password、private key。

## 文件
- `index.html` 单文件前端 · `kb_data.js` 站点数据(由 `../_build/build_site_data.py` 生成)
- `server.py` 安全后端 · `assets/` 商业图

## 经营作战台模块
- Command Center:首屏展示当前资产、执行状态、授权边界和三条主入口。
- 路径选择:新店冷启动、已有店诊断、Theme 快速上线、Hydrogen 改造、站外增长、联盟红人和 T7 测试店准备 7 条 Journey;T7 Journey 现在包含本地 preflight、development store 域名确认和人审文本。
- 技术选型中心:区分 Theme、Hydrogen、Shopify App、Checkout/UI Extension、CLI/MCP、Storefront MCP/UCP 的场景、输出和风险。
- SOP 库:把建站、Listing、SEO/CRO、增长、中文社媒入库、归因、素材授权、履约库存、客户 VOC、风控、Creator Store Front、UCP 和 T7 Runbook 变成可检索 playbook。
- 工程仓库地图:基于 GitHub P0 官方仓库结构快照,展示 Theme、Hydrogen、App Template、UI Extension、CLI/MCP 的适用场景、输出和边界。
- 增长作战室:把 SEO/GEO、Meta/Google Ads、Reddit、YouTube/PR、KOL/UGC、Affiliate/Creator Store Front、Deal/大促统一到渠道角色、承接、归因指标和复盘节奏。
- Agent 工作流库:市场洞察、内容素材、红人联盟、SEO/GEO、广告诊断、经营复盘 6 类 Agent,并展示任务模板和移交物。
- 配置与授权中心:统一录入测试店域名,生成 T7 preflight 命令、CLI 登录指引、只读/受控写审批文本,并维护浏览器本地证据台账;页面不登录 Shopify、不读写店铺、不保存 Shopify 凭据。
- 执行准备度:T6 多源入库、DeepSeek 问答、T7 测试店本地前置检查、测试店只读、T7 受控写、外部规则核验等能力状态。
- 风控与人审闸:真实店铺写入、Admin API/MCP token、Checkout/UI Extension、社区发帖、UGC 授权、广告预算和折扣佣金。
- 信息源可信度与覆盖:10 信息源 × 14 节点覆盖矩阵,区分本地只读快照、官方资料、本地资料和待外部核验,支持按验证状态筛选证据卡。
- 工具包入口:从站点直接看到本知识库 7 个 skill 的适用节点和文件位置。
- 内容债:P1 已为 `04-内容与素材生产`、`08-订单履约与供应链`、`09-客户与会员运营` 各补一篇最小专题 SOP;T6 已新增 Ac Hampton #11/#16/#17/#21/#24/#26/#29、跨频道长课/战略访谈/Theme/中文建站与高收入话术识别视频萃取,并补中文社媒案例入库 SOP;真实中文平台案例仍待正文或截图文字。

## P1 新增专题 SOP
- `../04-内容与素材生产/AI素材生产与授权SOP.md`:素材 brief、素材标签、UGC/KOL 授权、人审和复用。
- `../08-订单履约与供应链/订单履约与库存同步SOP.md`:库存口径、订单推送、活动前库存检查、售后异常。
- `../09-客户与会员运营/客户会员与VOC闭环SOP.md`:VOC 分类、会员分层、AI 客服升级、人审和复购闭环。

## T6 新增视频萃取
- `../90-AI能力地图/视频深度萃取_AcHampton_AI与履约小批次.md`:Ac Hampton #21/#24/#26 UI 转写级萃取,覆盖 AI 无货源社区选品、AutoDS/Shopify Orders、首单履约、tracking 回填和客户通知。
- `../90-AI能力地图/视频深度萃取_全流程长课与战略访谈.md`:Ac Hampton #17 + Rihab Seb 7 小时长课 + Learn With Shopify 完整教程 + Emma Grede/Shopify President 访谈 UI 转写级萃取,覆盖 AI 建店草稿、人审风控、Sidekick、Marketing Hub、上线前交易检查和受众优先战略。
- `../90-AI能力地图/视频深度萃取_CRO诊断与高收入话术识别.md`:Ac Hampton #11 UI 转写级 CRO 诊断 + Austin Rabin #44 内容级高收入话术识别,覆盖未出单诊断树、流量质量、A/B 实验、客户体验、信息质量和收益证据分层。
- `../90-AI能力地图/视频深度萃取_AppsTheme与中文建站教程.md`:Ac Hampton #16/#29 Apps 页面说明级 v0.1 + Code with Chris Theme 长课 + 梧桐小讲堂中文建站教程,覆盖 App 审计卡、Theme 工程路径和中文新人 onboarding。
- `../05-营销与引流/中文社媒独立站案例入库SOP.md`:抖音/小红书真实案例入库协议,当前只定义证据字段、分类规则和风控闸,不编写无正文案例。
- `rhuYy9LP72M` 已按 browser-harness 页面元数据标为 Mark Tilbury 跨频道候选,不计入 Ac Hampton 覆盖。

## T7 前置补充
- `../10-自动化编排/T7测试店授权前置包.md`:测试店创建、CLI/AI Toolkit/Dev MCP 本地前置、人审文本和低风险测试写入建议。
- `../tools/t7_test_store_preflight.py`:本地只读检查脚本,不登录 Shopify、不访问网络、不读取或写入店铺、不输出密钥值。
- 网站 `#config` 配置与授权中心:把测试店域名、preflight 命令、人审文本和本地证据台账统一到页面内;真实 `shopify auth login`、测试店读取和 mutation 执行仍必须由用户现场确认。
