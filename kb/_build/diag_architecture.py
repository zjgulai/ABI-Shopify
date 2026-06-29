# -*- coding: utf-8 -*-
import glob
import json
import os
import diag_common as d
from diag_common import txt,box,arrow
KB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS=sum(1 for _ in open(os.path.join(KB,"_rag","chunks.jsonl"),encoding="utf-8"))
DOCS=len(glob.glob(os.path.join(KB,"**","*.md"),recursive=True))
GRAPH=json.load(open(os.path.join(KB,"_kg","graph.json"),encoding="utf-8"))
ENTITIES=len(GRAPH["entities"])
RELATIONS=len(GRAPH["relations"])
INFO_SOURCES=10
f,ax=d.fig(16,12)  # 160 x 120
H=120
# ---- Title ----
txt(ax,7,H-6,"ABI 智能化独立站",size=29,color=d.INK,bold=True,ha="left")
txt(ax,7,H-10.3,"知识库 + 产品 总架构 · 让 Shopify 独立站从「人肉运营」升级为「AI 自动化经营」",size=12.5,color=d.GREEN,ha="left",bold=True)
txt(ax,153,H-6,"momcozy · 2026",size=10,color=d.GREY,ha="right")
txt(ax,153,H-11.3,f"{DOCS} 文档 · {CHUNKS} RAG块 · {ENTITIES} 实体/{RELATIONS} 关系 · {INFO_SOURCES} 信息源",size=9,color=d.GREY,ha="right")

# ---- 商业价值 ribbon ----
box(ax,4,99,140,8.5,fc=d.NAVY,ec=d.NAVY,r=0.5,z=2)
txt(ax,16,103.3,"商业价值",size=11,color="#FFFFFF",bold=True,z=4)
vals=[("降本","少人多店,Agent 顶替重复职能"),("提效","对话式建站/上架/投放"),("可复制","SOP + 插件 + 数据桥,开新店即用"),("可治理","人审 + 合规闸 + 图谱溯源")]
for i,(t,s) in enumerate(vals):
    x=33+i*27.3; box(ax,x,100,26,6.5,fc="#1C3A5E",ec="#2E5278",r=0.4,z=3)
    txt(ax,x+13,103.9,t,size=9.2,color="#7FE0B8",bold=True,z=5)
    txt(ax,x+13,101.2,s,size=6.3,color="#CFE0EF",z=5)

def band(y,h,fc,ec,tag,sub=""):
    box(ax,4,y,140,h,fc=fc,ec=ec,lw=1.6,r=0.5,z=2)
    box(ax,4,y,26,h,fc=ec,ec=ec,r=0.5,z=3)
    txt(ax,17,y+h/2+(1.7 if sub else 0),tag,size=11,color="#FFFFFF",bold=True,z=4)
    if sub: txt(ax,17,y+h/2-2.9,sub,size=7.6,color="#EAF2EE",z=4)
def chip(x,y,w,h,t,ec,sz=8.4,fc="#FFFFFF",sub=None):
    box(ax,x,y,w,h,fc=fc,ec=ec,lw=1.3,r=0.4,z=4)
    if sub:
        txt(ax,x+w/2,y+h*0.63,t,size=sz,color=d.INK,bold=True,z=5)
        txt(ax,x+w/2,y+h*0.27,sub,size=sz-2.0,color=d.GREY,z=5)
    else: txt(ax,x+w/2,y+h/2,t,size=sz,color=d.INK,bold=True,z=5)

# L1 消费/入口
band(87,9.5,"#FBEFD2","#C98A00","消费 / 入口","问·调·执行")
for i,(t,s) in enumerate([("网站","DeepSeek 问答"),("Claude Code 插件","7 skills+/命令"),("MCP 检索服务","kb_search/ask"),("运营 Agent","按节点路由")]):
    chip(33+i*27,88.8,25,6.4,t,"#E0B050",sz=8.8,sub=s)
# L2 产品/工具
band(72.5,12,"#E7E9F8","#5C6AC4","产品 / 工具层")
for i,(t,s) in enumerate([("网站+server.py","RAG+DeepSeek"),("腾讯云 Docker","隔离部署SOP"),("marketplace 插件","一键安装"),("Accio→Shopify","选品数据桥"),("商业图 ×4","全景/横/纵/矩阵")]):
    chip(33+i*21.6,74.8,20.4,6.6,t,"#9AA3DA",sz=7.6,sub=s)
# L3 机器层
band(59,11,"#D7EEF0","#0E7C86","机器可用层","RAG + 知识图谱")
chip(33,61.2,52,6.4,"RAG 检索","#5FA9B0",sz=9.3,sub=f"chunks.jsonl · {CHUNKS} 块 · 生产检索包(LSA→bge/OpenAI)")
chip(88,61.2,52,6.4,"知识图谱","#5FA9B0",sz=9.3,sub=f"{ENTITIES} 实体 / {RELATIONS} 关系(0 悬挂)· Mermaid")
# L4 内容层
band(37,19,"#DCF0E6","#008060","知识内容层","14 节点 + 深度专题")
nodes=["00 战略","01 选品","02 建站","03 上架","04 素材","05 营销","06 转化","07 数据","08 履约","09 会员","10 自动化"]
for i,n in enumerate(nodes): chip(33+i*9.9,49,9.2,5.0,n,"#7FBF9E",sz=6.9)
for i,n in enumerate(["90 AI能力地图","91 合规与风控","92 组织与SOP"]):
    chip(33+i*12.5,42.8,11.8,4.6,n,"#13294B",sz=7.2,fc="#EAEEF4")
txt(ax,33,40.0,"深度专题:代理式商务技术栈 · AI-Toolkit技能SOP · UCP接入 · Hydrogen脚手架 · 工具选型 · 全自动运营蓝图",size=7.0,color=d.GREEN,ha="left",bold=True)
# L5 信息源
band(17,18,"#E7F0FD","#2D6CDF","信息源层",f"{INFO_SOURCES} 源 · 萃取")
src=[("数字化中心周报","真实业务·SOP"),("Twitter 书签","行业发力点"),("Shopify 官方文档","平台能力"),("官方账号","Devs/Eng"),
("GitHub 开源","AI-Toolkit/UCP"),("YouTube Kevin","入门教程"),("YouTube Metics/AcH","实操视频"),("社区痛点","r/shopify 同类"),
("inbox 资料包","独立站实操"),("platform wiki","DTC/站外/AI")]
for i,(t,s) in enumerate(src):
    cx=33+(i%5)*21.6; cy=24.0 if i<5 else 18.2
    chip(cx,cy,20.4,5.2,t,"#9CC0F0",sz=6.8,sub=s)
# 人审 rail
box(ax,147,17,11,79.5,fc="#FFF4E8",ec=d.AMBER,lw=2,r=0.2,z=2)
txt(ax,152.5,91,"人审 /\n合规闸",size=10,color="#9A6A00",bold=True,z=5)
txt(ax,152.5,58,"贯穿所有层\n改价·支付·\n上线·采集\n→ 必经人审",size=7.8,color="#9A6A00",z=5)
# flow arrows (build bottom-up)
for y0,y1 in [(35,37),(56,59),(70.5,72.5),(82,87)]:
    arrow(ax,9,y0,9,y1,color=d.GREY,lw=1.9,mut=11,z=6)
txt(ax,4,13.5,"↑ 自下而上构建:萃取 → 结构化(RAG/KG)→ 产品化(网站/插件/部署)",size=9,color=d.INK,ha="left",bold=True)
txt(ax,4,9.6,"↓ 自上而下使用:提问 → 检索召回 → Agent 执行(人审兜底)",size=9,color=d.GREEN,ha="left",bold=True)
d.save(f,"00_ABI总架构_architecture")
