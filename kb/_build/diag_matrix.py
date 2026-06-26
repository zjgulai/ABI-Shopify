# -*- coding: utf-8 -*-
import diag_common as d
from diag_common import txt,box
f,ax=d.fig(15,10)  # 160 x 106.7
H=106.7
txt(ax,6,H-6,"节点 × Shopify 能力 矩阵",size=23,color=d.INK,bold=True,ha="left")
txt(ax,6,H-11,"每个节点由哪些 Shopify 原生 AI 能力支撑(✓)",size=12,color=d.GREEN,ha="left",bold=True)

caps=[("Sidekick","S"),("Pulse","S"),("Magic","C"),("Flow","A"),("Storefront\nMCP","M"),
("Dev MCP","M"),("Catalog\nAPI","M"),("AI Toolkit","M"),("Campaign\nAutopilot","A"),
("Store AI","C"),("UCP","M"),("Hydrogen","B"),("Functions","B"),("Sidekick\n扩展","S")]
catcol={"S":d.INDIGO,"C":d.GREEN,"A":d.AMBER,"M":d.TEAL,"B":d.BLUE}
rows=[("00 战略与定位",[]),("01 选品与市场调研",[6,10]),("02 建站与基础设施",[5,7,11,12]),
("03 商品上架与Listing",[2,6,9,12]),("04 内容与素材生产",[0,2]),("05 营销与引流",[0,2,8,13]),
("06 转化优化CRO",[1,11,12]),("07 数据与归因",[0,1]),("08 订单履约与供应链",[3,4]),
("09 客户与会员运营",[4,9,10,13]),("10 自动化编排",[0,3,4,5,6,7,10,13])]
# layout
x0=44; y0=12; cw=8.0; ch=6.3; n=len(caps); m=len(rows)
top=y0+m*ch
# column headers
for j,(c,cat) in enumerate(caps):
    cx=x0+j*cw
    box(ax,cx+0.4,top+0.6,cw-0.8,7.5,fc=catcol[cat],ec=catcol[cat],r=0.18,z=3)
    txt(ax,cx+cw/2,top+4.3,c,size=7.2,color="#FFFFFF",bold=True,z=5)
# rows
for i,(rname,sup) in enumerate(rows):
    ry=top-(i+1)*ch
    box(ax,6,ry+0.4,37,ch-0.8,fc="#FFFFFF",ec=d.LINE,r=0.12,z=3)
    txt(ax,9,ry+ch/2,rname,size=9.2,color=d.INK,ha="left",bold=True,z=5)
    for j in range(n):
        cx=x0+j*cw
        on=j in sup
        fc=catcol[caps[j][1]] if on else "#EEF2F7"
        box(ax,cx+0.4,ry+0.4,cw-0.8,ch-0.8,fc=fc,ec=("#FFFFFF" if on else d.LINE),lw=1,r=0.12,z=3)
        if on: txt(ax,cx+cw/2,ry+ch/2,"✓",size=11,color="#FFFFFF",bold=True,z=5)
# legend
ly=7
cats=[("S","Sidekick 家族"),("M","MCP / Catalog / UCP"),("C","内容 / 店面 AI"),("A","自动化 / 投放"),("B","建站 / 结账")]
for i,(k,lab) in enumerate(cats):
    lx=6+i*30
    box(ax,lx,ly,3.2,3.2,fc=catcol[k],ec=catcol[k],r=0.2,z=3)
    txt(ax,lx+4.2,ly+1.6,lab,size=8.6,color=d.INK,ha="left")
txt(ax,158,ly+1.6,"来源:知识图谱 SUPPORTS 关系",size=8,color=d.GREY,ha="right",italic=True)
d.save(f,"04_节点能力矩阵_matrix")
