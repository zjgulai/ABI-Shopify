# -*- coding: utf-8 -*-
import json,os,re,glob
KB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+os.sep
def parse(path):
    t=open(path,encoding="utf-8").read(); meta={}; body=t
    if t.startswith("---"):
        e=t.find("\n---",3); fm=t[3:e]; body=t[e+4:]
        for ln in fm.splitlines():
            m=re.match(r"\s*([A-Za-z_]+):\s*(.*)",ln)
            if m:
                k=m.group(1); v=re.sub(r"\s{2,}#.*$","",m.group(2)).strip()
                if v.startswith("[") and v.endswith("]"): v=[x.strip() for x in v[1:-1].split(",") if x.strip()]
                meta[k]=v
    body=re.sub(r"<!--.*?-->","",body,flags=re.S)
    return meta,body.strip()

def read(path):
    return open(path,encoding="utf-8").read() if os.path.exists(path) else ""

def table_rows(markdown, header_key):
    lines=markdown.splitlines()
    out=[]; active=False; headers=[]
    for ln in lines:
        if not ln.strip().startswith("|"): continue
        cells=[c.strip() for c in ln.strip().strip("|").split("|")]
        if header_key in cells:
            headers=cells; active=True; continue
        if not active: continue
        if all(re.fullmatch(r":?-{2,}:?",c or "") for c in cells): continue
        if len(cells)!=len(headers): continue
        out.append(dict(zip(headers,cells)))
    return out

def load_json(path, default):
    try:
        return json.load(open(path,encoding="utf-8"))
    except Exception:
        return default

def clip(s,n=88):
    s=re.sub(r"\s+"," ",s or "").strip()
    return s[:n-1]+"…" if len(s)>n else s

# nodes
nodes=[]
for d in sorted(glob.glob(KB+"[0-9]*/")):
    p=os.path.join(d,"README.md")
    if not os.path.exists(p): continue
    meta,body=parse(p)
    code=os.path.basename(d.rstrip("/"))
    secs=re.split(r"\n(?=## )",body)
    goal=""; subs=[]
    for s in secs:
        if s.startswith("## 1."): goal=re.sub(r"## 1\..*?\n","",s,1).strip()[:200]
        if s.startswith("## 2."):
            subs=[l.strip("- ").strip() for l in s.splitlines() if l.strip().startswith("- ")]
    docs=[]; doc_sources=[]
    for sub in sorted(glob.glob(os.path.join(d,"*.md"))):
        if os.path.basename(sub)=="README.md": continue
        sm,sb=parse(sub)
        if isinstance(sm.get("sources"),list): doc_sources.extend(sm.get("sources"))
        docs.append({"title":sm.get("title",os.path.basename(sub)[:-3]),"md":sb})
    sources=meta.get("sources",[]) if isinstance(meta.get("sources"),list) else []
    for src in doc_sources:
        if src not in sources: sources.append(src)
    nodes.append({"code":code,"num":code[:2],"name":code[2:].lstrip("-"),
        "layer":meta.get("layer",""),"summary":meta.get("summary",""),
        "sources":sources,
        "goal":goal,"subtopics":subs[:8],"docs":docs,"md":body})

# tool selection table
toolsel={}
selpath=KB+"90-AI能力地图/AI工具选型_每节点.md"
if os.path.exists(selpath):
    _,b=parse(selpath)
    for ln in b.splitlines():
        m=re.match(r"\|\s*(\d{2})\s+([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|",ln)
        if m: toolsel[m.group(1)]={"native":m.group(3).strip(),"external":m.group(4).strip(),"accio":m.group(5).strip(),"tip":m.group(6).strip()}

# 10-step
steps=[["1","找产品","Helium 10 · Jungle Scout","01"],["2","看市场趋势","Google Trends · Perplexity","01"],
["3","分析竞品","ChatGPT · Claude","01"],["4","写 Listing","ChatGPT · DeepSeek","03"],
["5","多语翻译","DeepL · Gemini","03"],["6","做主图和 A+","Midjourney · Canva · PS","04"],
["7","剪广告影片","CapCut · Runway · Kling","04"],["8","做配音","ElevenLabs","04"],
["9","做音乐/氛围音","Suno","04"],["10","自动化营运","Shopify · Zapier · Make","10"]]

# capabilities from KG
G=json.load(open(KB+"_kg/graph.json",encoding="utf-8"))
lab={e["id"]:e["label"] for e in G["entities"]}
caps={}
for e in G["entities"]:
    if e["type"]=="ShopifyCapability":
        sup=[lab[r["target"]] for r in G["relations"] if r["type"]=="SUPPORTS" and r["source"]==e["id"]]
        caps[e["label"]]=sup
# roadmap
roadmap=[
{"phase":"P0 · 已收口","when":"P0","items":["T1/T2/T3/T5 已形成本地或生产证据","页脚 10 源 + ABI,站点统计随 RAG/KG 构建动态刷新","代码与知识库已提交并可按 release 目录部署"]},
{"phase":"P1 · 继续深挖","when":"P1","items":["04/08/09 已补 P1 最小专题 SOP,站点 SOP 库扩展到 12 条","T6 已完成 Ac Hampton #11/#16/#17/#21/#24/#26/#29、跨频道长课/战略访谈/Theme/中文建站/高收入话术识别","中文社媒案例入库 SOP 已就绪,真实抖音/小红书案例仍需帖子正文或截图文字","页面手动录入 DeepSeek API Key 后做真实 provider 问答验收"]},
{"phase":"P2 · 受控写闭环","when":"P2","items":["T7 测试店授权前置包已落地:本地 preflight + 测试店创建清单 + 人审文本","T7 接 AI-Toolkit/UCP 测试店真实读写仍需用户授权","Shopify 测试店授权 + mutation 预览 + 人审批准","按《全自动运营蓝图》把节点 skill 化、编排化"]},
]
nextplan=[
{"t":"P0 · 发布收口","d":"本地 KB/RAG/KG/site 已重建;线上使用 BAAI/bge-small-zh-v1.5 + Chroma + Neo4j,服务器不保存 DeepSeek Key。"},
{"t":"P1 · 内容扩充","d":"04/08/09 最小专题 SOP 已入库;T6 已形成 7 组精选视频萃取,覆盖 AI 建店、履约、长课、CRO、Apps、Theme 和中文建站;中文社媒入库协议已就绪,下一步等真实帖子正文或截图文字。"},
{"t":"P2 · 自动化闭环","d":"T7 前置包已补:本地 preflight、development store 创建清单、授权文本和低风险写入建议;真实读写仍等测试店授权与逐次人审。"},
]

# source registry + coverage
source_registry=[]
for r in table_rows(read(KB+"_meta/信息源清单.md"),"#"):
    source_registry.append({
        "id":r.get("#",""),"name":r.get("信息源",""),"type":r.get("类型",""),
        "status":r.get("状态",""),"landing":r.get("落点","")
    })
coverage_headers=[]; coverage_rows=[]
cov_md=read(KB+"_meta/覆盖矩阵.md")
for ln in cov_md.splitlines():
    if not ln.strip().startswith("|"): continue
    cells=[c.strip() for c in ln.strip().strip("|").split("|")]
    if cells and cells[0]=="节点":
        coverage_headers=cells[1:]; continue
    if not coverage_headers or all(re.fullmatch(r":?-{2,}:?",c or "") for c in cells): continue
    if len(cells)==len(coverage_headers)+1:
        coverage_rows.append({"node":cells[0],"values":cells[1:]})
coverage_matrix={"headers":coverage_headers,"rows":coverage_rows}

# repo playbooks from P0 structure manifest
p0_manifest=load_json(KB+"_sources/github-shopify-repos/p0_structure_manifest_2026-06-28.json",{})
p0_by_repo={r.get("repo"):r for r in p0_manifest.get("records",[])}
repo_groups=[
    {"kind":"Theme","title":"Liquid Theme 基线","repos":["Shopify/dawn","Shopify/skeleton-theme"],
     "fit":"快速上线 Online Store 2.0 主题、首页/PDP/集合页/政策页结构。",
     "output":"theme_structure_ready / section_schema_check / preview_smoke",
     "boundary":"Theme Store 或生产发布前必须人工确认品牌、版权、支付、物流和政策页。"},
    {"kind":"Hydrogen","title":"Headless Storefront","repos":["Shopify/hydrogen","Shopify/storefront-api-examples"],
     "fit":"需要 React/Storefront API/CMS/高性能内容页和复杂前端体验。",
     "output":"route_map / storefront_api_boundary / seo_cache_e2e_smoke",
     "boundary":"不是简单换主题;必须管理 token、部署、缓存、SEO、监控和回滚。"},
    {"kind":"App Template","title":"Shopify App 自动化","repos":["Shopify/shopify-app-template-react-router","Shopify/shopify-app-template-remix"],
     "fit":"要把 Admin API、业务服务、Agent facade 和审批网关做成应用。",
     "output":"app_routes / shopify_adapter / domain_service / audit_log",
     "boundary":"写操作统一 dry_run -> preview -> approval -> execute -> audit_log。"},
    {"kind":"UI Extension","title":"Checkout / Account 扩展","repos":["Shopify/ui-extensions"],
     "fit":"Checkout、客户账户、订单状态等 Shopify host surface 的轻量 CRO。",
     "output":"target_api_version / extension_toml / fixture_test / fallback_plan",
     "boundary":"强版本敏感;必须按 surface、target、api_version 和测试店验收。"},
    {"kind":"CLI / MCP","title":"开发入口与 Agent 接口","repos":["Shopify/cli","Shopify/dev-mcp-gemini-cli"],
     "fit":"统一 App、Theme、Hydrogen、Extension 的脚手架、校验和 Dev MCP 接入。",
     "output":"command_boundary / dev_mcp_setup / test_store_only_plan",
     "boundary":"CLI 认证后可能触发远端操作;Dev MCP 不等于生产 Admin 写权限。"},
]
repo_playbooks=[]
for g in repo_groups:
    records=[]
    for repo in g["repos"]:
        r=p0_by_repo.get(repo,{})
        records.append({
            "repo":repo,"url":r.get("url","https://github.com/"+repo),
            "head":r.get("head_sha_prefix",""),"branch":r.get("branch",""),
            "files":r.get("file_count",0),
            "topDirs":[f"{a}({b})" for a,b in r.get("top_counts",[])[:5]],
            "keyFiles":r.get("key_files",[])[:6],
            "tomlCount":len(r.get("shopify_tomls",[])),
            "testDirs":r.get("test_dirs",[])[:4]
        })
    repo_playbooks.append({**g,"records":records})

growth_playbooks=[
    {"channel":"SEO / GEO","stage":"长期资产","action":"关键词、首页结构、FAQ/博客、内链、GSC 监控","output":"seo_backlog / home_keyword_map / schema_markup_draft","handoff":"06 HOME 页承接 + 07 GSC 复盘","metrics":["impressions","clicks","query_group","landing_page"],"cadence":"周复盘","risk":"规则时效性 needs_external_verification","source":"05/06 platform-operations-wiki"},
    {"channel":"Meta / Google Ads","stage":"冷启动与放量","action":"素材语义分层、小预算测试、否词/受众/落地页联动","output":"creative_test_plan / search_campaign_draft","handoff":"04 素材 + 06 落地页 + 07 归因","metrics":["spend","ctr","cpa","roas","asset_tag"],"cadence":"日监控/周复盘","risk":"预算、宣称、素材授权必须人审","source":"05/07/91 platform-operations-wiki"},
    {"channel":"Reddit GEO","stage":"信任问答","action":"选择真实问题帖,写中立完整回答,披露品牌关联","output":"reddit_answer_brief","handoff":"05 社区内容 + 91 风控","metrics":["thread_quality","brand_search_lift","referral_clicks"],"cadence":"发帖前核验/周复盘","risk":"社区规则与隐藏推广高风险","source":"05/91 platform-operations-wiki"},
    {"channel":"YouTube / PR","stage":"高信任解释","action":"红人筛选、PR pitch、样品、返稿和媒体外链","output":"youtube_creator_list / pr_outreach_queue","handoff":"04 素材复用 + 05 引流","metrics":["creator_fit","reply_rate","published_assets","referral_orders"],"cadence":"双周推进","risk":"联系信息、价格、频道状态需实时核验","source":"05/91 platform-operations-wiki"},
    {"channel":"KOL / UGC","stage":"内容供给","action":"候选池、邀约、寄样、授权、返稿、素材复用","output":"creator_pipeline / ugc_asset_register","handoff":"04 素材库 + 06 PDP 信任区","metrics":["asset_count","ad_usage_allowed","creator_orders","ugc_reuse_rate"],"cadence":"周入库/周授权复核","risk":"自然发布授权不自动等于广告/官网授权","source":"05/91/92 platform-operations-wiki"},
    {"channel":"Affiliate / Creator Store Front","stage":"长期分销","action":"专属页面、链接、折扣码、佣金、订单归因","output":"affiliate_storefront_plan","handoff":"05 增长 + 07 creator_id 归因","metrics":["creator_id_orders","coupon_orders","commission_roi","refund_rate"],"cadence":"周结算/月复盘","risk":"佣金、折扣和 Cookie 规则必须透明记录","source":"05/07 platform-operations-wiki"},
    {"channel":"Deal / 大促","stage":"爆发与清货","action":"预热、爆发、返场;库存/客服/预算联动","output":"promotion_war_room_plan","handoff":"08 库存 + 09 客服 + 07 复盘","metrics":["stock_guard","orders","refund_rate","support_load"],"cadence":"活动前/中/后三段复盘","risk":"虚假折扣、虚假原价、退款压力和品牌伤害","source":"00/05/92 platform-operations-wiki"},
]

agent_workflows=[
    {"agent":"市场洞察 Agent","input":"评论、竞品、关键词、趋势、社媒内容","output":"人群、痛点、卖点、机会缺口","review":"品类方向、合规预检","taskTemplate":"输入品类 brief -> 生成机会矩阵 -> 标记证据等级 -> 交给选品/定位人审","handoff":"选品评分卡 / 战略基线","nodes":["00","01","07"]},
    {"agent":"内容素材 Agent","input":"卖点、场景、渠道规格、历史表现","output":"脚本、图片 brief、视频 brief、素材标签","review":"功效宣称、素材授权","taskTemplate":"读取 PDP 卖点 -> 生成素材 brief -> 产出标签和授权清单 -> 进入素材人审","handoff":"creative_brief / asset_register","nodes":["04","05","91"]},
    {"agent":"红人/联盟 Agent","input":"creator list、粉丝画像、预算、合作记录","output":"红人分层、邀约话术、合作条款草案","review":"佣金、合同、寄样、授权","taskTemplate":"筛选 creator -> 生成邀约 -> 拆佣金/折扣/UTM -> 交给 BD 人审","handoff":"creator_pipeline / affiliate_storefront_plan","nodes":["05","07","92"]},
    {"agent":"SEO/GEO Agent","input":"关键词、GSC、页面结构、FAQ、社区问题","output":"首页 SEO、博客/FAQ、Reddit 回答草案","review":"官方规则、社区规则、品牌披露","taskTemplate":"聚合查询和问题 -> 匹配页面/FAQ -> 生成草稿 -> 标记待外部核验","handoff":"home_keyword_map / reddit_answer_brief","nodes":["05","06","91"]},
    {"agent":"广告诊断 Agent","input":"广告报表、素材标签、落地页、订单","output":"浪费流量、胜出素材、扩量/停投建议","review":"预算、上线、否词和素材替换","taskTemplate":"读取 spend/ROAS/asset_tag -> 找浪费与胜出项 -> 输出预算建议 -> 人审后执行","handoff":"creative_test_matrix / weekly_review","nodes":["05","06","07"]},
    {"agent":"经营复盘 Agent","input":"订单、库存、渠道、客服、广告、内容","output":"日/周/月复盘、异常预警、SOP 更新建议","review":"经营结论、生产写操作","taskTemplate":"聚合订单/库存/VOC/渠道 -> 生成异常和行动项 -> 写入复盘 -> owner 确认","handoff":"closed_loop_report / operating_review","nodes":["07","08","09","92"]},
]

risk_gates=[
    {"gate":"真实店铺写入","status":"test_store_only","trigger":"商品、价格、库存、主题、折扣、订单、客户数据写操作","review":"dry_run -> preview -> explicit approval -> execute -> audit_log","source":"10 AI-Toolkit/UCP Runbook"},
    {"gate":"Admin API / MCP token","status":"manual_review_required","trigger":"Admin GraphQL、社区 MCP、店铺 token、客户/订单数据","review":"scope、日志、遥测、只读模式、安全审查","source":"10/91 GitHub MCP 风控"},
    {"gate":"Checkout / UI Extension","status":"manual_review_required","trigger":"checkout、customer account、order status surface 变更","review":"target、api_version、fallback、测试店 E2E","source":"06 GitHub Checkout SOP"},
    {"gate":"社区发帖 / Reddit GEO","status":"needs_external_verification","trigger":"品牌提及、链接、产品推荐、账号身份动作","review":"版规、披露、贡献比例、反刷量检查","source":"91 社区风控"},
    {"gate":"UGC / KOL 素材复用","status":"manual_review_required","trigger":"红人内容进入广告、官网、EDM、SEO、PDP","review":"usage_scope、duration、territory、ad_usage_allowed、approval_record","source":"91 素材授权"},
    {"gate":"广告预算 / 折扣佣金","status":"manual_review_required","trigger":"扩预算、上线广告、折扣码、佣金、Deal 站","review":"预算上限、利润、虚假折扣、归因透明、回滚方式","source":"05/07/91/92 增长 SOP"},
]

journeys=[
    {"id":"new-store-0-1","title":"新店 0-1 冷启动","stage":"P0","audience":"品牌负责人 / 运营负责人",
     "complexity":"中","readiness":"local_ready","nodes":["00","01","02","03","05","07","91"],
     "inputs":["品类 brief","目标市场","预算边界","供应商线索"],
     "outputs":["战略基线","选品评分卡","站点结构","PDP 草稿","UTM 规范"],
     "sops":["独立站 0 到 1 建站 SOP","Listing 内容工厂 SOP","全域增长数据归因 SOP"],
     "riskGates":["支付/域名/政策页","素材授权","广告预算"],
     "ask":"我是 Shopify 新店冷启动,下一步应该按什么路径做?"},
    {"id":"store-diagnosis","title":"已有 Shopify 店铺诊断","stage":"P0","audience":"运营负责人 / 增长负责人",
     "complexity":"中","readiness":"local_ready","nodes":["02","03","05","06","07","91"],
     "inputs":["店铺 URL","核心页面","流量来源","订单/广告/GA/GSC 摘要"],
     "outputs":["站点问题清单","CRO 假设","渠道归因缺口","优先级路线图"],
     "sops":["HOME 页 SEO 与落地页承接 SOP","全域增长数据归因 SOP"],
     "riskGates":["平台规则待核验","指标口径人审"],
     "ask":"已有 Shopify 店铺应该如何做站点、增长和归因诊断?"},
    {"id":"theme-launch","title":"Theme 快速上线","stage":"P0","audience":"运营负责人 / 开发执行者",
     "complexity":"低","readiness":"local_ready","nodes":["02","03","06","91"],
     "inputs":["品牌资产","主题选择","PDP/集合页字段","政策页清单"],
     "outputs":["页面结构","主题改造清单","上线前检查表"],
     "sops":["独立站 0 到 1 建站 SOP","GitHub P0 官方仓库工程结构 SOP"],
     "riskGates":["支付/政策页/物流/隐私上线人审"],
     "ask":"Theme 快速上线 Shopify 独立站需要哪些步骤和验收?"},
    {"id":"hydrogen-headless","title":"Hydrogen / Headless 改造","stage":"P1","audience":"技术负责人 / 开发执行者",
     "complexity":"高","readiness":"manual_review_required","nodes":["02","06","07","10","91"],
     "inputs":["Storefront API 边界","路由/SEO 需求","部署目标","缓存与监控要求"],
     "outputs":["route_map","storefront_api_boundary","seo_cache_smoke","rollback_plan"],
     "sops":["Hydrogen 脚手架 SOP","GitHub Hydrogen 与 Theme 工程实践"],
     "riskGates":["token scope","SEO/cache","部署回滚"],
     "ask":"Theme 与 Hydrogen 在 Shopify 独立站建站中如何选择?"},
    {"id":"full-funnel-growth","title":"站外全域增长","stage":"P0","audience":"增长负责人 / 运营负责人",
     "complexity":"中","readiness":"needs_external_verification","nodes":["04","05","06","07","91","92"],
     "inputs":["渠道目标","素材资产","落地页","UTM 规则","预算边界"],
     "outputs":["渠道作战计划","素材测试矩阵","承接页 brief","复盘模板"],
     "sops":["独立站全域流量增长 SOP","AI 素材生产与授权 SOP","站外渠道风控 SOP","HOME 页 SEO 与落地页承接 SOP"],
     "riskGates":["预算人审","素材授权","社区/平台规则待核验"],
     "ask":"站外全域流量增长 SOP 应该如何串联 SEO、广告、红人和归因?"},
    {"id":"creator-storefront","title":"Creator Store Front / 联盟红人","stage":"P1","audience":"增长负责人 / 红人运营",
     "complexity":"中","readiness":"manual_review_required","nodes":["04","05","07","91","92"],
     "inputs":["creator list","佣金规则","折扣码","授权条款","归因字段"],
     "outputs":["creator_pipeline","affiliate_storefront_plan","ugc_asset_register"],
     "sops":["Creator Store Front 联盟红人 SOP","AI 素材生产与授权 SOP","社区营销与素材授权风控 SOP"],
     "riskGates":["佣金/折扣人审","UGC 授权","Cookie/归因透明"],
     "ask":"Creator Store Front 和联盟红人如何落地并控制素材授权风险?"},
    {"id":"t7-readiness","title":"T7 测试店自动化准备","stage":"P2","audience":"开发执行者 / 审批人",
     "complexity":"高","readiness":"blocked_auth","nodes":["10","90","91","92"],
     "inputs":["development store 域名","本地 preflight 输出","shopify auth login","mutation 预案","审批文本"],
     "outputs":["preflight_report","只读连接证据","低风险写入预案","审批台账","回滚记录"],
     "sops":["T7 测试店授权前置包","AI-Toolkit / UCP 测试店受控写验收 Runbook","UCP 接入 SOP"],
     "riskGates":["test_store_only","manual_review_required","no_production_write"],
     "ask":"T7 测试店授权前置要检查什么,为什么不能直接写店铺?"},
]

technical_routes=[
    {"id":"theme","label":"Theme / Liquid","bestFor":"快速上线 Online Store 2.0 首页、PDP、集合页和政策页。",
     "decisionHint":"已有标准 Shopify 店铺、重视上线速度、前端定制复杂度低时优先选。",
     "repoRefs":["Shopify/dawn","Shopify/skeleton-theme"],"nodes":["02","03","06"],
     "outputs":["theme_structure_ready","section_schema_check","preview_smoke"],
     "riskGates":["发布前人工确认品牌、版权、支付、物流和政策页"],"readiness":"local_ready"},
    {"id":"hydrogen","label":"Hydrogen / Headless","bestFor":"React 前端、Storefront API、复杂内容体验和独立部署。",
     "decisionHint":"需要 Headless 体验、复杂路由、内容性能和自定义前端时选。",
     "repoRefs":["Shopify/hydrogen","Shopify/storefront-api-examples"],"nodes":["02","06","10"],
     "outputs":["route_map","storefront_api_boundary","seo_cache_smoke"],
     "riskGates":["Storefront API token","部署回滚","SEO/cache 监控"],"readiness":"manual_review_required"},
    {"id":"app","label":"Shopify App / Admin API","bestFor":"Admin API、业务服务、Agent facade 和审批网关。",
     "decisionHint":"需要读写商品、订单、客户、折扣、店铺设置时必须进入 App/Admin API 路线。",
     "repoRefs":["Shopify/shopify-app-template-react-router","Shopify/shopify-app-template-remix"],"nodes":["03","07","10","91"],
     "outputs":["app_routes","shopify_adapter","audit_log"],
     "riskGates":["scope","dry_run","preview","approval","audit_log"],"readiness":"manual_review_required"},
    {"id":"extension","label":"Checkout / UI Extension","bestFor":"Checkout、Customer Account、Order Status 等 host surface 的轻量 CRO。",
     "decisionHint":"涉及结账或账户页面扩展时选,但必须测试店和版本校验。",
     "repoRefs":["Shopify/ui-extensions"],"nodes":["06","91"],
     "outputs":["target_api_version","extension_toml","fixture_test","fallback_plan"],
     "riskGates":["target","api_version","checkout E2E","fallback"],"readiness":"manual_review_required"},
    {"id":"cli-mcp","label":"CLI / Dev MCP","bestFor":"统一 App、Theme、Hydrogen、Extension 的脚手架、校验和 Agent 开发入口。",
     "decisionHint":"适合开发环境和 Codex/Claude 辅助工程,不等于生产 Admin 写权限。",
     "repoRefs":["Shopify/cli","Shopify/dev-mcp-gemini-cli"],"nodes":["02","10","92"],
     "outputs":["command_boundary","dev_mcp_setup","test_store_only_plan"],
     "riskGates":["CLI 认证","目标店确认","测试店优先"],"readiness":"requires_user_input"},
    {"id":"storefront-mcp-ucp","label":"Storefront MCP / UCP","bestFor":"面向买家和 AI channel 的商品发现、购物车、身份和结账 readiness。",
     "decisionHint":"当前只展示 readiness,后续按官方入口和测试店授权推进。",
     "repoRefs":["Shopify Storefront MCP","UCP 接入 SOP"],"nodes":["10","90","91"],
     "outputs":["agent_profile_plan","catalog_readiness","cart_checkout_boundary"],
     "riskGates":["identity","payment mandate","order management audit"],"readiness":"needs_external_verification"},
]

sop_playbooks=[
    {"id":"dtc-0-1","title":"独立站 0 到 1 建站 SOP","nodes":["00","02","03","91"],"scenario":"新店从定位、基础设施、政策页到预览上线。",
     "inputs":["品牌定位","产品资料","域名/支付/物流清单"],"outputs":["站点结构","上线前检查表"],"source":"kb/02-建站与基础设施/平台运营Wiki_独立站0到1建站SOP.md","verification":"local_material_needs_external_verification"},
    {"id":"listing-factory","title":"Listing 内容工厂 SOP","nodes":["03","04","06","91"],"scenario":"把商品资料转成 PDP、SEO、多语言和素材 brief。",
     "inputs":["商品资料","关键词","认证/卖点"],"outputs":["PDP 草稿","SEO 字段","素材 brief"],"source":"kb/03-商品上架与Listing/Listing内容工厂SOP.md","verification":"local_ready"},
    {"id":"home-seo","title":"HOME 页 SEO 与落地页承接 SOP","nodes":["05","06","07"],"scenario":"自然搜索与站外流量进入首页/落地页后的承接。",
     "inputs":["关键词","渠道意图","目标页面","GSC/GA 数据"],"outputs":["keyword_map","landing_page_brief","measurement_plan"],"source":"kb/06-转化优化CRO/平台运营Wiki_HOME页SEO与落地页承接SOP.md","verification":"needs_external_verification"},
    {"id":"growth-all-channel","title":"独立站全域流量增长 SOP","nodes":["04","05","06","07","91"],"scenario":"SEO、广告、社区、红人、联盟和大促的增长闭环。",
     "inputs":["渠道目标","素材资产","预算","承接页"],"outputs":["channel_plan","creative_test_plan","utm_plan"],"source":"kb/05-营销与引流/平台运营Wiki_独立站全域流量增长SOP.md","verification":"needs_external_verification"},
    {"id":"cn-social-intake","title":"中文社媒独立站案例入库 SOP","nodes":["01","04","05","06","91"],"scenario":"把抖音/小红书帖子正文、截图 OCR 和评论摘要转成选品、素材、渠道、承接和风控卡。",
     "inputs":["帖子正文","截图文字","评论摘要","来源链接"],"outputs":["product_signal_card","creative_angle_card","channel_case_card","risk_review_card"],"source":"kb/05-营销与引流/中文社媒独立站案例入库SOP.md","verification":"source_schema_only"},
    {"id":"attribution","title":"全域增长数据归因 SOP","nodes":["05","07","92"],"scenario":"用 UTM、GA、GSC、广告数据和订单数据复盘渠道。",
     "inputs":["UTM 规则","GA/GSC/Ads export","订单数据"],"outputs":["channel_roi","creator_id_report","weekly_review"],"source":"kb/07-数据与归因/平台运营Wiki_全域增长数据归因SOP.md","verification":"local_material_needs_external_verification"},
    {"id":"community-ugc-risk","title":"社区营销与素材授权风控 SOP","nodes":["04","05","91"],"scenario":"Reddit、UGC、KOL 素材复用和隐藏推广风险控制。",
     "inputs":["发帖 brief","UGC 授权","creator 合同"],"outputs":["risk_checklist","approval_record","asset_register"],"source":"kb/91-合规与风控/平台运营Wiki_社区营销与素材授权风控.md","verification":"needs_external_verification"},
    {"id":"ai-asset-rights","title":"AI 素材生产与授权 SOP","nodes":["04","05","91"],"scenario":"把 AI 生成、UGC/KOL 和广告素材纳入 brief、标注、授权和人审。",
     "inputs":["商品资料","渠道需求","品牌约束","授权记录"],"outputs":["creative_brief","asset_register","creative_test_matrix"],"source":"kb/04-内容与素材生产/AI素材生产与授权SOP.md","verification":"local_material_needs_external_verification"},
    {"id":"fulfillment-inventory","title":"订单履约与库存同步 SOP","nodes":["08","09","07","91"],"scenario":"把订单、库存、海外仓/3PL、客服和售后组织成可审计履约闭环。",
     "inputs":["SKU 主数据","库存口径","仓库/3PL 信息","Shopify 订单"],"outputs":["inventory_sync_policy","fulfillment_queue","activity_stock_guard"],"source":"kb/08-订单履约与供应链/订单履约与库存同步SOP.md","verification":"local_material_needs_external_verification"},
    {"id":"customer-voc-loop","title":"客户会员与 VOC 闭环 SOP","nodes":["09","07","08","91"],"scenario":"把客户账户、会员权益、客服工单、评论/VOC、社区反馈串成复购闭环。",
     "inputs":["客户账户","订单行为","客服工单","评论/VOC"],"outputs":["voc_taxonomy","customer_segments","closed_loop_report"],"source":"kb/09-客户与会员运营/客户会员与VOC闭环SOP.md","verification":"local_material_needs_external_verification"},
    {"id":"creator-storefront","title":"Creator Store Front 联盟红人 SOP","nodes":["04","05","07","91","92"],"scenario":"用 creator_id、专属页面、折扣码、佣金和素材授权把红人合作做成长期分销渠道。",
     "inputs":["creator list","佣金规则","折扣码","UGC 授权"],"outputs":["creator_pipeline","affiliate_storefront_plan","ugc_asset_register"],"source":"kb/05-营销与引流/平台运营Wiki_独立站全域流量增长SOP.md","verification":"needs_external_verification"},
    {"id":"ucp-onboarding","title":"UCP 接入 SOP","nodes":["10","90","91"],"scenario":"商品进入 AI channel 的 agent profile、Catalog、Cart、Identity readiness。",
     "inputs":["Developer Dashboard","Catalog 数据","政策/FAQ","Shop Pay 状态"],"outputs":["agent_profile_plan","catalog_readiness"],"source":"kb/10-自动化编排/UCP接入SOP.md","verification":"needs_external_verification"},
    {"id":"t7-runbook","title":"AI-Toolkit / UCP 测试店受控写验收 Runbook","nodes":["10","91","92"],"scenario":"测试店读写能力的授权、人审、回滚和证据台账。",
     "inputs":["测试店授权","mutation 预案","审批文本"],"outputs":["pre_read","approval_log","post_read","rollback_record"],"source":"kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md","verification":"blocked_auth"},
    {"id":"t7-preflight","title":"T7 测试店授权前置包","nodes":["10","90","91","92"],"scenario":"在 Shopify 登录和 Dev MCP 连接前,先做本地 CLI/插件/目标店/人审文本准备。",
     "inputs":["development store domain","node/npm/npx/git","shopify-ai-kb marketplace","approval boundary"],"outputs":["preflight_report","manual_auth_checklist","low_risk_mutation_plan"],"source":"kb/10-自动化编排/T7测试店授权前置包.md","verification":"blocked_auth_preflight_ready"},
]

execution_readiness=[
    {"id":"local-kb","label":"本地 KB / RAG / KG / site","status":"local_ready","detail":"可本地重建、检索和静态预览。","requires":["repo files"],"forbidden":[],"runbook":"kb/site/README.md"},
    {"id":"deepseek-rag","label":"DeepSeek RAG 问答","status":"requires_user_input","detail":"页面手动录入 API Key;默认不写服务器环境。","requires":["页面 API Key"],"forbidden":["把 Key 写入 Git","把 Key 写入前端静态文件"],"runbook":"kb/site/README.md"},
    {"id":"t6-intake","label":"T6 多源深挖入库","status":"requires_user_input","detail":"已完成 7 组视频深度萃取和中文社媒案例入库 SOP;真实抖音/小红书案例仍需要正文、截图文字或评论摘要。","requires":["字幕/清单/帖子","browser-harness 可读转写","截图文字或评论摘要"],"forbidden":["绕过平台限制","编写无证据案例"],"runbook":"kb/90-AI能力地图/T6多源深挖执行队列.md"},
    {"id":"test-store-preflight","label":"T7 测试店本地前置检查","status":"blocked_auth_preflight_ready","detail":"已补本地只读 preflight 脚本;下一步等用户提供 development store 域名并现场授权。","requires":["python3 kb/tools/t7_test_store_preflight.py --store-domain your-dev-store.myshopify.com","Node.js 22.12+","Git 2.28+","测试店域名确认"],"forbidden":["shopify auth login without user","secret values in logs"],"runbook":"kb/10-自动化编排/T7测试店授权前置包.md"},
    {"id":"test-store-read","label":"Shopify 测试店只读连接","status":"blocked_auth","detail":"待用户完成测试店授权。","requires":["preflight_report","shopify auth login","测试店确认"],"forbidden":["读取生产敏感数据"],"runbook":"kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md"},
    {"id":"t7-controlled-write","label":"T7 测试店受控写入","status":"blocked_auth","detail":"必须先只读、再 mutation preview、再明确人审。","requires":["test_store","mutation preview","explicit approval"],"forbidden":["production store write","payment","refund","real ad spend"],"runbook":"kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md"},
    {"id":"external-rules","label":"SEO/GEO/社区/广告规则","status":"needs_external_verification","detail":"时效规则执行前需官方或一手材料复核。","requires":["最新官方/平台规则"],"forbidden":["把本地资料包装成官方事实"],"runbook":"kb/91-合规与风控/站外渠道风控SOP.md"},
]

configuration_center={
    "storageKey":"abi.shopify.config.v1",
    "statuses":[
        {"id":"deepseek-key","label":"DeepSeek RAG Key","status":"requires_user_input","detail":"页面手动录入;服务器不保存。"},
        {"id":"shopify-store-domain","label":"Shopify 测试店域名","status":"requires_user_input","detail":"仅保存 name.myshopify.com 格式域名,不保存 token。"},
        {"id":"t7-preflight","label":"T7 本地前置检查","status":"blocked_auth_preflight_ready","detail":"复制命令到本机终端执行;线上站点不代跑。"},
        {"id":"shopify-read-write","label":"Shopify 读写","status":"blocked_auth","detail":"未登录、未读取、未写入;需用户现场授权。"},
    ],
    "commandTemplates":{
        "preflight":"python3 kb/tools/t7_test_store_preflight.py --store-domain {store_domain}",
        "authLogin":"shopify auth login",
        "readOnlyCheck":"shopify auth whoami",
    },
    "approvalTemplates":{
        "readOnly":"同意在 {store_domain} 测试店执行 T7 只读连接检查。",
        "controlledWrite":"同意仅在 {store_domain} 测试店,对 {target} 执行本次 mutation: {planned_change};禁止生产店写入和资金动作。",
    },
    "forbidden":[
        "不要在页面输入 Shopify password/token/private key。",
        "不要把 Shopify token 写入 Git、kb_data.js 或前端静态文件。",
        "不要从线上服务器执行本机 preflight 或 Shopify auth login。",
        "不要在未生成 mutation preview 和未逐次人审前写店铺。",
    ],
    "officialLinks":[
        {"label":"Shopify CLI","url":"https://shopify.dev/docs/api/shopify-cli"},
        {"label":"Development stores","url":"https://shopify.dev/docs/apps/build/dev-dashboard/stores/development-stores"},
        {"label":"Generated test data","url":"https://shopify.dev/docs/api/development-stores/generated-test-data"},
        {"label":"Shopify AI Toolkit","url":"https://shopify.dev/docs/apps/build/ai-toolkit"},
    ],
}

evidence_items=[
    {"claim":"当前网站采用静态优先单页和 kb_data.js 数据驱动。","source":"kb/site/index.html + kb/_build/build_site_data.py","status":"local_ready","nodes":["90","92"]},
    {"claim":"T7 测试店本地前置包已落地,真实读写仍待测试店授权和人审批准。","source":"kb/10-自动化编排/T7测试店授权前置包.md","status":"blocked_auth_preflight_ready","nodes":["10","91","92"]},
    {"claim":"T7 真实读写待测试店授权和人审批准。","source":"kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md","status":"blocked_auth","nodes":["10","91","92"]},
    {"claim":"GitHub P0 工程地图覆盖 Theme、Hydrogen、App、UI Extension、CLI/MCP。","source":"kb/_build/build_site_data.py repo_groups","status":"local_ready","nodes":["02","06","10"]},
    {"claim":"SEO/GEO、Reddit、广告算法等时效规则需要外部核验。","source":"kb/_meta/信息源清单.md + platform-operations-wiki 萃取","status":"needs_external_verification","nodes":["05","06","91"]},
    {"claim":"P1 已为 04/08/09 补齐最小专题 SOP,用于素材、履约和客户 VOC 的下钻检索。","source":"kb/04-内容与素材生产/AI素材生产与授权SOP.md + kb/08-订单履约与供应链/订单履约与库存同步SOP.md + kb/09-客户与会员运营/客户会员与VOC闭环SOP.md","status":"local_material_needs_external_verification","nodes":["04","08","09"]},
    {"claim":"T6 已完成 Ac Hampton #11/#16/#17/#21/#24/#26/#29,并完成 Rihab Seb / Learn With Shopify / Emma Grede / Austin Rabin / Code with Chris / 梧桐小讲堂跨频道资料萃取。","source":"kb/90-AI能力地图/视频深度萃取_精选.md + kb/90-AI能力地图/视频深度萃取_AppsTheme与中文建站教程.md","status":"local_ready","nodes":["00","01","02","03","05","06","07","08","09","10","90","91","92"]},
    {"claim":"抖音/小红书真实案例尚未提供正文或截图文字;当前仅完成中文社媒独立站案例入库 SOP。","source":"kb/05-营销与引流/中文社媒独立站案例入库SOP.md","status":"requires_user_input","nodes":["01","04","05","06","91"]},
]

query_presets=[
    {"label":"新店冷启动怎么做?","query":"我是 Shopify 新店冷启动,下一步应该按什么路径做?","context":["00","01","02","03","05"]},
    {"label":"Theme vs Hydrogen","query":"Theme 与 Hydrogen 在 Shopify 独立站建站中如何选择?分别适合什么场景和风险边界?","context":["02","10","91"]},
    {"label":"App 接入怎么审?","query":"Shopify App 接入前应该检查哪些权限、数据、脚本注入、指标和回滚边界?","context":["02","06","07","91"]},
    {"label":"中文社媒怎么入库?","query":"抖音和小红书独立站案例应该用哪些字段入库,如何区分选品信号、素材角度和风控?","context":["01","04","05","91"]},
    {"label":"T7 前置检查","query":"T7 测试店授权前置要检查什么,为什么不能直接写店铺?","context":["10","90","91","92"]},
    {"label":"T7 为什么不能直接写?","query":"T7 当前为什么不能直接写店铺,需要哪些授权和人审步骤?","context":["10","91","92"]},
    {"label":"Creator Store Front","query":"Creator Store Front 和联盟红人如何落地并控制素材授权风险?","context":["05","07","91"]},
    {"label":"素材授权怎么做?","query":"AI 素材生产与 UGC/KOL 素材授权应该怎么做 SOP 和验收?","context":["04","05","91"]},
    {"label":"履约库存怎么控?","query":"Shopify 订单履约与库存同步应该如何设置风险闸和活动前库存检查?","context":["08","09","07"]},
    {"label":"VOC 闭环怎么做?","query":"客户会员与 VOC 闭环 SOP 如何连接客服、复购、履约和素材优化?","context":["09","08","04","07"]},
    {"label":"哪些内容待核验?","query":"当前知识库中哪些平台规则、SEO/GEO、社区或广告内容需要外部核验?","context":["05","06","91"]},
]

skill_catalog=[]
for sp in sorted(glob.glob(KB+"skills/*/SKILL.md")):
    sm,sb=parse(sp)
    node="90"
    m=re.search(r"节点\s*(\d{2})",sb)
    if m: node=m.group(1)
    elif "Hydrogen" in sb or "建站" in sb: node="02"
    elif "Listing" in sb: node="03"
    elif "CRO" in sb or "Functions" in sb: node="06"
    elif "履约" in sb or "库存" in sb: node="08"
    elif "UCP" in sb or "MCP" in sb: node="10"
    skill_catalog.append({
        "name":sm.get("name",os.path.basename(os.path.dirname(sp))),
        "description":sm.get("description",""),
        "node":node,
        "file":os.path.relpath(sp,KB),
        "summary":clip(re.sub(r"^#.*?\n","",sb,1),120)
    })

# chunks
chunks=[]
for ln in open(KB+"_rag/chunks.jsonl",encoding="utf-8"):
    o=json.loads(ln); chunks.append({"doc":o["doc_title"],"sec":o["section"],"stage":o.get("stage",""),
        "src":o.get("sources",[]),"file":o["source_file"],"text":o["text"]})

chunk_by_stage={}
for c in chunks:
    st=(c.get("stage") or "")[:2]
    if st: chunk_by_stage[st]=chunk_by_stage.get(st,0)+1
node_readiness=[]; content_debt=[]
for n in nodes:
    doc_count=len(n.get("docs",[]))
    chunk_count=chunk_by_stage.get(n["num"],0)
    if doc_count==0:
        status="content_debt"
        reason="当前只有 README 或基础节点说明,缺少可下钻专题文档。"
        rec_map={
            "04":["AI 素材生产与授权 SOP","UGC 素材授权 SOP","广告素材测试矩阵"],
            "08":["订单履约与库存同步 SOP","3PL/ERP/WMS 数据边界","售后与退货 SOP"],
            "09":["客户会员分层 SOP","VOC 闭环 SOP","复购生命周期运营 SOP"],
        }
        recommended=rec_map.get(n["num"],["补充专题 SOP"])
        content_debt.append({"node":n["code"],"status":status,"docCount":doc_count,"chunkCount":chunk_count,"reason":reason,"recommendedDocs":recommended})
    elif doc_count<2:
        status="partial"
        reason="已有专题资料,但仍建议补充场景化 SOP。"
        recommended=[]
    else:
        status="ready"
        reason="已有多个专题文档支撑页面下钻。"
        recommended=[]
    node_readiness.append({"node":n["code"],"num":n["num"],"name":n["name"],"docCount":doc_count,
        "chunkCount":chunk_count,"status":status,"reason":reason,"recommendedDocs":recommended})

command_center={
    "title":"ABI 智能化独立站经营作战台",
    "subtitle":"把 Shopify/DTC 知识、工程选型、增长 SOP、Agent 工作流和风险闸口组织成可执行经营路径。",
    "kpis":[
        {"label":"流程节点","value":len(nodes)},
        {"label":"知识块","value":len(chunks)},
        {"label":"图谱实体","value":len(G["entities"])},
        {"label":"图谱关系","value":len(G["relations"])},
    ],
    "snapshots":[
        {"label":"本地知识库","status":"local_ready","detail":"14 节点已入站点"},
        {"label":"RAG / KG / Site","status":"local_ready","detail":"可本地重建与检索"},
        {"label":"DeepSeek 问答","status":"requires_user_input","detail":"页面手动录入 API Key"},
        {"label":"T7 测试店前置","status":"blocked_auth_preflight_ready","detail":"本地 preflight 已落地"},
        {"label":"T7 测试店写入","status":"blocked_auth","detail":"待测试店授权与人审"},
    ],
    "guardrails":["不保存 API Key","测试店先行","写操作需人审","时效规则待核验"]
}

data={"nodes":nodes,"toolsel":toolsel,"steps":steps,"caps":caps,"roadmap":roadmap,"nextplan":nextplan,
      "sourceRegistry":source_registry,"coverageMatrix":coverage_matrix,
      "repoPlaybooks":repo_playbooks,"growthPlaybooks":growth_playbooks,
      "agentWorkflows":agent_workflows,"riskGates":risk_gates,"skillCatalog":skill_catalog,
      "commandCenter":command_center,"journeys":journeys,"technicalRoutes":technical_routes,
      "nodeReadiness":node_readiness,"sopPlaybooks":sop_playbooks,
      "executionReadiness":execution_readiness,"evidenceItems":evidence_items,
      "queryPresets":query_presets,"contentDebt":content_debt,
      "configurationCenter":configuration_center,
      "chunks":chunks,"stats":{"nodes":len(nodes),"chunks":len(chunks),
      "entities":len(G["entities"]),"relations":len(G["relations"])}}
out=KB+"site/kb_data.js"
open(out,"w",encoding="utf-8").write("window.KB="+json.dumps(data,ensure_ascii=False)+";")
print("kb_data.js:",os.path.getsize(out)//1024,"KB | nodes",len(nodes),"chunks",len(chunks),"caps",len(caps),"toolsel",len(toolsel))
print("sample node:",nodes[2]["num"],nodes[2]["name"],"| subs:",len(nodes[2]["subtopics"]),"| toolsel02:",bool(toolsel.get("02")))
