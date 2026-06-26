# -*- coding: utf-8 -*-
import diag_common as d
from diag_common import txt,box,arrow
f,ax=d.fig(13,10); W=160; H=160*10/13  # 123
txt(ax,6,H-6,"纵向架构蓝图 · 三层编排",size=23,color=d.INK,bold=True,ha="left")
txt(ax,6,H-11.5,"大脑(编排) → 手脚(能力) → 地基(数据),写操作过人审闸",size=12,color=d.GREEN,ha="left",bold=True)

def layer(y,h,fc,ec,tag,title):
    box(ax,18,y,118,h,fc=fc,ec=ec,lw=1.8,r=0.25,z=2)
    box(ax,4,y,12,h,fc=ec,ec=ec,r=0.25,z=3)
    txt(ax,10,y+h/2,tag,size=11,color="#FFFFFF",bold=True,z=4,rot=90)
    txt(ax,22,y+h-5,title,size=12.5,color=ec,bold=True,ha="left",z=4)

def chip(x,y,w,h,t,ec,sz=8.6,fc="#FFFFFF"):
    box(ax,x,y,w,h,fc=fc,ec=ec,lw=1.3,r=0.25,z=4); 
    for k,ln in enumerate(t.split("\n")):
        txt(ax,x+w/2,y+h/2+(len(t.split("\n"))-1-2*k)*2.0,ln,size=sz,color=d.INK,z=5,bold=(k==0))

# L1 编排层
layer(96,22,d.AMBERBG,d.AMBER,"大脑","编排层 · 运营 Agent")
for i,t in enumerate(["Claude / Codex\n编排","CLAUDE.md\n行为规范","Trellis\n持久记忆","Skill 库\n(节点能力)","人审兜底\n+ 异常回滚"]):
    chip(22+i*22,98,20,11,t,d.AMBER)
# L2 能力层
layer(60,30,d.MINT,d.GREEN,"手脚","能力层 · 工具与接口")
row1=["Storefront / Dev\nMCP","Shopify Flow","Sidekick\n(+ App 扩展)","Shopify Magic","Campaign\nAutopilot"]
for i,t in enumerate(row1): chip(22+i*22,76,20,11,t,d.GREEN)
row2=["UCP / Catalog\n(AI 渠道)","外部工具链\n选品/素材/视频","自建中台\n广告/数据/会员","Functions /\nHydrogen","Store AI\n店面助手"]
for i,t in enumerate(row2): chip(22+i*22,63,20,11,t,d.GREEN)
# L3 数据层
layer(30,24,d.TEALBG,d.TEAL,"地基","数据层 · 单一事实源")
for i,t in enumerate(["Shopify 数据\n目录/订单/库存","GA4 / BigQuery\n归因","VOC / 舆情\n社区声量","竞品 / 市占\nCLV / 会员"]):
    chip(24+i*27,33,24,12,t,d.TEAL)

# flows
arrow(ax,77,96,77,90,color=d.AMBER,lw=2.2,mut=14,z=6); txt(ax,82,93,"指令 / 调用",size=8.6,color=d.AMBER,ha="left",italic=True)
arrow(ax,77,60,77,54,color=d.TEAL,lw=2.2,mut=14,z=6); txt(ax,82,57,"读写 / 执行",size=8.6,color=d.TEAL,ha="left",italic=True)
arrow(ax,64,30,64,57,color=d.GREY,lw=1.6,mut=11,z=1,ls="--",rad=0); txt(ax,52,44,"数据回流",size=8.2,color=d.GREY,italic=True,rot=90)

# human gate (right)
box(ax,140,30,15,88,fc="#FFF4E8",ec=d.AMBER,lw=2,r=0.15,z=2)
txt(ax,147.5,108,"人审 /\n审批闸",size=10.5,color="#9A6A00",bold=True,z=5)
for yy,t in [(86,"改价"),(74,"上下架"),(62,"退款"),(50,"投放预算"),(38,"发布上线")]:
    box(ax,142,yy,11,7,fc="#FFFFFF",ec=d.AMBER,r=0.3,z=4); txt(ax,147.5,yy+3.5,t,size=8,color="#9A6A00",z=5)
arrow(ax,136,75,140,75,color=d.AMBER,lw=1.6,mut=10,z=5)
txt(ax,80,24,"原则:读操作放手交给 Agent;不可逆写操作必须过人审闸(沿用 Campaign Autopilot「设预算→审批→执行」)",size=9,color=d.GREY,ha="center",italic=True)
d.save(f,"03_纵向架构蓝图_vertical")
