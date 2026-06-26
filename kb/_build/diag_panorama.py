# -*- coding: utf-8 -*-
import os
import diag_common as d
from diag_common import txt,box,arrow
KB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS=sum(1 for _ in open(os.path.join(KB,"_rag","chunks.jsonl"),encoding="utf-8"))
f,ax=d.fig(16,10)  # 160 x 100

# ---- Title ----
txt(ax,8,95.5,"ABI 智能化独立站",size=25,color=d.INK,bold=True,ha="left")
txt(ax,8,91,"全景图 · 知识库 + 产品 · 建站 → 全自动运营",size=13,color=d.GREEN,ha="left",bold=True)
txt(ax,157,95,"momcozy 独立站 · 2026",size=10,color=d.GREY,ha="right")
txt(ax,157,91.5,f"14 节点 · 8 源 · {CHUNKS} RAG块 · 213 实体/593 关系",size=9,color=d.GREY,ha="right")

def band(y,h,fc,ec,title,tcolor):
    box(ax,4,y,152,h,fc=fc,ec=ec,lw=1.6,r=0.6,z=2)
    box(ax,4,y,30,h,fc=ec,ec=ec,r=0.6,z=3)
    txt(ax,19,y+h/2,title,size=11.5,color="#FFFFFF",bold=True,z=4)

def chip(x,y,w,h,label,fc,ec,tc=d.INK,sz=9,sub=None,bold=True):
    box(ax,x,y,w,h,fc=fc,ec=ec,lw=1.3,r=0.5,z=4)
    if sub:
        txt(ax,x+w/2,y+h*0.62,label,size=sz,color=tc,bold=bold,z=5)
        txt(ax,x+w/2,y+h*0.3,sub,size=sz-2.2,color=d.GREY,z=5)
    else:
        txt(ax,x+w/2,y+h/2,label,size=sz,color=tc,bold=bold,z=5)

# ---- 编排层 ----
band(82,7,"#FBEFD2","#C98A00","编排层\n大脑",d.AMBER)
orch=["Claude/Codex 编排","CLAUDE.md 规范","Trellis 记忆","Skill 库","人审兜底"]
for i,t in enumerate(orch):
    chip(37+i*23.5,83.3,21.5,4.4,t,"#FFFFFF","#E0C064",sz=9)

# ---- Pipeline 00-10 ----
txt(ax,8,77.3,"全流程 00 → 10",size=11,color=d.INK,bold=True,ha="left")
nodes=[("00","战略定位",d.BLUEBG,d.BLUE),("01","选品调研",d.BLUEBG,d.BLUE),
("02","建站基建",d.MINT,d.GREEN),("03","上架Listing",d.MINT,d.GREEN),("04","内容素材",d.MINT,d.GREEN),
("05","营销引流",d.LAV,d.INDIGO),("06","转化CRO",d.LAV,d.INDIGO),
("07","数据归因",d.TEALBG,d.TEAL),("08","履约供应链",d.TEALBG,d.TEAL),("09","会员运营",d.TEALBG,d.TEAL),
("10","自动化",d.AMBERBG,d.AMBER)]
x0=5; w=12.9; gap=1.0; y=64; hh=10
xs=[]
for i,(num,name,fc,ec) in enumerate(nodes):
    x=x0+i*(w+gap); xs.append(x)
    box(ax,x,y,w,hh,fc=fc,ec=ec,lw=1.8,r=0.5,z=4)
    txt(ax,x+w/2,y+hh*0.66,num,size=15,color=ec,bold=True,z=5)
    txt(ax,x+w/2,y+hh*0.27,name,size=8.2,color=d.INK,z=5)
    if i<len(nodes)-1:
        arrow(ax,x+w,y+hh/2,x+w+gap,y+hh/2,color=d.GREY,lw=1.6,mut=9,z=3)
# feedback
arrow(ax,xs[9]+w/2,y+hh,xs[1]+w/2,y+hh,color=d.CORAL,lw=1.6,ls="--",mut=11,rad=-0.35,z=3)
txt(ax,(xs[1]+xs[9])/2+6,y+hh+5.2,"复购 / VOC 回流",size=8.5,color=d.CORAL,italic=True)

# ---- Shopify capability layer ----
band(46,11.5,d.MINT,d.GREEN,"Shopify\n原生能力",d.GREEN)
caps=["Sidekick / Pulse","Shopify Magic","Shopify Flow","Storefront / Dev MCP","Catalog API","UCP (与 Google)","Campaign Autopilot","Functions","Store AI / Hydrogen"]
cw=13.0
for i,c in enumerate(caps):
    cx=37+(i%5)*23.6 if i<5 else 37+(i-5)*23.6
    cy=52.4 if i<5 else 47.2
    chip(cx,cy,22.6,4.0,c,"#FFFFFF","#7FBF9E",sz=8.4)
for xi in [xs[2],xs[5],xs[7],xs[10]]:
    arrow(ax,xi+w/2,63.8,xi+w/2,57.6,color="#7FBF9E",lw=1.3,mut=8,z=3,style="-|>")

# ---- data base ----
band(31,11.5,d.TEALBG,d.TEAL,"数据底座",d.TEAL)
data=["Shopify 店铺数据","GA4 / GTM / BigQuery","UTM / 渠道归因","VOC / 舆情","竞品 / 市占 / CLV"]
for i,c in enumerate(data):
    chip(37+i*23.6,37.3,22.6,4.0,c,"#FFFFFF","#5FA9B0",sz=8.4)
for i,c in enumerate(["库存 / 海外仓 / 退款","会员 / 礼品卡","素材库 / 视频中心","埋点 / 看板","Reddit / 趋势"]):
    chip(37+i*23.6,32.4,22.6,4.0,c,"#FFFFFF","#5FA9B0",sz=8.4)

# ---- sources (left) ----
txt(ax,4,29.4,"信息源(8 源)",size=10.5,color=d.INK,bold=True,ha="left")
src=[("数字化中心周报","真实业务 · SOP"),("Twitter 书签 + 官方账号","发力点 · @ShopifyDevs"),("官方文档·GitHub·YouTube·社区","平台/开源/教程/痛点 +Accio")]
for i,(s,sub) in enumerate(src):
    chip(4,13+(2-i)*5.0,46,4.4,s,"#FFFFFF",d.LINE,sz=7.9,sub=sub)
    arrow(ax,50,15.2+(2-i)*5.0,56,21,color=d.GREY,lw=1.2,mut=8,rad=0.12,z=3)
txt(ax,52.5,26.5,"萃取",size=8.2,color=d.GREEN,italic=True)

# ---- KB core (center) · 14 节点分类(填补断点) ----
box(ax,58,12.5,46,15.5,fc="#EAF3EE",ec=d.GREEN,lw=1.8,r=0.4,z=3)
txt(ax,81,24.3,"ABI 知识库",size=11,color=d.GREEN,bold=True,z=5)
txt(ax,81,20.6,"14 节点分类",size=9,color=d.INK,bold=True,z=5)
txt(ax,81,17.4,"00–10 流程 · 90/91/92 横切",size=7.2,color=d.GREY,z=5)
txt(ax,81,14.5,"↑ 详见上方流程带",size=7.2,color=d.GREEN,italic=True,z=5)
arrow(ax,81,28,81,31,color=d.GREEN,lw=1.6,mut=10,ls="--",z=2)
arrow(ax,104,20.2,108,20.2,color=d.GREY,lw=1.4,mut=9,z=3)

# ---- outputs (right) ----
txt(ax,108,26.5,"产出 / 消费",size=11,color=d.INK,bold=True,ha="left")
outs=[("RAG 检索",f"chunks.jsonl · {CHUNKS} 块"),("知识图谱","213 实体 · 593 关系"),("商业图 ×4 + 网站","DeepSeek 问答"),("插件 + 数据桥","运营 Agent")]
for i,(s,sub) in enumerate(outs):
    cx=108+(i%2)*26; cy=15+(1-i//2)*5.6
    chip(cx,cy,24.5,4.8,s,"#FFFFFF",d.LINE,sz=9,sub=sub,)

# ---- crosscut footer ----
box(ax,4,4.5,152,5.4,fc=d.NAVY,ec=d.NAVY,r=0.5,z=2)
txt(ax,8,7.2,"横切层",size=10,color="#FFFFFF",bold=True,ha="left")
txt(ax,34,7.2,"90 AI 能力地图",size=9.5,color="#CFE8DC",ha="center")
txt(ax,74,7.2,"91 合规与风控",size=9.5,color="#CFE8DC",ha="center")
txt(ax,108,7.2,"92 组织与 SOP",size=9.5,color="#CFE8DC",ha="center")
txt(ax,140,7.2,"贯穿所有节点",size=9,color="#9FB3C8",italic=True,ha="center")

d.save(f,"01_全景图_panorama")
